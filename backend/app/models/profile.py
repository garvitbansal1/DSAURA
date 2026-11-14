import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Platform(str, enum.Enum):
    leetcode = "leetcode"
    codeforces = "codeforces"
    geeksforgeeks = "geeksforgeeks"
    hackerrank = "hackerrank"


class SyncStatus(str, enum.Enum):
    never = "never"
    pending = "pending"
    syncing = "syncing"
    success = "success"
    failed = "failed"


class CodingProfile(Base):
    __tablename__ = "coding_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform = Column(SAEnum(Platform), nullable=False)
    username = Column(String(255), nullable=False)
    profile_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    last_synced_at = Column(DateTime, nullable=True)
    raw_stats = Column(JSON, default={})
    sync_status = Column(SAEnum(SyncStatus), default=SyncStatus.never)
    created_at = Column(DateTime, default=datetime.utcnow)
    sync_records = relationship("SyncRecord", back_populates="profile", cascade="all, delete-orphan")
    user = relationship("User", backref="coding_profiles")
