"""Utility router providing real-time auxiliary data and HTTP client functionality.

This module provides endpoints for server utilities including time and HTTP fetch capabilities.
"""

import aiohttp
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, HttpUrl

class FetchRequest(BaseModel):
    """Model for fetch request parameters."""
    url: HttpUrl
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    timeout: int = 10

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/time")
async def current_time():
    """Return current server local time as HH:MM:SS string."""
    return {"now": datetime.now().strftime("%H:%M:%S")}


@router.post("/fetch")
async def fetch_url(request: FetchRequest):
    """
    Make an HTTP request to the specified URL and return the response.
    
    This endpoint acts as a proxy for making HTTP requests from the frontend,
    which can help with CORS issues and provides a centralized point for
    request logging and security policies.
    
    Args:
        request: FetchRequest containing URL, method, headers, and body
        
    Returns:
        dict: Response data including status code, headers, and content
    """
    # List of allowed domains for security (can be expanded as needed)
    ALLOWED_DOMAINS = [
        "api.sheily.com",
        "api.openai.com",
        "api.anthropic.com",
        "api.cohere.ai"
    ]
    
    # Extract domain from URL
    domain = str(request.url.host)
    
    # Check if domain is allowed
    if not any(allowed in domain for allowed in ALLOWED_DOMAINS):
        raise HTTPException(
            status_code=403,
            detail=f"Requests to {domain} are not allowed"
        )
    
    # Set default headers if none provided
    headers = request.headers or {}
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'SHEILY-light/1.0'
    
    # Set default timeout
    timeout = aiohttp.ClientTimeout(total=request.timeout)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Make the request
            async with session.request(
                method=request.method,
                url=str(request.url),
                headers=headers,
                json=request.body,
                timeout=timeout
            ) as response:
                # Read response content
                content = await response.text()
                
                # Try to parse as JSON if possible
                try:
                    parsed_content = json.loads(content)
                    content = parsed_content
                except json.JSONDecodeError:
                    pass
                
                # Return response data
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content
                }
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error making request: {str(e)}"
        )
