import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

pattern_prerequisites = Table(
    "pattern_prerequisites", Base.metadata,
    Column("pattern_id", UUID(as_uuid=True), ForeignKey("dsa_patterns.id"), primary_key=True),
    Column("prerequisite_id", UUID(as_uuid=True), ForeignKey("dsa_patterns.id"), primary_key=True)
)


class DSAPattern(Base):
    __tablename__ = "dsa_patterns"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("dsa_topics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    explanation = Column(String(5000), nullable=True)
    when_to_use = Column(String(2000), nullable=True)
    recognition_clues = Column(String(2000), nullable=True)
    common_keywords = Column(JSON, default=[])
    pseudocode = Column(String(5000), nullable=True)
    java_template = Column(String(5000), nullable=True)
    python_template = Column(String(5000), nullable=True)
    time_complexity = Column(String(100), nullable=True)
    space_complexity = Column(String(100), nullable=True)
    common_mistakes = Column(JSON, default=[])
    difficulty_level = Column(String(50), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    topic = relationship("DSATopic", back_populates="patterns")
    prerequisites = relationship(
        "DSAPattern",
        secondary=pattern_prerequisites,
        primaryjoin=lambda: DSAPattern.id == pattern_prerequisites.c.pattern_id,
        secondaryjoin=lambda: DSAPattern.id == pattern_prerequisites.c.prerequisite_id,
    )
