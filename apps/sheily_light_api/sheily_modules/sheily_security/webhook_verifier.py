"""Verify reward webhooks signed by SHEILY-CORE.

CORE sends headers:
    X-Sheily-Signature: base64 Ed25519 signature of (timestamp + '.' + body)
    X-Sheily-Timestamp: unix epoch seconds

The node stores CORE public key in env var CORE_SIGNING_PUBLIC_KEY (base64).
"""

from __future__ import annotations

import base64
import json
import os
import time
from typing import Dict

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from fastapi import HTTPException

PUBLIC_KEY_B64 = os.getenv("CORE_SIGNING_PUBLIC_KEY", "")
MAX_SKEW = 300  # 5 minutes


class WebhookVerificationError(HTTPException):
    def __init__(self, detail: str = "invalid signature"):
        super().__init__(status_code=401, detail=detail)


def _public_key() -> Ed25519PublicKey:
    if not PUBLIC_KEY_B64:
        raise RuntimeError("CORE_SIGNING_PUBLIC_KEY env var not set")
    try:
        return Ed25519PublicKey.from_public_bytes(base64.b64decode(PUBLIC_KEY_B64))
    except Exception as exc:
        raise RuntimeError("bad CORE_SIGNING_PUBLIC_KEY") from exc


def verify(headers: Dict[str, str], body: bytes) -> None:
    sig_b64 = headers.get("x-sheily-signature")
    ts = headers.get("x-sheily-timestamp")
    if not sig_b64 or not ts:
        raise WebhookVerificationError("missing signature headers")
    try:
        timestamp = int(ts)
    except ValueError:
        raise WebhookVerificationError("bad timestamp")
    if abs(time.time() - timestamp) > MAX_SKEW:
        raise WebhookVerificationError("timestamp skew too large")

    message = ts.encode() + b"." + body
    signature = base64.b64decode(sig_b64)
    try:
        _public_key().verify(signature, message)
    except Exception:
        raise WebhookVerificationError()
