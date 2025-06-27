import pytest
import json
import tempfile
import os
from sheily_modules.sheily_audit_module.sheily_local_audit_tool import SheilyLocalAuditTool

@pytest.fixture
def audit_tool():
    """Fixture que provee una instancia limpia de la herramienta de auditoría"""
    with tempfile.NamedTemporaryFile(suffix='.jsonl') as temp_file:
        yield SheilyLocalAuditTool(temp_file.name)

def test_audit_event_recording(audit_tool):
    """Test que verifica el registro de eventos de auditoría"""
    # Registrar varios eventos
    assert audit_tool.record_event("login", "user1", {"ip": "192.168.1.1"}, "info")
    assert audit_tool.record_event("token_usage", "user1", {"amount": 10}, "warning")
    assert audit_tool.record_event("failed_login", "user2", {"ip": "192.168.1.2"}, "critical")
    
    # Verificar que se registraron
    events = audit_tool.get_audit_events()
    assert len(events) == 3
    assert events[0]["event_type"] == "login"
    assert events[1]["event_type"] == "token_usage"
    assert events[2]["event_type"] == "failed_login"
    assert events[2]["severity"] == "critical"

def test_audit_event_filtering(audit_tool):
    """Test que verifica el filtrado de eventos de auditoría"""
    # Registrar varios eventos
    audit_tool.record_event("login", "user1", {"ip": "192.168.1.1"}, "info")
    audit_tool.record_event("login", "user2", {"ip": "192.168.1.2"}, "info")
    audit_tool.record_event("token_usage", "user1", {"amount": 10}, "warning")
    audit_tool.record_event("failed_login", "user2", {"ip": "192.168.1.2"}, "critical")
    
    # Filtrar por tipo
    logins = audit_tool.get_audit_events(event_type="login")
    assert len(logins) == 2
    assert all(e["event_type"] == "login" for e in logins)
    
    # Filtrar por usuario
    user1_events = audit_tool.get_audit_events(user="user1")
    assert len(user1_events) == 2
    assert all(e["user"] == "user1" for e in user1_events)
    
    # Filtrar por severidad
    critical_events = audit_tool.get_audit_events(severity="critical")
    assert len(critical_events) == 1
    assert critical_events[0]["event_type"] == "failed_login"
    
    # Combinar filtros
    filtered = audit_tool.get_audit_events(event_type="login", user="user2")
    assert len(filtered) == 1
    assert filtered[0]["user"] == "user2"
    assert filtered[0]["event_type"] == "login"

def test_audit_log_export(audit_tool):
    """Test que verifica la exportación del registro de auditoría"""
    # Registrar algunos eventos
    audit_tool.record_event("login", "user1", {"ip": "192.168.1.1"}, "info")
    audit_tool.record_event("token_usage", "user1", {"amount": 10}, "warning")
    
    # Exportar a un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        export_path = temp_file.name
    
    try:
        assert audit_tool.export_audit_log(export_path)
        
        # Verificar que el archivo exportado contiene los eventos
        with open(export_path, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 2
            assert "login" in lines[0]
            assert "token_usage" in lines[1]
    finally:
        os.unlink(export_path)

def test_corrupt_audit_entries(audit_tool):
    """Test que verifica el manejo de entradas corruptas"""
    # Escribir directamente líneas corruptas
    with open(audit_tool.audit_file_path, 'a') as f:
        f.write("not a valid json\n")
        f.write("{invalid_json\n")
        f.write(json.dumps({"valid": "entry"}) + "\n")
    
    # Debería ignorar las corruptas y devolver las válidas
    events = audit_tool.get_audit_events()
    assert len(events) == 1
    assert events[0]["valid"] == "entry"
