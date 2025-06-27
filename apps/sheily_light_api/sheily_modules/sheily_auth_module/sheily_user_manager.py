from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from passlib.context import CryptContext

from sheily_light_api.core.database import SessionLocal
from sheily_light_api.models import User
from .sheily_jwt_manager import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------ helpers ------------------

def _get_user(db: Session, username: str) -> Optional[User]:
    return db.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()


# ------------------ API functions ------------------


def register_user(payload: Dict[str, str]) -> Dict[str, str]:
    """Register a new user with the provided credentials.

    Args:
        payload: Dictionary containing 'username' and 'password' keys

    Returns:
        Dict with operation result or error message
    """
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}

    if len(password) < 8:
        return {"error": "Password must be at least 8 characters long"}

    db = SessionLocal()
    try:
        # Check if user already exists
        if _get_user(db, username):
            return {"error": "Username already exists"}

        # Create new user
        user = User(
            username=username,
            hashed_password=pwd_context.hash(password)
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"detail": "User registered successfully"}

    except Exception as e:
        db.rollback()
        return {"error": f"Registration failed: {str(e)}"}
        
    finally:
        db.close()


def login_user(payload: Dict[str, str]) -> Dict[str, str]:
    """Authenticate a user and return an access token if successful.

    Args:
        payload: Dictionary containing 'username' and 'password' keys

    Returns:
        Dict with access token on success, or error message on failure
    """
    username = payload.get("username")
    password = payload.get("password")
    
    if not username or not password:
        return {"error": "Username and password are required"}
    
    db = SessionLocal()
    try:
        # Get user from database
        user = _get_user(db, username)

        # Verify user exists and password is correct
        if not user or not pwd_context.verify(password, user.hashed_password):
            # Use generic message to avoid user enumeration
            return {"error": "Invalid username or password"}
        
        # Generate JWT token
        token = create_access_token(subject=username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user.id)
        }

    except Exception as e:
        # Log the actual error for debugging
        print(f"Login error: {str(e)}")
        return {"error": "Authentication failed. Please try again later."}

    finally:
        db.close()


def logout_user(_: Dict[str, str]) -> Dict[str, str]:
    """Handle user logout (client-side token invalidation).

    Note: Since JWT is stateless, the actual invalidation must be handled
    client-side by discarding the token. This endpoint is provided for
    API consistency.

    Args:
        _: Unused payload for API consistency

    Returns:
        Dict with logout confirmation message
    """
    return {"detail": "Successfully logged out. Please discard your token."}
