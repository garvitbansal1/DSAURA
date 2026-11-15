from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.user import UserPublic


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    experience_level: Optional[str] = None
    learning_goal: Optional[str] = None
    preferred_language: Optional[str] = "python"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepass123",
                "experience_level": "beginner",
                "learning_goal": "placement",
                "preferred_language": "python"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
