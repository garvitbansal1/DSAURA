import pytest
import uuid
from app.integrations.leetcode import LeetCodeIntegration
from app.integrations.codeforces import CodeforcesIntegration
from app.integrations.geeksforgeeks import GFGIntegration
from app.integrations.hackerrank import HackerRankIntegration
from app.services.sync_service import run_sync
from app.models.profile import CodingProfile, Platform, SyncStatus
from app.models.user import User
from app.database import Base, engine, SessionLocal


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.mark.asyncio
async def test_integrations_fetch_stats():
    lc = LeetCodeIntegration()
    stats = await lc.fetch_stats("test_dev")
    assert stats["available"] is True
    assert stats["total_solved"] > 0
    assert stats["username"] == "test_dev"

    cf = CodeforcesIntegration()
    cf_stats = await cf.fetch_stats("tourist")
    assert cf_stats["available"] is True
    assert cf_stats["total_solved"] > 0

    gfg = GFGIntegration()
    gfg_stats = await gfg.fetch_stats("test_gfg")
    assert gfg_stats["available"] is True
    assert gfg_stats["total_solved"] > 0

    hr = HackerRankIntegration()
    hr_stats = await hr.fetch_stats("test_hr")
    assert hr_stats["available"] is True
    assert hr_stats["total_solved"] > 0


@pytest.mark.asyncio
async def test_run_sync_service(db_session):
    # Ensure a test user exists
    user = db_session.query(User).first()
    if not user:
        user = User(
            id=uuid.uuid4(),
            email="test_sync@dsaura.dev",
            name="Sync Tester",
            password_hash="fakehash",
        )
        db_session.add(user)
        db_session.commit()

    profile = CodingProfile(
        id=uuid.uuid4(),
        user_id=user.id,
        platform=Platform.leetcode,
        username="dsaura_tester",
    )
    db_session.add(profile)
    db_session.commit()

    synced_profile = await run_sync(profile.id, db_session)
    assert synced_profile is not None
    assert synced_profile.sync_status == SyncStatus.success
    assert synced_profile.raw_stats is not None
    assert synced_profile.raw_stats.get("total_solved", 0) > 0
    assert synced_profile.last_synced_at is not None
