import logging
import time
import psutil
import platform
import socket
import os
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger("sheily_monitoring")


class SheilyNodeStatusMonitor:
    """
    Monitor de estado del nodo SHEILY-light para seguimiento de recursos,
    rendimiento y estado general del sistema.
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = None
        self.history = []
        self.max_history_size = 100
        self.hostname = socket.gethostname()

    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información básica del sistema donde corre el nodo"""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": self.hostname,
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(logical=True),
            "physical_cpu_count": psutil.cpu_count(logical=False),
        }

    def get_memory_usage(self) -> Dict[str, Any]:
        """Obtiene información sobre el uso de memoria"""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
            "free": mem.free,
        }

    def get_disk_usage(self) -> Dict[str, Any]:
        """Obtiene información sobre el uso de disco"""
        disk = psutil.disk_usage("/")
        return {"total": disk.total, "used": disk.used, "free": disk.free, "percent": disk.percent}

    def get_process_info(self) -> Dict[str, Any]:
        """Obtiene información sobre el proceso actual"""
        process = psutil.Process(os.getpid())
        return {
            "pid": process.pid,
            "memory_percent": process.memory_percent(),
            "cpu_percent": process.cpu_percent(interval=0.1),
            "threads": process.num_threads(),
            "create_time": datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "status": process.status(),
        }

    def get_node_uptime(self) -> Dict[str, Any]:
        """Calcula el tiempo de actividad del nodo"""
        uptime = datetime.now() - self.start_time
        return {
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime_seconds": uptime.total_seconds(),
            "uptime_human": str(uptime),
        }

    def get_complete_status(self) -> Dict[str, Any]:
        """Obtiene un estado completo del nodo y sistema"""
        now = datetime.now()

        status = {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": self.get_system_info(),
            "memory": self.get_memory_usage(),
            "disk": self.get_disk_usage(),
            "process": self.get_process_info(),
            "uptime": self.get_node_uptime(),
            "network": {"hostname": self.hostname, "ip_address": socket.gethostbyname(self.hostname)},
        }

        # Actualizar historial
        self.last_check = now
        self.history.append(
            {
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "memory_percent": status["memory"]["percent"],
                "disk_percent": status["disk"]["percent"],
                "cpu_percent": status["process"]["cpu_percent"],
            }
        )

        # Mantener historial dentro del tamaño máximo
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size :]

        return status

    def get_status_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen más ligero del estado del nodo"""
        status = self.get_complete_status()
        return {
            "timestamp": status["timestamp"],
            "memory_percent": status["memory"]["percent"],
            "disk_percent": status["disk"]["percent"],
            "cpu_percent": status["process"]["cpu_percent"],
            "uptime_seconds": status["uptime"]["uptime_seconds"],
            "hostname": status["network"]["hostname"],
        }

    def get_status_history(self) -> List[Dict[str, Any]]:
        """Obtiene el historial de estado"""
        return self.history


# Instancia global del monitor de estado
node_monitor = SheilyNodeStatusMonitor()


def get_node_status(summary: bool = True):
    """Función pública para routers: devuelve estado del nodo."""
    return node_monitor.get_status_summary() if summary else node_monitor.get_complete_status()
