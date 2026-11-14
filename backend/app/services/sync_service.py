import asyncio
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


async def run_sync(profile_id: str, db: Session):
    profile = db.query(CodingProfile).filter(CodingProfile.id == profile_id).first()
    if not profile:
        return

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
        sync_record.status = "success"
        sync_record.problems_fetched = stats.get("total_solved", 0)
    except Exception as e:
        profile.sync_status = SyncStatus.failed
        sync_record.status = "failed"
        sync_record.error_message = str(e)[:900]
    finally:
        sync_record.completed_at = datetime.utcnow()
        db.commit()


def run_sync_background(profile_id: str):
    """Synchronous wrapper for background tasks (FastAPI BackgroundTasks)."""
    db = SessionLocal()
    try:
        asyncio.run(run_sync(profile_id, db))
    finally:
        db.close()
