import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import enum


class ExperienceLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class PreferredLanguage(str, enum.Enum):
    java = "java"
    python = "python"


class LearningGoal(str, enum.Enum):
    placement = "placement"
    competitive = "competitive"
    interview = "interview"
    fundamentals = "fundamentals"
    advanced = "advanced"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    experience_level = Column(SAEnum(ExperienceLevel), nullable=True)
    preferred_language = Column(SAEnum(PreferredLanguage), default=PreferredLanguage.python)
    learning_goal = Column(SAEnum(LearningGoal), nullable=True)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
