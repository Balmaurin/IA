import pytest
from unittest.mock import MagicMock
from sheily_modules.sheily_orchestrator_module.sheily_node_orchestrator import SheilyNodeOrchestrator
from sheily_modules.sheily_orchestrator_module.sheily_self_recovery_logic import SheliySelfRecoveryLogic


@pytest.fixture
def orchestrator():
    """Fixture que provee una instancia limpia del orquestador"""
    return SheilyNodeOrchestrator()


@pytest.fixture
def recovery_logic():
    """Fixture que provee una instancia limpia de la lógica de recuperación"""
    return SheliySelfRecoveryLogic()


class MockModule:
    """Módulo mock para testing"""

    def __init__(self, name, healthy=True):
        self.name = name
        self.healthy = healthy
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def health_check(self):
        return self.healthy

    def get_status(self):
        return {"status": "running" if self.started else "stopped"}


def test_module_registration(orchestrator):
    """Test que verifica el registro correcto de módulos"""
    mock_module = MockModule("test_module")
    orchestrator.register_module("test", mock_module)

    assert "test" in orchestrator.modules
    assert orchestrator.modules["test"] == mock_module


def test_service_startup_sequence(orchestrator):
    """Test que verifica la secuencia de inicio de servicios"""
    # Registrar módulos mock en el orden correcto
    modules = {
        "config": MockModule("config"),
        "monitoring": MockModule("monitoring"),
        "auth": MockModule("auth"),
        "tokens": MockModule("tokens"),
        "comms": MockModule("comms"),
        "chat": MockModule("chat"),
        "logs": MockModule("logs"),
        "backup": MockModule("backup"),
        "tasks": MockModule("tasks"),
    }

    for name, module in modules.items():
        orchestrator.register_module(name, module)

    # Iniciar todos los servicios
    results = orchestrator.start_all_services()

    # Verificar que todos los módulos se iniciaron
    assert len(results) == len(modules)
    for name in modules:
        assert results[name] == "started"
        assert modules[name].started


def test_service_shutdown_sequence(orchestrator):
    """Test que verifica la secuencia de apagado de servicios"""
    # Registrar módulos mock
    modules = {
        "config": MockModule("config"),
        "monitoring": MockModule("monitoring"),
        "auth": MockModule("auth"),
        "tokens": MockModule("tokens"),
        "comms": MockModule("comms"),
        "chat": MockModule("chat"),
        "logs": MockModule("logs"),
        "backup": MockModule("backup"),
        "tasks": MockModule("tasks"),
    }

    for name, module in modules.items():
        orchestrator.register_module(name, module)
        module.started = True  # Simular que están iniciados

    # Detener todos los servicios
    results = orchestrator.stop_all_services()

    # Verificar que todos los módulos se detuvieron
    assert len(results) == len(modules)
    for name in modules:
        assert results[name] == "stopped"
        assert not modules[name].started


def test_node_status(orchestrator):
    """Test que verifica el reporte de estado del nodo"""
    # Registrar módulos mock
    modules = {"config": MockModule("config"), "monitoring": MockModule("monitoring")}

    for name, module in modules.items():
        orchestrator.register_module(name, module)
        module.started = True

    # Obtener estado
    status = orchestrator.get_node_status()

    # Verificar estructura del estado
    assert "orchestrator_status" in status
    assert status["orchestrator_status"] == "running"

    assert "modules" in status
    assert len(status["modules"]) == len(modules)
    for name in modules:
        assert status["modules"][name]["status"] == "running"


def test_recovery_logic(recovery_logic, orchestrator):
    """Test que verifica la lógica de auto-recuperación"""
    # Configurar
    recovery_logic.register_orchestrator(orchestrator)

    # Registrar módulo mock problemático
    faulty_module = MockModule("faulty", healthy=False)
    orchestrator.register_module("faulty", faulty_module)

    # Verificar que detecta el módulo problemático
    assert not recovery_logic.check_module_health("faulty")

    # Intentar recuperación
    assert recovery_logic.attempt_recovery("faulty")

    # Verificar que se llamó a stop() y start()
    assert faulty_module.started

    # Ejecutar chequeo completo
    results = recovery_logic.run_recovery_check()
    assert results["checked"] == 1
    assert results["recovered"] == 1
    assert results["details"]["faulty"] == "recovered"


def test_too_many_recovery_attempts(recovery_logic, orchestrator):
    """Test que verifica el límite de intentos de recuperación"""
    recovery_logic.register_orchestrator(orchestrator)
    faulty_module = MockModule("faulty", healthy=False)
    orchestrator.register_module("faulty", faulty_module)

    # Simular múltiples intentos fallidos
    recovery_logic.recovery_attempts["faulty"] = [
        time.time() - 10,  # Hace 10 segundos
        time.time() - 5,  # Hace 5 segundos
        time.time() - 1,  # Hace 1 segundo
    ]

    # El cuarto intento debería fallar
    assert not recovery_logic.attempt_recovery("faulty")
