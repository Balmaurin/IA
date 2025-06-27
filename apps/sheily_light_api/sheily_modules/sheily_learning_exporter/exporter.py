"""Batch exporter of training data from SHEILY-light to SHEILY-CORE."""

from __future__ import annotations

import json
import lzma
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests
from sqlalchemy.orm import Session

from ..sheily_chat_module.sheily_chat_service import get_chat_history  # reuse for DB access
from ...dependencies import get_db
from ...models import User, ChatMessage

logger = logging.getLogger("sheily_exporter")

CORE_URL = "http://localhost:8001"  # core ingest endpoint
BATCH_DIR = Path.home() / ".sheily" / "batches"
BATCH_DIR.mkdir(parents=True, exist_ok=True)
MAX_RECORDS = 1000


def _serialize_message(msg: ChatMessage) -> Dict[str, Any]:
    return {
        "user_id": msg.user_id,
        "prompt": msg.prompt,
        "response": msg.response,
        "ts": msg.created_at.isoformat(),
    }


def collect_batch(db: Session, user: User, limit: int = MAX_RECORDS) -> List[Dict[str, Any]]:
    records = get_chat_history(db, user, limit)
    return [_serialize_message(r) for r in records]


def build_payload(records: List[Dict[str, Any]]) -> bytes:
    raw = "\n".join(json.dumps(r, ensure_ascii=False) for r in records).encode()
    compressed = lzma.compress(raw)
    digest = hashlib.sha256(compressed).hexdigest()
    logger.info("Built batch size=%s sha256=%s", len(records), digest)
    return compressed


def send_batch(user: User, data: bytes) -> bool:
    try:
        resp = requests.post(
            f"{CORE_URL}/api/ingest",
            files={"file": ("batch.xz", data)},
            headers={"X-Node-Id": user.username},
            timeout=30,
        )
        resp.raise_for_status()
        logger.info("Batch sent: %s", resp.json())
        return True
    except Exception as exc:
        logger.error("Failed to send batch: %s", exc)
        return False


def export_training_batch(user: User, db: Session):
    records = collect_batch(db, user)
    if not records:
        return {"detail": "no data"}
    payload = build_payload(records)
    ok = send_batch(user, payload)
    return {"sent": ok, "records": len(records)}
