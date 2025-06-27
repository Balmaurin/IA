import pytest
import time
import os
from fastapi.testclient import TestClient
from sheily_main_api import app
from sheily_modules.sheily_auth_module.sheily_user_manager import user_manager
from sheily_modules.sheily_tokens_module.sheily_token_vault_manager import token_vault
from sheily_modules.sheily_backup_module.sheily_backup_manager import backup_manager
from sheily_modules.sheily_chat_module.sheily_chat_local_engine import chat_engine

@pytest.fixture
def client():
    """Fixture que provee un cliente de prueba para la API"""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Fixture que crea y elimina un usuario de prueba"""
    # Crear usuario
    user = {"username": "endtoenduser", "password": "endtoendpass"}
    user_manager.create_user(user["username"], user["password"])
    
    yield user
    
    # Eliminar usuario
    user_manager.delete_user(user["username"])

def test_chat_conversation_flow(client, test_user):
    """Test que verifica el flujo completo de una conversación con historial"""
    # 1. Login
    login_response = client.post("/auth/login", 
                               json={"username": "endtoenduser", "password": "endtoendpass"})
    token = login_response.json()["access_token"]
    
    # 2. Iniciar conversación
    messages = [
        "Hello, how are you?",
        "What can you do?",
        "Tell me about yourself"
    ]
    
    responses = []
    for message in messages:
        response = client.post("/chat", 
                             json={"message": message}, 
                             headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        responses.append(response.json()["response"])
    
    # 3. Verificar que todas las respuestas son diferentes
    assert len(responses) == 3
    assert responses[0] != responses[1] != responses[2]
    
    # 4. Verificar que se mantiene contexto en la conversación
    # (En una implementación real, verificaríamos referencias cruzadas en las respuestas)

def test_token_earning_flow(client, test_user):
    """Test que verifica el flujo completo de ganar y gastar tokens"""
    # 1. Login
    login_response = client.post("/auth/login", 
                               json={"username": "endtoenduser", "password": "endtoendpass"})
    token = login_response.json()["access_token"]
    
    # 2. Obtener balance inicial
    balance_response = client.get("/tokens/balance", 
                                headers={"Authorization": f"Bearer {token}"})
    initial_balance = balance_response.json()["balance"]
    
    # 3. Realizar actividad que gana tokens (ej. completar tarea)
    task_response = client.post("/tasks/complete", 
                              json={"task_type": "test_task"}, 
                              headers={"Authorization": f"Bearer {token}"})
    assert task_response.status_code == 200
    earned_tokens = task_response.json()["tokens_earned"]
    assert earned_tokens > 0
    
    # 4. Verificar nuevo balance
    balance_response = client.get("/tokens/balance", 
                                headers={"Authorization": f"Bearer {token}"})
    assert balance_response.json()["balance"] == initial_balance + earned_tokens
    
    # 5. Gastar tokens en premium feature
    spend_response = client.post("/tokens/spend", 
                               json={"amount": 5, "reason": "premium_feature"}, 
                               headers={"Authorization": f"Bearer {token}"})
    assert spend_response.status_code == 200
    
    # 6. Verificar balance final
    balance_response = client.get("/tokens/balance", 
                                headers={"Authorization": f"Bearer {token}"})
    assert balance_response.json()["balance"] == initial_balance + earned_tokens - 5

def test_backup_restore_flow_with_chat_history(client, test_user):
    """Test que verifica que el historial de chat se restaura correctamente"""
    # 1. Login
    login_response = client.post("/auth/login", 
                               json={"username": "endtoenduser", "password": "endtoendpass"})
    token = login_response.json()["access_token"]
    
    # 2. Generar historial de chat
    messages = ["Message 1", "Message 2", "Message 3"]
    for msg in messages:
        client.post("/chat", 
                  json={"message": msg}, 
                  headers={"Authorization": f"Bearer {token}"})
    
    # 3. Crear backup
    backup_response = client.post("/auth/backup", 
                                json={"password": "backup_pass"}, 
                                headers={"Authorization": f"Bearer {token}"})
    backup_id = backup_response.json()["backup_id"]
    
    # 4. Simular pérdida de datos
    user_manager.delete_user("endtoenduser")
    assert not chat_engine.get_chat_history("endtoenduser")
    
    # 5. Restaurar backup
    restore_response = client.post("/auth/restore", 
                                 json={"backup_id": backup_id, "password": "backup_pass"})
    assert restore_response.status_code == 200
    
    # 6. Verificar que el historial de chat se restauró
    # Login nuevamente
    login_response = client.post("/auth/login", 
                               json={"username": "endtoenduser", "password": "endtoendpass"})
    token = login_response.json()["access_token"]
    
    # Obtener historial
    history_response = client.get("/chat/history", 
                                headers={"Authorization": f"Bearer {token}"})
    assert history_response.status_code == 200
    history = history_response.json()["history"]
    
    # Verificar que contiene los mensajes anteriores
    assert len(history) >= 3
    assert any(msg["user_message"] == "Message 1" for msg in history)
    assert any(msg["user_message"] == "Message 2" for msg in history)
    assert any(msg["user_message"] == "Message 3" for msg in history)
