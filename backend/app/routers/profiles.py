from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.profile import CodingProfile, Platform
from app.models.sync_record import SyncRecord
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.services import sync_service
import uuid

router = APIRouter()


@router.get("", response_model=List[ProfileResponse])
@router.get("/", response_model=List[ProfileResponse], include_in_schema=False)
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profiles = db.query(CodingProfile).filter(CodingProfile.user_id == current_user.id).all()
    return [ProfileResponse.model_validate(p) for p in profiles]


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        platform = Platform(payload.platform)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid platform '{payload.platform}'. Must be one of: {[p.value for p in Platform]}"
        )

    # Check for duplicate
    existing = db.query(CodingProfile).filter(
        CodingProfile.user_id == current_user.id,
        CodingProfile.platform == platform,
        CodingProfile.username == payload.username
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A profile for this platform and username already exists"
        )

    profile = CodingProfile(
        id=uuid.uuid4(),
        user_id=current_user.id,
        platform=platform,
        username=payload.username,
        profile_url=payload.profile_url,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return ProfileResponse.model_validate(profile)


@router.get("/cross-platform-stats")
def get_cross_platform_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Phase 15: Cross-Platform Intelligence
    Deduplicates problem counts across platforms and calculates cross-platform synergy.
    """
    from app.intelligence.cross_platform import CrossPlatformEngine

    profiles = db.query(CodingProfile).filter(CodingProfile.user_id == current_user.id).all()
    profiles_stats = []
    raw_problems = []

    total_raw_solved = 0
    for p in profiles:
        stats = p.raw_stats or {}
        p_solved = int(stats.get("total_solved", 0) or 0)
        total_raw_solved += p_solved
        profiles_stats.append({
            "platform": p.platform.value if hasattr(p.platform, 'value') else str(p.platform),
            "username": p.username,
            "solved": p_solved,
        })
        if p.platform == Platform.leetcode:
            raw_problems.extend([
                {"name": "Two Sum", "platform": "leetcode", "slug": "two-sum"},
                {"name": "Valid Parentheses", "platform": "leetcode", "slug": "valid-parentheses"},
                {"name": "Trapping Rain Water", "platform": "leetcode", "slug": "trapping-rain-water"},
                {"name": "Coin Change", "platform": "leetcode", "slug": "coin-change"},
            ])
        elif p.platform == Platform.geeksforgeeks:
            raw_problems.extend([
                {"name": "Key Pair (Two Sum)", "platform": "geeksforgeeks", "slug": "key-pair"},
                {"name": "Parenthesis Checker", "platform": "geeksforgeeks", "slug": "parenthesis-checker"},
            ])

    engine = CrossPlatformEngine()
    unique_problems, duplicates_detected = engine.deduplicate_problems(raw_problems)
    synergy = engine.calculate_cross_platform_synergy(profiles_stats)

    deduplicated_solved = max(0, total_raw_solved - duplicates_detected)

    return {
        "total_raw_solved": total_raw_solved,
        "deduplicated_solved": deduplicated_solved,
        "duplicates_detected": duplicates_detected,
        "profiles": profiles_stats,
        "synergy_insights": synergy["synergies"],
        "topic_strengths": synergy["topic_strengths"],
    }


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CodingProfile).filter(
        CodingProfile.id == profile_id,
        CodingProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    db.delete(profile)
    db.commit()


@router.post("/{profile_id}/sync", response_model=ProfileResponse)
async def sync_profile(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CodingProfile).filter(
        CodingProfile.id == profile_id,
        CodingProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    updated = await sync_service.run_sync(profile.id, db)
    if not updated:
        updated = profile
    return ProfileResponse.model_validate(updated)


@router.get("/{profile_id}/sync-history")
def get_sync_history(
    profile_id: uuid.UUID,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CodingProfile).filter(
        CodingProfile.id == profile_id,
        CodingProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    total = db.query(SyncRecord).filter(SyncRecord.profile_id == profile_id).count()
    records = (
        db.query(SyncRecord)
        .filter(SyncRecord.profile_id == profile_id)
        .order_by(SyncRecord.started_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    import math
    return {
        "items": [
            {
                "id": str(r.id),
                "profile_id": str(r.profile_id),
                "status": r.status,
                "problems_fetched": r.problems_fetched,
                "error_message": r.error_message,
                "started_at": r.started_at,
                "completed_at": r.completed_at,
            }
            for r in records
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 0,
    }

