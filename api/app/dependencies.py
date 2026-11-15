import uuid
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def _to_uuid(val: any) -> Optional[uuid.UUID]:
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(str(val))
    except (ValueError, TypeError):
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")
    email = payload.get("email")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    uid = _to_uuid(user_id)
    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token identity")
        
    user = db.query(User).filter(User.id == uid, User.is_active == True).first()
    if not user and email:
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        
    if not user and email:
        # Re-hydrate the authenticated user into this serverless container's ephemeral DB
        from app.utils.security import hash_password
        user = User(
            id=uid,
            name=payload.get("name") or "Test Architect",
            email=email,
            password_hash=hash_password("Password123!"),
        )
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            from app.routers.mastery import ensure_user_problem_history
            ensure_user_problem_history(user.id, db)
        except Exception:
            db.rollback()
            user = db.query(User).filter((User.id == uid) | (User.email == email)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user


def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            return None
        uid = _to_uuid(user_id)
        if not uid:
            return None
        user = db.query(User).filter(User.id == uid, User.is_active == True).first()
        if not user and payload.get("email"):
            user = db.query(User).filter(User.email == payload.get("email"), User.is_active == True).first()
        return user
    except Exception:
        return None
