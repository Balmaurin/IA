from datetime import datetime
from sqlalchemy.orm import Session

from sheily_light_api.models import ChatMessage, User
from sheily_light_api.sheily_modules.sheily_chat_module.sheily_chat_local_engine import (
    ask_local_ai,
)
from sheily_light_api.sheily_modules.sheily_chat_module.search_utils import (
    needs_search,
    google_search,
)


def chat_with_local_ai(db: Session, user: User, prompt: str) -> str:
    """
    Envía un mensaje a la IA local, almacena la conversación y devuelve la respuesta.

    Args:
        db: Sesión de base de datos
        user: Usuario que realiza la consulta
        prompt: Mensaje del usuario

    Returns:
        str: Respuesta generada por la IA
    """
    # Enriquecer el prompt con búsqueda si es necesario
    enriched_prompt = _enrich_prompt_with_search(prompt)

    # Obtener respuesta de la IA
    response = ask_local_ai(enriched_prompt)

    # Registrar la conversación en la base de datos
    _save_chat_message(db, user.id, prompt, response)

    return response


def _enrich_prompt_with_search(prompt: str) -> str:
    """Añade información de búsqueda al prompt si es necesario."""
    if needs_search(prompt):
        search_summary = google_search(prompt)
        if search_summary:
            return f"{prompt}\n\n[DATO EN TIEMPO REAL]\n{search_summary}"
    return prompt


def _save_chat_message(db: Session, user_id: int, prompt: str, response: str) -> None:
    """Guarda un mensaje de chat en la base de datos."""
    chat = ChatMessage(user_id=user_id, prompt=prompt, response=response, created_at=datetime.utcnow())
    db.add(chat)
    db.commit()


def get_chat_history(db: Session, user: User, limit: int = 20):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
