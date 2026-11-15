import asyncio
import uuid
from typing import Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.profile import CodingProfile, Platform, SyncStatus
from app.models.sync_record import SyncRecord
from app.integrations.leetcode import LeetCodeIntegration
from app.integrations.codeforces import CodeforcesIntegration
from app.integrations.geeksforgeeks import GFGIntegration
from app.integrations.hackerrank import HackerRankIntegration

INTEGRATION_MAP = {
    Platform.leetcode: LeetCodeIntegration,
    Platform.codeforces: CodeforcesIntegration,
    Platform.geeksforgeeks: GFGIntegration,
    Platform.hackerrank: HackerRankIntegration,
}


def _to_uuid(val: Any) -> Any:
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(str(val))
    except Exception:
        return val


async def run_sync(profile_id: Any, db: Session) -> Optional[CodingProfile]:
    p_uuid = _to_uuid(profile_id)
    profile = db.query(CodingProfile).filter(CodingProfile.id == p_uuid).first()
    if not profile:
        return None

    sync_record = SyncRecord(profile_id=profile.id, status="running", started_at=datetime.utcnow())
    db.add(sync_record)
    profile.sync_status = SyncStatus.syncing
    db.commit()

    try:
        integration_class = INTEGRATION_MAP.get(profile.platform)
        if not integration_class:
            raise ValueError(f"Unknown platform: {profile.platform}")
        integration = integration_class()
        stats = await integration.fetch_stats(profile.username)

        profile.raw_stats = stats
        profile.last_synced_at = datetime.utcnow()
        profile.sync_status = SyncStatus.success
        profile.is_verified = True
        sync_record.status = "success"
        sync_record.problems_fetched = int(stats.get("total_solved", 0) or 0)

        # Populate user problem history to drive topic intelligence & mastery engine
        try:
            from app.routers.mastery import ensure_user_problem_history
            ensure_user_problem_history(profile.user_id, db)
        except Exception:
            pass

    except Exception as e:
        profile.sync_status = SyncStatus.failed
        sync_record.status = "failed"
        sync_record.error_message = str(e)[:900]
    finally:
        sync_record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(profile)

    return profile


def run_sync_background(profile_id: str):
    """Synchronous wrapper for background tasks (FastAPI BackgroundTasks)."""
    db = SessionLocal()
    try:
        asyncio.run(run_sync(profile_id, db))
    finally:
        db.close()
