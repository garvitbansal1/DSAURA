import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SyncRecord(Base):
    __tablename__ = "sync_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("coding_profiles.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)  # success, failed, partial
    problems_fetched = Column(Integer, default=0)
    error_message = Column(String(1000), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    profile = relationship("CodingProfile", back_populates="sync_records")
