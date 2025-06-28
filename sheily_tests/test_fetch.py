"""Test module for the fetch utility endpoint."""

import pytest
from fastapi.testclient import TestClient
from sheily_light_api.sheily_main_api import app

client = TestClient(app)

def test_fetch_endpoint():
    """Test the /utils/fetch endpoint with a sample request."""
    test_url = "https://httpbin.org/get"
    
    # Test GET request
    response = client.post(
        "/utils/fetch",
        json={
            "url": test_url,
            "method": "GET"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "headers" in data
    assert "content" in data
    assert data["content"]["url"] == test_url

@pytest.mark.asyncio
async def test_fetch_domain_restriction():
    """Test that only allowed domains can be accessed."""
    # Test with a non-allowed domain
    response = client.post(
        "/utils/fetch",
        json={
            "url": "https://example.com",
            "method": "GET"
        }
    )
    
    assert response.status_code == 403
    assert "not allowed" in response.json()["detail"]

def test_fetch_with_headers():
    """Test fetch with custom headers."""
    test_url = "https://httpbin.org/headers"
    test_header = {"X-Test-Header": "test-value"}
    
    response = client.post(
        "/utils/fetch",
        json={
            "url": test_url,
            "method": "GET",
            "headers": test_header
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["content"]["headers"]["X-Test-Header"] == "test-value"
