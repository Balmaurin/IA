"""Pruebas unitarias para el módulo de chat."""
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Importar la aplicación FastAPI
from run_simple import app

# Cliente de prueba
client = TestClient(app)

def test_chat_endpoint_success():
    """Prueba el endpoint de chat con una respuesta exitosa."""
    # Datos de prueba
    test_data = {
        "messages": [
            {"role": "user", "content": "Hola, ¿cómo estás?"}
        ],
        "model": "llama3",
        "temperature": 0.7
    }
    
    # Respuesta simulada de Ollama
    mock_response = {
        "message": {"content": "¡Hola! Estoy bien, ¿y tú?"},
        "model": "llama3"
    }
    
    # Mock para la petición HTTP a Ollama
    with patch('requests.post') as mock_post:
        # Configurar el mock
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json.return_value = mock_response
        mock_post.return_value = mock_response_obj
        
        # Realizar la petición
        response = client.post(
            "/api/chat/chat/",
            json=test_data
        )
    
    # Verificar la respuesta
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["model"] == "llama3"

def test_chat_endpoint_invalid_data():
    """Prueba el endpoint de chat con datos inválidos."""
    # Datos de prueba inválidos (falta el campo 'messages')
    test_data = {
        "model": "llama3",
        "temperature": 0.7
    }
    
    # Realizar la petición
    response = client.post(
        "/api/chat/chat/",
        json=test_data
    )
    
    # Verificar que devuelve un error 422 (validación fallida)
    assert response.status_code == 422

# Para ejecutar las pruebas:
# pytest sheily_tests/unit/test_chat.py -v
