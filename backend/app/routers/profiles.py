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


@router.get("/", response_model=List[ProfileResponse])
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profiles = db.query(CodingProfile).filter(CodingProfile.user_id == current_user.id).all()
    return [ProfileResponse.model_validate(p) for p in profiles]


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
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


@router.post("/{profile_id}/sync")
def sync_profile(
    profile_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CodingProfile).filter(
        CodingProfile.id == profile_id,
        CodingProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    background_tasks.add_task(sync_service.run_sync_background, str(profile_id))
    return {"message": "Sync started", "profile_id": str(profile_id)}


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
