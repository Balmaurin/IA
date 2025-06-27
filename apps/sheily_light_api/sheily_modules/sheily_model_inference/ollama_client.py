"""Light node Ollama client (same as CORE but default URL is localhost)."""

from __future__ import annotations

import os
from typing import Any, Dict, Generator, Optional

import httpx

__all__ = ["OllamaClient"]


class OllamaClient:
    def __init__(self, base_url: Optional[str] = None, *, timeout: int = 300):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def generate(self, model: str, prompt: str, **params: Any) -> str:
        data = {"model": model, "prompt": prompt, **params}
        resp = self._client.post("/api/generate", json=data)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def embed(self, model: str, prompt: str) -> list[float]:
        data = {"model": model, "prompt": prompt}
        resp = self._client.post("/api/embeddings", json=data)
        resp.raise_for_status()
        return resp.json().get("embedding", [])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()
