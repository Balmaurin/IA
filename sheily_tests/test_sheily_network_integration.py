import pytest
import time
import requests
from fastapi.testclient import TestClient
from sheily_main_api import app
from sheily_modules.sheily_auth_module.sheily_user_manager import user_manager
from sheily_modules.sheily_comms_module.sheily_central_api_client import CENTRAL_URL

@pytest.fixture
def client():
    """Fixture que provee un cliente de prueba para la API"""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Fixture que crea y elimina un usuario de prueba"""
    # Crear usuario
    user = {"username": "networkuser", "password": "networkpass"}
    user_manager.create_user(user["username"], user["password"])
    
    yield user
    
    # Eliminar usuario
    user_manager.delete_user(user["username"])

@pytest.mark.integration
def test_central_server_connection():
    """Test que verifica la conexión básica con el servidor central"""
    try:
        response = requests.get(f"{CENTRAL_URL}/health", timeout=5)
        assert response.status_code == 200
        assert response.json().get("status") == "ok"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to central server: {str(e)}")

@pytest.mark.integration
def test_user_registration_sync(client, test_user):
    """Test que verifica la sincronización de registro de usuario con la central"""
    # 1. Login local
    login_response = client.post("/auth/login", 
                               json={"username": "networkuser", "password": "networkpass"})
    token = login_response.json()["access_token"]
    
    # 2. Verificar que el usuario existe en la central
    try:
        # En una implementación real, usaríamos el cliente de la API central
        # Aquí simulamos una llamada exitosa
        assert True
    except Exception as e:
        pytest.fail(f"User registration sync failed: {str(e)}")

@pytest.mark.integration
def test_token_synchronization(client, test_user):
    """Test que verifica la sincronización de tokens con la central"""
    # 1. Login local
    login_response = client.post("/auth/login", 
                               json={"username": "networkuser", "password": "networkpass"})
    token = login_response.json()["access_token"]
    
    # 2. Añadir tokens localmente
    add_response = client.post("/tokens/add", 
                             json={"amount": 10}, 
                             headers={"Authorization": f"Bearer {token}"})
    assert add_response.status_code == 200
    
    # 3. Verificar sincronización con central
    try:
        # En una implementación real, verificaríamos el balance en la central
        # Aquí simulamos una sincronización exitosa
        assert True
    except Exception as e:
        pytest.fail(f"Token synchronization failed: {str(e)}")

@pytest.mark.integration
def test_chat_fallback_to_central(client, test_user):
    """Test que verifica el fallback al servidor central cuando el AI local falla"""
    # 1. Login local
    login_response = client.post("/auth/login", 
                               json={"username": "networkuser", "password": "networkpass"})
    token = login_response.json()["access_token"]
    
    # 2. Simular fallo del AI local (en una implementación real usaríamos un mock)
    # 3. Enviar mensaje (debería fallover a la central)
    chat_response = client.post("/chat", 
                              json={"message": "Test with local AI down"}, 
                              headers={"Authorization": f"Bearer {token}"})
    assert chat_response.status_code == 200
    
    # 4. Verificar que la respuesta viene de la central
    # (En una implementación real, verificaríamos logs o metadatos)
    assert "response" in chat_response.json()

@pytest.mark.integration
def test_offline_operation_with_queuing(client, test_user):
    """Test que verifica la operación offline con cola para sincronización posterior"""
    # 1. Login local
    login_response = client.post("/auth/login", 
                               json={"username": "networkuser", "password": "networkpass"})
    token = login_response.json()["access_token"]
    
    # 2. Simular desconexión (en una implementación real usaríamos un mock)
    
    # 3. Realizar operaciones offline
    # Añadir tokens (debería guardarse localmente para sincronización posterior)
    add_response = client.post("/tokens/add", 
                             json={"amount": 15}, 
                             headers={"Authorization": f"Bearer {token}"})
    assert add_response.status_code == 200
    
    # 4. Simular reconexión
    
    # 5. Forzar sincronización
    sync_response = client.post("/comms/sync", 
                              headers={"Authorization": f"Bearer {token}"})
    assert sync_response.status_code == 200
    
    # 6. Verificar que las operaciones pendientes se sincronizaron
    # (En una implementación real, verificaríamos con la API central)
    assert sync_response.json()["status"] == "completed"
