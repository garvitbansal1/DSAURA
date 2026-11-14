from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    avatar_url: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_language: Optional[str] = None
    learning_goal: Optional[str] = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_language: Optional[str] = None
    learning_goal: Optional[str] = None
