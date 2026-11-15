import uuid
from datetime import datetime, date
from sqlalchemy import Column, Float, String, Date, DateTime, ForeignKey, Integer, JSON
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from app.database import Base


class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("dsa_topics.id"), nullable=True)
    mastery_score = Column(Float, default=0.0)
    mastery_level = Column(String(50), nullable=True)
    snapshot_date = Column(Date, default=date.today)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    reason = Column(String(1000), nullable=True)
    expected_outcome = Column(String(500), nullable=True)
    priority = Column(Integer, default=5)
    status = Column(String(50), default="pending")  # pending, dismissed, completed
    generated_at = Column(DateTime, default=datetime.utcnow)
    dismissed_at = Column(DateTime, nullable=True)
    problem = relationship("Problem")
