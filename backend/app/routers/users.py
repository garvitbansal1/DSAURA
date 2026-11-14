from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, ExperienceLevel, PreferredLanguage, LearningGoal
from app.schemas.user import UserPublic, UserUpdateRequest
from datetime import datetime

router = APIRouter()


@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_user)):
    return UserPublic.model_validate(current_user)


@router.patch("/me", response_model=UserPublic)
def update_me(
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.name is not None:
        current_user.name = payload.name

    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url

    if payload.experience_level is not None:
        try:
            current_user.experience_level = ExperienceLevel(payload.experience_level)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid experience_level: {payload.experience_level}")

    if payload.preferred_language is not None:
        try:
            current_user.preferred_language = PreferredLanguage(payload.preferred_language)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid preferred_language: {payload.preferred_language}")

    if payload.learning_goal is not None:
        try:
            current_user.learning_goal = LearningGoal(payload.learning_goal)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid learning_goal: {payload.learning_goal}")

    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return UserPublic.model_validate(current_user)
