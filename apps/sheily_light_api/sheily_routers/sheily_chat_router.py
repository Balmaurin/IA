from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from sheily_light_api.dependencies import get_current_user, get_db_dep
from sheily_light_api.models import User
from sheily_light_api.sheily_modules.sheily_chat_module \
    .sheily_chat_service import chat_with_local_ai, get_chat_history

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatPrompt(BaseModel):
    message: str


@router.get("/history")
def history(
    limit: int = 20,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep)
):
    """Get chat history for the current user."""
    records = get_chat_history(db, user, limit)
    return [
        {
            "prompt": r.prompt,
            "response": r.response,
            "created_at": r.created_at.isoformat()
        } for r in records
    ]


@router.post("/")
def chat_endpoint(
    prompt: ChatPrompt,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep),
):
    response = chat_with_local_ai(db, user, prompt.message)
    return {"answer": response}


# Alias para compatibilidad: /api/chat/chat/


@router.post("/chat/")
def chat_endpoint_alias(
    prompt: ChatPrompt,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_dep),
):
    return chat_endpoint(prompt, user, db)
