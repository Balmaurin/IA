from datetime import datetime
from sqlalchemy.orm import Session

from sheily_light_api.models import ChatMessage, User
from sheily_light_api.sheily_modules.sheily_chat_module \
    .sheily_chat_local_engine import ask_local_ai
from sheily_light_api.sheily_modules.sheily_chat_module.search_utils import (
    needs_search, google_search
)


def chat_with_local_ai(db: Session, user: User, prompt: str) -> str:
    """Send prompt to local AI, store chat message and return response."""
    enriched_prompt = prompt
    if needs_search(prompt):
        search_summary = google_search(prompt)
        if search_summary:
            enriched_prompt += (
                "\n\n[DATO EN TIEMPO REAL]\n"
                f"{search_summary}"
            )
    response = ask_local_ai(enriched_prompt)
    chat = ChatMessage(
        user_id=user.id,
        prompt=prompt,
        response=response,
        created_at=datetime.utcnow()
    )
    db.add(chat)
    db.commit()
    return response


def get_chat_history(db: Session, user: User, limit: int = 20):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
