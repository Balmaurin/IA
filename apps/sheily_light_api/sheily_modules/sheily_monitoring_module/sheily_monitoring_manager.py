import psutil
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import os


@dataclass
class SystemMetrics:
    """Métricas del sistema"""

    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    process_count: int
    uptime: str
    timestamp: str


class SheilyMonitoringManager:
    """
    Gestor de monitorización para el nodo SHEILY-light.
    Supervisa recursos del sistema, estado de módulos y métricas de rendimiento.
    """

    def __init__(self):
        self.logger = logging.getLogger("sheily_monitoring")
        self.metrics_history: List[SystemMetrics] = []
        self.max_history_size = 1000
        self.monitoring_interval = 30  # segundos
        self.is_monitoring = False
        self.monitoring_task = None
        self.alert_thresholds = {"cpu_percent": 80.0, "memory_percent": 85.0, "disk_percent": 90.0}
        self.startup_time = datetime.now()

    async def start(self):
        """Inicia el servicio de monitorización"""
        self.logger.info("Starting monitoring service...")
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())

    async def stop(self):
        """Detiene el servicio de monitorización"""
        self.logger.info("Stopping monitoring service...")
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass

    async def _monitoring_loop(self):
        """Bucle principal de monitorización"""
        while self.is_monitoring:
            try:
                metrics = await self._collect_system_metrics()
                self._store_metrics(metrics)
                await self._check_alerts(metrics)
                await asyncio.sleep(self.monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(5)

    async def _collect_system_metrics(self) -> SystemMetrics:
        """Recopila métricas del sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memoria
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disco
            disk = psutil.disk_usage("/")
            disk_percent = (disk.used / disk.total) * 100

            # Red
            network_io = psutil.net_io_counters()._asdict()

            # Procesos
            process_count = len(psutil.pids())

            # Uptime
            uptime = str(datetime.now() - self.startup_time)

            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                process_count=process_count,
                uptime=uptime,
                timestamp=datetime.now().isoformat(),
            )

        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {str(e)}")
            raise

    def _store_metrics(self, metrics: SystemMetrics):
        """Almacena métricas en el historial"""
        self.metrics_history.append(metrics)

        # Mantener solo las últimas N métricas
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size :]

    async def _check_alerts(self, metrics: SystemMetrics):
        """Verifica alertas basadas en umbrales"""
        alerts = []

        if metrics.cpu_percent > self.alert_thresholds["cpu_percent"]:
            alerts.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")

        if metrics.memory_percent > self.alert_thresholds["memory_percent"]:
            alerts.append(f"High memory usage: {metrics.memory_percent:.1f}%")

        if metrics.disk_percent > self.alert_thresholds["disk_percent"]:
            alerts.append(f"High disk usage: {metrics.disk_percent:.1f}%")

        for alert in alerts:
            self.logger.warning(f"ALERT: {alert}")

    def get_current_metrics(self) -> Dict[str, Any]:
        """Obtiene las métricas actuales del sistema"""
        try:
            # Obtener métricas en tiempo real
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                    "count_physical": psutil.cpu_count(logical=False),
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "free": memory.free,
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100,
                },
                "network": psutil.net_io_counters()._asdict(),
                "processes": len(psutil.pids()),
                "uptime": str(datetime.now() - self.startup_time),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error getting current metrics: {str(e)}")
            return {"error": str(e)}

    def get_metrics_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene el historial de métricas"""
        history = self.metrics_history
        if limit:
            history = history[-limit:]

        return [
            {
                "cpu_percent": m.cpu_percent,
                "memory_percent": m.memory_percent,
                "disk_percent": m.disk_percent,
                "network_io": m.network_io,
                "process_count": m.process_count,
                "uptime": m.uptime,
                "timestamp": m.timestamp,
            }
            for m in history
        ]

    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información completa del sistema"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())

            return {
                "platform": {
                    "system": psutil.LINUX if hasattr(psutil, "LINUX") else "unknown",
                    "node": os.uname().nodename,
                    "release": os.uname().release,
                    "version": os.uname().version,
                    "machine": os.uname().machine,
                    "processor": os.uname().machine,
                },
                "boot_time": boot_time.isoformat(),
                "users": [u._asdict() for u in psutil.users()],
                "cpu_info": {
                    "physical_cores": psutil.cpu_count(logical=False),
                    "total_cores": psutil.cpu_count(logical=True),
                    "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown",
                    "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown",
                },
                "memory_info": {"total": psutil.virtual_memory().total, "swap_total": psutil.swap_memory().total},
            }

        except Exception as e:
            self.logger.error(f"Error getting system info: {str(e)}")
            return {"error": str(e)}

    def get_process_info(self, pid: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene información de procesos"""
        try:
            if pid:
                # Información de un proceso específico
                process = psutil.Process(pid)
                return {
                    "pid": process.pid,
                    "name": process.name(),
                    "status": process.status(),
                    "cpu_percent": process.cpu_percent(),
                    "memory_percent": process.memory_percent(),
                    "memory_info": process.memory_info()._asdict(),
                    "create_time": datetime.fromtimestamp(process.create_time()).isoformat(),
                    "cmdline": process.cmdline(),
                }
            else:
                # Información de todos los procesos
                processes = []
                for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                    try:
                        processes.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                return {
                    "total_processes": len(processes),
                    "processes": sorted(processes, key=lambda x: x.get("cpu_percent", 0), reverse=True)[:10],
                }

        except Exception as e:
            self.logger.error(f"Error getting process info: {str(e)}")
            return {"error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de salud del servicio de monitorización"""
        return {
            "healthy": self.is_monitoring,
            "monitoring_active": self.is_monitoring,
            "metrics_count": len(self.metrics_history),
            "uptime": str(datetime.now() - self.startup_time),
            "last_collection": self.metrics_history[-1].timestamp if self.metrics_history else None,
        }

    def get_status_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del estado del sistema"""
        current_metrics = self.get_current_metrics()

        # Determinar estado general
        status = "healthy"
        issues = []

        if current_metrics.get("cpu", {}).get("percent", 0) > self.alert_thresholds["cpu_percent"]:
            status = "warning"
            issues.append("High CPU usage")

        if current_metrics.get("memory", {}).get("percent", 0) > self.alert_thresholds["memory_percent"]:
            status = "warning"
            issues.append("High memory usage")

        if current_metrics.get("disk", {}).get("percent", 0) > self.alert_thresholds["disk_percent"]:
            status = "critical"
            issues.append("High disk usage")

        return {
            "status": status,
            "issues": issues,
            "summary": {
                "cpu_percent": current_metrics.get("cpu", {}).get("percent", 0),
                "memory_percent": current_metrics.get("memory", {}).get("percent", 0),
                "disk_percent": current_metrics.get("disk", {}).get("percent", 0),
                "processes": current_metrics.get("processes", 0),
                "uptime": current_metrics.get("uptime", "Unknown"),
            },
            "timestamp": datetime.now().isoformat(),
        }

    def export_metrics(self, filepath: str, days: int = 7):
        """Exporta métricas a archivo JSON"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            filtered_metrics = [m for m in self.metrics_history if datetime.fromisoformat(m.timestamp) > cutoff_date]

            export_data = {
                "export_date": datetime.now().isoformat(),
                "days_exported": days,
                "metrics_count": len(filtered_metrics),
                "metrics": self.get_metrics_history(),
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2)

            self.logger.info(f"Metrics exported to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return False


# Instancia global del gestor de monitorización
monitoring_manager = SheilyMonitoringManager()
