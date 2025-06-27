import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger("sheily_recovery")

class SheliySelfRecoveryLogic:
    """
    Lógica de auto-recuperación del nodo SHEILY-light que detecta problemas
    y trata de recuperarse automáticamente sin intervención humana.
    """
    
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.recovery_attempts = {}
        self.max_recovery_attempts = 3
        self.recovery_timeout = 300  # seconds
        
    def register_orchestrator(self, orchestrator):
        """Registra el orquestador para poder reiniciar módulos"""
        self.orchestrator = orchestrator
        
    def check_module_health(self, module_name: str) -> bool:
        """Verifica si un módulo específico está funcionando correctamente"""
        if not self.orchestrator or module_name not in self.orchestrator.modules:
            logger.error(f"Cannot check health for unknown module: {module_name}")
            return False
            
        module = self.orchestrator.modules[module_name]
        
        # Si el módulo tiene un método health_check, lo usamos
        if hasattr(module, 'health_check'):
            try:
                is_healthy = module.health_check()
                return is_healthy
            except Exception as e:
                logger.error(f"Health check for {module_name} failed: {str(e)}")
                return False
        
        # Si no tiene health_check, verificamos si tiene is_running o status
        if hasattr(module, 'is_running'):
            return module.is_running
        elif hasattr(module, 'status'):
            return module.status == 'running'
            
        # Si no podemos verificar, asumimos que está bien
        return True
        
    def attempt_recovery(self, module_name: str) -> bool:
        """Intenta recuperar un módulo problemático"""
        # Verificar si ya intentamos recuperar este módulo demasiadas veces
        now = time.time()
        if module_name in self.recovery_attempts:
            attempts = [t for t in self.recovery_attempts[module_name] 
                       if now - t < self.recovery_timeout]
            
            # Actualizar lista de intentos recientes
            self.recovery_attempts[module_name] = attempts
            
            # Si hay demasiados intentos recientes, no intentamos más
            if len(attempts) >= self.max_recovery_attempts:
                logger.warning(f"Too many recovery attempts for {module_name}, giving up")
                return False
                
        # Registrar este intento
        if module_name not in self.recovery_attempts:
            self.recovery_attempts[module_name] = []
        self.recovery_attempts[module_name].append(now)
        
        logger.info(f"Attempting to recover module {module_name}")
        
        try:
            # Intentar detener el módulo
            if self.orchestrator and module_name in self.orchestrator.modules:
                module = self.orchestrator.modules[module_name]
                
                # Detener el módulo si es posible
                if hasattr(module, 'stop'):
                    module.stop()
                
                # Esperar un momento
                time.sleep(2)
                
                # Reiniciar el módulo
                if hasattr(module, 'start'):
                    module.start()
                    logger.info(f"Successfully recovered module {module_name}")
                    return True
        except Exception as e:
            logger.error(f"Failed to recover module {module_name}: {str(e)}")
            
        return False
        
    def run_recovery_check(self) -> Dict[str, Any]:
        """Ejecuta verificación de salud en todos los módulos y recupera los problemáticos"""
        if not self.orchestrator:
            return {"status": "error", "message": "No orchestrator registered"}
            
        results = {
            "checked": 0,
            "healthy": 0,
            "recovered": 0,
            "failed": 0,
            "details": {}
        }
        
        for module_name in self.orchestrator.modules:
            results["checked"] += 1
            is_healthy = self.check_module_health(module_name)
            
            if is_healthy:
                results["healthy"] += 1
                results["details"][module_name] = "healthy"
            else:
                # Intentar recuperación
                recovery_success = self.attempt_recovery(module_name)
                
                if recovery_success:
                    results["recovered"] += 1
                    results["details"][module_name] = "recovered"
                else:
                    results["failed"] += 1
                    results["details"][module_name] = "failed_recovery"
        
        return results

# Instancia global de la lógica de auto-recuperación
self_recovery = SheliySelfRecoveryLogic()
