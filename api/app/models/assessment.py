import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("dsa_topics.id"), nullable=True)
    session_type = Column(String(50), default="mixed")  # pattern_recognition, mcq, pseudocode, mixed
    score = Column(Float, default=0.0)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    responses = relationship("AssessmentResponse", back_populates="session", cascade="all, delete-orphan")


class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False)
    pattern_id = Column(UUID(as_uuid=True), ForeignKey("dsa_patterns.id"), nullable=True)
    question_type = Column(String(50), nullable=False)
    question_data = Column(JSON, nullable=False)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_taken_seconds = Column(Integer, default=0)
    session = relationship("AssessmentSession", back_populates="responses")
