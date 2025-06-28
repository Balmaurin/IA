import pytest
from fastapi.testclient import TestClient
from sheily_main_api import app
from sheily_modules.sheily_auth_module.sheily_user_manager import user_manager


@pytest.fixture
def client():
    """Fixture que provee un cliente de prueba para la API"""
    return TestClient(app)


@pytest.fixture
def test_user():
    """Fixture que crea y elimina un usuario de prueba"""
    # Crear usuario
    user = {"username": "testuser", "password": "testpass123"}
    user_manager.create_user(user["username"], user["password"])

    yield user

    # Eliminar usuario
    user_manager.delete_user(user["username"])


def test_health_check(client):
    """Test que verifica el endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_user_registration(client):
    """Test que verifica el registro de usuarios"""
    user_data = {"username": "newuser", "password": "newpass123"}

    # Registrar usuario
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

    # Intentar registrar el mismo usuario (debería fallar)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400


def test_user_login(client, test_user):
    """Test que verifica el login de usuarios"""
    # Login correcto
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Login con contraseña incorrecta
    response = client.post("/auth/login", json={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401

    # Login con usuario inexistente
    response = client.post("/auth/login", json={"username": "nonexistent", "password": "testpass123"})
    assert response.status_code == 401


def test_protected_endpoints(client, test_user):
    """Test que verifica los endpoints protegidos"""
    # Obtener token
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    token = login_response.json()["access_token"]

    # Endpoint protegido con token válido
    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    # Endpoint protegido sin token
    response = client.get("/user/me")
    assert response.status_code == 401

    # Endpoint protegido con token inválido
    response = client.get("/user/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401


def test_chat_endpoint(client, test_user):
    """Test que verifica el endpoint de chat"""
    # Obtener token
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    token = login_response.json()["access_token"]

    # Enviar mensaje
    response = client.post("/chat", json={"message": "Hello"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_token_operations(client, test_user):
    """Test que verifica las operaciones con tokens"""
    # Obtener token
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    token = login_response.json()["access_token"]

    # Obtener balance inicial
    response = client.get("/tokens/balance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    initial_balance = response.json()["balance"]

    # Añadir tokens
    response = client.post("/tokens/add", json={"amount": 10}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Verificar nuevo balance
    response = client.get("/tokens/balance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["balance"] == initial_balance + 10


def test_backup_restore_flow(client, test_user):
    """Test que verifica el flujo completo de backup y restauración"""
    # Obtener token
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    token = login_response.json()["access_token"]

    # Crear backup
    response = client.post(
        "/auth/backup", json={"password": "backuppass"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    backup_data = response.json()
    assert "backup_id" in backup_data

    # Restaurar backup (simulado)
    response = client.post(
        "/auth/restore",
        json={"backup_id": backup_data["backup_id"], "password": "backuppass"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "success"
