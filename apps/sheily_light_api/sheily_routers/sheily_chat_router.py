from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sheily_light_api.core.database import get_db, get_db_dep
from sheily_light_api.models import User, ChatMessage
from sheily_light_api.core.security import get_current_user
from sheily_light_api.sheily_modules.sheily_chat_module.sheily_chat_service import (
    chat_with_local_ai,
    get_chat_history,
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatPrompt(BaseModel):
    message: str


class ChatRequest(BaseModel):
    prompt: str


@router.post("/local", response_model=Dict[str, str])
async def chat_local(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """Send a chat message to the local AI and get a response."""
    response = chat_with_local_ai(db, current_user, request.prompt)
    return {"answer": response}


@router.get("/history")
def history(
    limit: int = 20,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, str]]:
    """Get chat history for the current user."""
    records = get_chat_history(db, user, limit)
    return [{"prompt": r.prompt, "response": r.response, "created_at": r.created_at.isoformat()} for r in records]


@router.post("/")
def chat_endpoint(
    prompt: ChatPrompt,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep),
) -> Dict[str, str]:
    """Main chat endpoint that forwards messages to the local AI."""
    response = chat_with_local_ai(db, user, prompt.message)
    return {"answer": response}


@router.post("/v1/chat")
def chat_endpoint_alias(
    prompt: ChatPrompt,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep),
) -> Dict[str, str]:
    """Alias for the main chat endpoint with v1 prefix."""
    response = chat_with_local_ai(db, user, prompt.message)
    return {"answer": response}  # Alias para compatibilidad: /api/chat/chat/


@router.post("/chat/")
def chat_endpoint_alias(
    prompt: ChatPrompt,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep),
):
    return chat_endpoint(prompt, user, db)
