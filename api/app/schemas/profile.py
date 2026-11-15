from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    platform: str
    username: str
    profile_url: Optional[str] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    platform: str
    username: str
    profile_url: Optional[str] = None
    is_verified: bool
    last_synced_at: Optional[datetime] = None
    sync_status: str
    created_at: datetime
    raw_stats: Optional[Dict[str, Any]] = None
