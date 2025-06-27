import pytest
import tempfile
import os
import yaml
from sheily_modules.sheily_config_module.sheily_user_config_manager import SheilyUserConfigManager

@pytest.fixture
def config_manager():
    """Fixture que provee una instancia limpia del gestor de configuración"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield SheilyUserConfigManager(temp_dir)

def test_config_initialization(config_manager):
    """Test que verifica la inicialización correcta de la configuración"""
    # Verificar que se cargan los valores por defecto
    assert config_manager.get_config() == config_manager.default_config
    
    # Verificar que se creó el archivo de configuración
    assert os.path.exists(config_manager.config_file)

def test_config_sections(config_manager):
    """Test que verifica el acceso a secciones de configuración"""
    # Obtener sección completa
    ai_config = config_manager.get_config("ai")
    assert "model" in ai_config
    assert "temperature" in ai_config
    
    # Sección inexistente devuelve dict vacío
    assert config_manager.get_config("nonexistent") == {}

def test_config_updates(config_manager):
    """Test que verifica la actualización de la configuración"""
    # Actualizar una sección
    new_ai_config = {"model": "llama2", "temperature": 0.8}
    assert config_manager.update_config(new_ai_config, "ai")
    
    # Verificar cambios
    updated_config = config_manager.get_config("ai")
    assert updated_config["model"] == "llama2"
    assert updated_config["temperature"] == 0.8
    
    # Otros valores deberían permanecer igual
    assert updated_config["context_window"] == config_manager.default_config["ai"]["context_window"]
    
    # Verificar que se guardó en disco
    with open(config_manager.config_file, 'r') as f:
        saved_config = yaml.safe_load(f)
        assert saved_config["ai"]["model"] == "llama2"

def test_config_reset(config_manager):
    """Test que verifica el restablecimiento a valores por defecto"""
    # Hacer cambios
    config_manager.update_config({"model": "custom"}, "ai")
    
    # Resetear solo la sección AI
    assert config_manager.reset_to_defaults("ai")
    assert config_manager.get_config("ai") == config_manager.default_config["ai"]
    
    # Hacer más cambios
    config_manager.update_config({"theme": "dark"}, "ui")
    
    # Resetear toda la configuración
    assert config_manager.reset_to_defaults()
    assert config_manager.get_config() == config_manager.default_config

def test_config_export_import(config_manager):
    """Test que verifica la exportación e importación de configuración"""
    # Hacer cambios
    config_manager.update_config({"model": "export_test"}, "ai")
    
    # Exportar a archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        export_path = temp_file.name
    
    try:
        assert config_manager.export_config(export_path)
        
        # Modificar configuración local
        config_manager.update_config({"model": "should_be_overwritten"}, "ai")
        
        # Importar configuración exportada
        assert config_manager.import_config(export_path)
        
        # Verificar que se restauró el valor exportado
        assert config_manager.get_config("ai")["model"] == "export_test"
    finally:
        os.unlink(export_path)

def test_invalid_config_file(config_manager):
    """Test que verifica el manejo de archivos de configuración inválidos"""
    # Escribir un archivo corrupto
    with open(config_manager.config_file, 'w') as f:
        f.write("invalid: yaml: [")
    
    # Debería cargar los valores por defecto
    assert config_manager.load_config()
    assert config_manager.get_config() == config_manager.default_config
