"""Utility router providing real-time auxiliary data for the frontend.
Currently exposes /time returning the server's local time in ISO format.
"""
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/time")
def current_time():
    """Return current server local time as HH:MM:SS string."""
    return {"now": datetime.now().strftime("%H:%M:%S")}
