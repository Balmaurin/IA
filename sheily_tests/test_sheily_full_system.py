import pytest
import time
import os
from fastapi.testclient import TestClient
from sheily_main_api import app
from sheily_modules.sheily_auth_module.sheily_user_manager import user_manager
from sheily_modules.sheily_tokens_module.sheily_token_vault_manager import token_vault
from sheily_modules.sheily_backup_module.sheily_backup_manager import backup_manager


@pytest.fixture
def client():
    """Fixture que provee un cliente de prueba para la API"""
    return TestClient(app)


@pytest.fixture
def test_user():
    """Fixture que crea y elimina un usuario de prueba"""
    # Crear usuario
    user = {"username": "fullsystemuser", "password": "fullsystempass"}
    user_manager.create_user(user["username"], user["password"])

    yield user

    # Eliminar usuario
    user_manager.delete_user(user["username"])


def test_full_user_flow(client, test_user):
    """Test que verifica el flujo completo de un usuario"""
    # 1. Login
    login_response = client.post("/auth/login", json={"username": "fullsystemuser", "password": "fullsystempass"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 2. Obtener perfil
    profile_response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert profile_response.status_code == 200
    assert profile_response.json()["username"] == "fullsystemuser"

    # 3. Usar chat
    chat_response = client.post("/chat", json={"message": "Test message"}, headers={"Authorization": f"Bearer {token}"})
    assert chat_response.status_code == 200
    assert "response" in chat_response.json()

    # 4. Ganar tokens
    initial_balance = token_vault.get_balance("fullsystemuser")

    add_tokens_response = client.post("/tokens/add", json={"amount": 15}, headers={"Authorization": f"Bearer {token}"})
    assert add_tokens_response.status_code == 200

    new_balance = token_vault.get_balance("fullsystemuser")
    assert new_balance == initial_balance + 15

    # 5. Crear backup
    backup_response = client.post(
        "/auth/backup", json={"password": "backup_password"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert backup_response.status_code == 200
    backup_id = backup_response.json()["backup_id"]

    # Verificar que el backup existe
    backups = backup_manager.list_backups()
    assert any(b["filename"] == backup_id for b in backups)

    # 6. Simular pérdida de nodo (borrar usuario localmente)
    user_manager.delete_user("fullsystemuser")
    assert token_vault.get_balance("fullsystemuser") == 0

    # 7. Restaurar desde backup
    restore_response = client.post("/auth/restore", json={"backup_id": backup_id, "password": "backup_password"})
    assert restore_response.status_code == 200
    assert restore_response.json()["status"] == "success"

    # 8. Verificar que los datos se restauraron
    # Login con credenciales originales
    login_response = client.post("/auth/login", json={"username": "fullsystemuser", "password": "fullsystempass"})
    assert login_response.status_code == 200

    # Verificar tokens
    restored_balance = token_vault.get_balance("fullsystemuser")
    assert restored_balance == new_balance

    # Verificar configuración
    config_response = client.get(
        "/config", headers={"Authorization": f"Bearer {login_response.json()['access_token']}"}
    )
    assert config_response.status_code == 200
    assert "ai" in config_response.json()
    assert "ui" in config_response.json()


def test_offline_operation(client, test_user):
    """Test que verifica operación offline con posterior sincronización"""
    # 1. Login
    login_response = client.post("/auth/login", json={"username": "fullsystemuser", "password": "fullsystempass"})
    token = login_response.json()["access_token"]

    # 2. Simular modo offline (deshabilitar comms)
    # En una implementación real, esto sería un mock del módulo de comunicaciones
    initial_balance = token_vault.get_balance("fullsystemuser")

    # 3. Realizar operaciones offline
    # Añadir tokens offline (no se sincronizaría con la central)
    offline_tokens = 25
    token_vault.add_tokens("fullsystemuser", offline_tokens)

    # Verificar balance local
    assert token_vault.get_balance("fullsystemuser") == initial_balance + offline_tokens

    # 4. Simular reconexión (habilitar comms)
    # En una implementación real, aquí se llamaría al módulo de sincronización

    # 5. Verificar sincronización
    sync_response = client.post("/tokens/sync", headers={"Authorization": f"Bearer {token}"})
    assert sync_response.status_code == 200

    # Verificar que el balance se mantiene
    assert token_vault.get_balance("fullsystemuser") == initial_balance + offline_tokens

    # En una implementación real, aquí verificaríamos que los tokens
    # se reportaron correctamente a SHEILY-central
