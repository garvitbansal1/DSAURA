from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, ExperienceLevel, PreferredLanguage, LearningGoal
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, RefreshRequest,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.schemas.user import UserPublic
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
import uuid

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )

    # Validate enums if provided
    exp_level = None
    if payload.experience_level:
        try:
            exp_level = ExperienceLevel(payload.experience_level)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid experience_level: {payload.experience_level}")

    goal = None
    if payload.learning_goal:
        try:
            goal = LearningGoal(payload.learning_goal)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid learning_goal: {payload.learning_goal}")

    pref_lang = PreferredLanguage.python
    if payload.preferred_language:
        try:
            pref_lang = PreferredLanguage(payload.preferred_language)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid preferred_language: {payload.preferred_language}")

    new_user = User(
        id=uuid.uuid4(),
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        experience_level=exp_level,
        learning_goal=goal,
        preferred_language=pref_lang,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token_data = {"sub": str(new_user.id), "email": new_user.email, "name": new_user.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserPublic.model_validate(new_user),
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    token_data = {"sub": str(user.id), "email": user.email, "name": user.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserPublic.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    token_payload = decode_token(payload.refresh_token)
    if token_payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = token_payload.get("sub")
    try:
        uid = uuid.UUID(str(user_id))
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token identity")
    user = db.query(User).filter(User.id == uid, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    token_data = {"sub": str(user.id), "email": user.email, "name": user.name}
    access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        user=UserPublic.model_validate(user),
    )


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Always return success to avoid user enumeration
    return {"message": "If this email exists, a reset link will be sent."}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Placeholder: in production, validate token from a password reset tokens table
    return {"message": "Password has been reset successfully. Please log in with your new password."}
