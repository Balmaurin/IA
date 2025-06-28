import pytest
import psutil
from sheily_modules.sheily_monitoring_module.sheily_node_status_monitor import SheilyNodeStatusMonitor


@pytest.fixture
def monitor():
    """Fixture que provee una instancia limpia del monitor"""
    return SheilyNodeStatusMonitor()


def test_system_info(monitor):
    """Test que verifica la obtención de información del sistema"""
    info = monitor.get_system_info()

    assert isinstance(info, dict)
    assert "platform" in info
    assert "architecture" in info
    assert "hostname" in info
    assert isinstance(info["cpu_count"], int)


def test_memory_usage(monitor):
    """Test que verifica la obtención de uso de memoria"""
    memory = monitor.get_memory_usage()

    assert isinstance(memory, dict)
    assert "total" in memory
    assert "available" in memory
    assert "percent" in memory
    assert memory["total"] > 0

    # Verificar que los valores son consistentes
    assert memory["used"] + memory["free"] <= memory["total"]


def test_disk_usage(monitor):
    """Test que verifica la obtención de uso de disco"""
    disk = monitor.get_disk_usage()

    assert isinstance(disk, dict)
    assert "total" in disk
    assert "used" in disk
    assert "free" in disk
    assert disk["total"] > 0

    # Verificar que los valores son consistentes
    assert disk["used"] + disk["free"] == disk["total"]


def test_process_info(monitor):
    """Test que verifica la obtención de información del proceso"""
    process = monitor.get_process_info()

    assert isinstance(process, dict)
    assert "pid" in process
    assert "memory_percent" in process
    assert "cpu_percent" in process
    assert "threads" in process
    assert "create_time" in process
    assert "status" in process

    assert process["pid"] > 0
    assert isinstance(process["threads"], int)


def test_uptime(monitor):
    """Test que verifica el cálculo de tiempo de actividad"""
    uptime = monitor.get_node_uptime()

    assert isinstance(uptime, dict)
    assert "start_time" in uptime
    assert "uptime_seconds" in uptime
    assert "uptime_human" in uptime

    assert uptime["uptime_seconds"] >= 0


def test_complete_status(monitor):
    """Test que verifica el estado completo del nodo"""
    status = monitor.get_complete_status()

    assert isinstance(status, dict)
    assert "timestamp" in status
    assert "system_info" in status
    assert "memory" in status
    assert "disk" in status
    assert "process" in status
    assert "uptime" in status
    assert "network" in status

    # Verificar que el historial se actualiza
    history = monitor.get_status_history()
    assert len(history) == 1
    assert history[0]["timestamp"] == status["timestamp"]


def test_status_summary(monitor):
    """Test que verifica el resumen de estado"""
    summary = monitor.get_status_summary()

    assert isinstance(summary, dict)
    assert "timestamp" in summary
    assert "memory_percent" in summary
    assert "disk_percent" in summary
    assert "cpu_percent" in summary
    assert "uptime_seconds" in summary
    assert "hostname" in summary

    assert 0 <= summary["memory_percent"] <= 100
    assert 0 <= summary["disk_percent"] <= 100
    assert summary["uptime_seconds"] >= 0


def test_status_history(monitor):
    """Test que verifica el historial de estados"""
    # Limpiar historial
    monitor.history = []

    # Generar varios estados
    for _ in range(15):
        monitor.get_complete_status()

    history = monitor.get_status_history()

    # Verificar que no excede el tamaño máximo
    assert len(history) <= monitor.max_history_size

    # Verificar que los datos tienen la estructura correcta
    for entry in history:
        assert "timestamp" in entry
        assert "memory_percent" in entry
        assert "disk_percent" in entry
        assert "cpu_percent" in entry
