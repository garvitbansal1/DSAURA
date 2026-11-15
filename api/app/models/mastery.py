import uuid
from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class UserTopicMastery(Base):
    __tablename__ = "user_topic_mastery"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("dsa_topics.id"), nullable=False)
    mastery_score = Column(Float, default=0.0)
    mastery_level = Column(String(50), default="insufficient_evidence")
    evidence_confidence = Column(Float, default=0.0)
    score_breakdown = Column(JSON, default={})
    evidence_summary = Column(JSON, default={})
    calculated_at = Column(DateTime, default=datetime.utcnow)
    topic = relationship("DSATopic")
    user = relationship("User")


class UserPatternMastery(Base):
    __tablename__ = "user_pattern_mastery"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pattern_id = Column(UUID(as_uuid=True), ForeignKey("dsa_patterns.id"), nullable=False)
    mastery_score = Column(Float, default=0.0)
    mastery_level = Column(String(50), default="insufficient_evidence")
    evidence_confidence = Column(Float, default=0.0)
    problems_attempted = Column(Float, default=0)
    problems_solved = Column(Float, default=0)
    score_breakdown = Column(JSON, default={})
    calculated_at = Column(DateTime, default=datetime.utcnow)
    pattern = relationship("DSAPattern")
    user = relationship("User")
