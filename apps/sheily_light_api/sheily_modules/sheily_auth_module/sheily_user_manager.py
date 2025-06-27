from typing import Dict, Optional
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from sheily_light_api.core.database import SessionLocal
from sheily_light_api.models import User
from .sheily_jwt_manager import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------ helpers ------------------

def _get_user(db, username: str) -> Optional[User]:
    return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

# ------------------ API functions ------------------

def register_user(payload: Dict):
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return {"error": "username and password required"}

    db = SessionLocal()
    try:
        if _get_user(db, username):
            return {"error": "User exists"}
        user = User(username=username, hashed_password=pwd_context.hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"detail": "registered"}
    except IntegrityError:
        db.rollback()
        return {"error": "User exists"}
    finally:
        db.close()


def login_user(payload: Dict):
    username = payload.get("username")
    password = payload.get("password")
    db = SessionLocal()
    try:
        user = _get_user(db, username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return {"error": "invalid credentials"}
        token = create_access_token(subject=username)
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()


def logout_user(_: Dict):
    # With stateless JWT nothing to do; client discards token.
    return {"detail": "logged_out"}
