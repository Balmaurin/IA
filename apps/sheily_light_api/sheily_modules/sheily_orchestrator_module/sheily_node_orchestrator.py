import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import traceback
from .sheily_orchestrator_status import OrchestrationStatus


class SheilyNodeOrchestrator:
    """
    Orquestador principal del nodo SHEILY-light.
    Gestiona el arranque, parada, monitorización y recuperación de todos los módulos.
    """

    def __init__(self):
        self.modules: Dict[str, Any] = {}
        self.module_status: Dict[str, str] = {}
        self.startup_order: List[str] = []
        self.shutdown_order: List[str] = []
        self.logger = logging.getLogger("sheily_orchestrator")
        self.max_recovery_attempts = 3
        self.recovery_attempts: Dict[str, int] = {}
        self.is_running = False

    def register_module(self, name: str, module: Any, startup_priority: int = 0):
        """Registra un módulo en el orquestador con prioridad de arranque"""
        self.modules[name] = module
        self.module_status[name] = "registered"
        self.recovery_attempts[name] = 0

        # Insertar en orden de prioridad
        self.startup_order.append(name)
        self.startup_order.sort(key=lambda x: getattr(self.modules[x], "startup_priority", 0))

        self.shutdown_order = list(reversed(self.startup_order))
        self.logger.info(f"Registered module: {name} with priority {startup_priority}")

    async def start_all_services(self):
        """Inicia todos los servicios registrados en orden de prioridad"""
        self.logger.info("Starting SHEILY-light node orchestration...")
        self.is_running = True

        for module_name in self.startup_order:
            await self._start_module(module_name)

        self.logger.info("All services started successfully")

    async def _start_module(self, module_name: str):
        """Inicia un módulo específico con manejo de errores"""
        try:
            module = self.modules[module_name]
            self.logger.info(f"Starting module: {module_name}")

            if hasattr(module, "start"):
                await module.start()
            elif hasattr(module, "initialize"):
                await module.initialize()

            self.module_status[module_name] = "running"
            self.recovery_attempts[module_name] = 0
            self.logger.info(f"Module {module_name} started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start module {module_name}: {str(e)}")
            self.logger.debug(traceback.format_exc())
            self.module_status[module_name] = "failed"
            await self._attempt_recovery(module_name)

    async def stop_all_services(self):
        """Detiene todos los servicios en orden inverso"""
        self.logger.info("Stopping SHEILY-light node orchestration...")
        self.is_running = False

        for module_name in self.shutdown_order:
            await self._stop_module(module_name)

        self.logger.info("All services stopped")

    async def _stop_module(self, module_name: str):
        """Detiene un módulo específico"""
        try:
            module = self.modules[module_name]
            self.logger.info(f"Stopping module: {module_name}")

            if hasattr(module, "stop"):
                await module.stop()
            elif hasattr(module, "shutdown"):
                await module.shutdown()

            self.module_status[module_name] = "stopped"
            self.logger.info(f"Module {module_name} stopped successfully")

        except Exception as e:
            self.logger.error(f"Error stopping module {module_name}: {str(e)}")
            self.module_status[module_name] = "error"

    async def restart_module(self, module_name: str):
        """Reinicia un módulo específico"""
        self.logger.info(f"Restarting module: {module_name}")
        await self._stop_module(module_name)
        await asyncio.sleep(1)
        await self._start_module(module_name)

    async def check_modules_health(self):
        """Verifica el estado de salud de todos los módulos"""
        health_report = {}

        for module_name, module in self.modules.items():
            try:
                if hasattr(module, "health_check"):
                    health_status = await module.health_check()
                    health_report[module_name] = health_status

                    if not health_status.get("healthy", True):
                        self.logger.warning(f"Module {module_name} is unhealthy")
                        await self._attempt_recovery(module_name)
                else:
                    # Verificación básica basada en el estado
                    health_report[module_name] = {
                        "healthy": self.module_status[module_name] == "running",
                        "status": self.module_status[module_name],
                    }

            except Exception as e:
                self.logger.error(f"Health check failed for {module_name}: {str(e)}")
                health_report[module_name] = {"healthy": False, "error": str(e)}
                await self._attempt_recovery(module_name)

        return health_report

    async def _attempt_recovery(self, module_name: str):
        """Intenta recuperar un módulo fallido"""
        if self.recovery_attempts[module_name] >= self.max_recovery_attempts:
            self.logger.error(f"Max recovery attempts reached for {module_name}")
            self.module_status[module_name] = "permanently_failed"
            return False

        self.recovery_attempts[module_name] += 1
        self.logger.info(f"Attempting recovery for {module_name} (attempt {self.recovery_attempts[module_name]})")

        try:
            await asyncio.sleep(2 ** self.recovery_attempts[module_name])  # Backoff exponencial
            await self._start_module(module_name)
            return True
        except Exception as e:
            self.logger.error(f"Recovery attempt failed for {module_name}: {str(e)}")
            return False

    def get_modules_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual de todos los módulos"""
        return {
            "orchestrator_running": self.is_running,
            "modules": {
                name: {"status": status, "recovery_attempts": self.recovery_attempts.get(name, 0)}
                for name, status in self.module_status.items()
            },
            "startup_order": self.startup_order,
            "total_modules": len(self.modules),
        }

    async def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información completa del sistema"""
        health_report = await self.check_modules_health()

        return {
            "timestamp": datetime.now().isoformat(),
            "orchestrator_status": "running" if self.is_running else "stopped",
            "modules_status": self.get_modules_status(),
            "health_report": health_report,
            "uptime": self._get_uptime(),
        }

    def _get_uptime(self) -> str:
        """Calcula el tiempo de actividad del orquestador"""
        if hasattr(self, "start_time"):
            uptime = datetime.now() - self.start_time
            return str(uptime)
        return "Unknown"


# Instancia global del orquestador
orchestrator = SheilyNodeOrchestrator()
