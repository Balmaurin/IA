import pytest
import os
import tempfile
from sheily_modules.sheily_backup_module.sheily_backup_manager import SheilyBackupManager
from sheily_modules.sheily_backup_module.sheily_restore_manager import SheilyRestoreManager


@pytest.fixture
def backup_manager():
    """Fixture que provee una instancia limpia del BackupManager"""
    # Usamos un directorio temporal para los tests
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = SheilyBackupManager(temp_dir)
        yield manager


@pytest.fixture
def restore_manager(backup_manager):
    """Fixture que provee una instancia limpia del RestoreManager"""
    return SheilyRestoreManager(backup_manager)


@pytest.fixture
def sample_user_data():
    """Datos de usuario de ejemplo para los tests"""
    return {
        "user": {"username": "test_user", "email": "test@example.com"},
        "tokens": 1500,
        "config": {"theme": "dark", "language": "en"},
    }


def test_backup_creation(backup_manager, sample_user_data):
    """Test que verifica la creación correcta de un backup"""
    password = "secure_password123"
    backup_path = backup_manager.create_backup(sample_user_data, password)

    assert backup_path is not None
    assert os.path.exists(backup_path)
    assert os.path.getsize(backup_path) > 0


def test_backup_restoration(backup_manager, restore_manager, sample_user_data):
    """Test que verifica que un backup puede ser restaurado correctamente"""
    password = "secure_password123"
    backup_path = backup_manager.create_backup(sample_user_data, password)

    # Validar backup
    assert restore_manager.validate_backup(backup_path, password)

    # Restaurar backup
    result = restore_manager.restore_user_account(backup_path, password)
    assert result["status"] == "success"
    assert result["restored_data"] is not None
    assert result["restored_data"]["user"]["username"] == "test_user"
    assert result["restored_data"]["tokens"] == 1500
    assert result["restored_data"]["config"]["theme"] == "dark"


def test_invalid_password(backup_manager, restore_manager, sample_user_data):
    """Test que verifica que no se puede restaurar con contraseña incorrecta"""
    backup_path = backup_manager.create_backup(sample_user_data, "correct_password")

    # Intentar restaurar con contraseña incorrecta
    assert not restore_manager.validate_backup(backup_path, "wrong_password")

    result = restore_manager.restore_user_account(backup_path, "wrong_password")
    assert result["status"] == "error"
    assert "failed" in result["message"].lower()


def test_corrupted_backup(restore_manager):
    """Test que verifica el manejo de backups corruptos"""
    # Crear un archivo que no es un backup válido
    with tempfile.NamedTemporaryFile(suffix=".enc") as temp_file:
        temp_file.write(b"not a valid backup")
        temp_file.flush()

        assert not restore_manager.validate_backup(temp_file.name, "any_password")

        result = restore_manager.restore_user_account(temp_file.name, "any_password")
        assert result["status"] == "error"
        assert "invalid" in result["message"].lower()


def test_backup_listing(backup_manager, sample_user_data):
    """Test que verifica el listado de backups disponibles"""
    # Crear varios backups
    passwords = ["pw1", "pw2", "pw3"]
    backup_paths = []

    for i, pw in enumerate(passwords):
        data = sample_user_data.copy()
        data["user"]["username"] = f"user_{i}"
        path = backup_manager.create_backup(data, pw)
        backup_paths.append(path)

    # Verificar listado
    backups = backup_manager.list_backups()
    assert len(backups) == 3

    # Verificar orden (más reciente primero)
    assert os.path.basename(backups[0]["path"]) == os.path.basename(backup_paths[2])
    assert os.path.basename(backups[1]["path"]) == os.path.basename(backup_paths[1])
    assert os.path.basename(backups[2]["path"]) == os.path.basename(backup_paths[0])
