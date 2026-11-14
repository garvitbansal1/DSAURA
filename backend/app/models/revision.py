import uuid
from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class RevisionSchedule(Base):
    __tablename__ = "revision_schedules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    interval_days = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    repetition_count = Column(Integer, default=0)
    last_revised_at = Column(DateTime, nullable=True)
    problem = relationship("Problem")
