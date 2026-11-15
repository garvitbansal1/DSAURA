import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

problem_topics = Table(
    "problem_topics", Base.metadata,
    Column("problem_id", UUID(as_uuid=True), ForeignKey("problems.id"), primary_key=True),
    Column("topic_id", UUID(as_uuid=True), ForeignKey("dsa_topics.id"), primary_key=True)
)

problem_patterns = Table(
    "problem_patterns", Base.metadata,
    Column("problem_id", UUID(as_uuid=True), ForeignKey("problems.id"), primary_key=True),
    Column("pattern_id", UUID(as_uuid=True), ForeignKey("dsa_patterns.id"), primary_key=True),
    Column("confidence", Float, default=1.0)
)


class Problem(Base):
    __tablename__ = "problems"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String(50), nullable=False)
    platform_id = Column(String(255), nullable=False)
    name = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=True)
    difficulty = Column(String(50), nullable=True)  # easy, medium, hard
    classification_confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    topics = relationship("DSATopic", secondary=problem_topics)
    patterns = relationship("DSAPattern", secondary=problem_patterns)
