"""Utilities for detecting when a prompt needs fresh web data and retrieving it via SerpAPI."""

from __future__ import annotations

import os
import re
from typing import List

import requests

_SERPAPI_KEY = os.getenv("SERPAPI_KEY")
_SERP_ENDPOINT = "https://serpapi.com/search"

# Very simple Spanish keywords indicating current/updated data
_NEEDS_SEARCH_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r"\b(hoy|ahora|últim[ao]s?|actual|reciente|precio|cuánto vale|quién ganó)\b", re.I),
]


def needs_search(prompt: str) -> bool:
    """Return True if the prompt likely requires up-to-date external data."""
    return any(p.search(prompt) for p in _NEEDS_SEARCH_PATTERNS)


def google_search(query: str, num: int = 5) -> str:
    """Return a plain-text summary of top search results using SerpAPI.

    If SERPAPI_KEY is not set or the request fails, returns empty string.
    """
    if not _SERPAPI_KEY:
        return ""

    params = {
        "engine": "google",
        "q": query,
        "api_key": _SERPAPI_KEY,
        "hl": "es",
        "num": num,
    }

    try:
        r = requests.get(_SERP_ENDPOINT, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        results = data.get("organic_results", [])
    except Exception:
        return ""

    lines: List[str] = []
    for idx, item in enumerate(results[:num], 1):
        title = item.get("title", "")
        link = item.get("link", "")
        lines.append(f"{idx}. {title} – {link}")
    return "\n".join(lines)
