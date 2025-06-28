import json
import logging
import datetime
from typing import Dict, Any, List, Optional
import os

logger = logging.getLogger("sheily_audit")


class SheilyLocalAuditTool:
    """
    Herramienta de auditoría local para SHEILY-light que registra eventos
    críticos de seguridad y acciones importantes en formato auditable.
    """

    def __init__(self, audit_file_path: str = "/tmp/sheily_audit.jsonl"):
        self.audit_file_path = audit_file_path
        self.ensure_audit_file_exists()

    def ensure_audit_file_exists(self) -> None:
        """Asegura que el archivo de auditoría exista"""
        if not os.path.exists(self.audit_file_path):
            try:
                with open(self.audit_file_path, "w") as f:
                    f.write("")  # Crear archivo vacío
                logger.info(f"Audit file created at {self.audit_file_path}")
            except Exception as e:
                logger.error(f"Failed to create audit file: {str(e)}")

    def record_event(self, event_type: str, user: str, details: Dict[str, Any], severity: str = "info") -> bool:
        """
        Registra un evento de auditoría

        Args:
            event_type: Categoría del evento (login, token_usage, backup, etc)
            user: Usuario que realizó la acción
            details: Detalles adicionales del evento
            severity: Nivel de severidad (info, warning, critical)

        Returns:
            bool: True si se registró correctamente, False si hubo error
        """
        timestamp = datetime.datetime.now().isoformat()

        audit_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "user": user,
            "severity": severity,
            "details": details,
        }

        try:
            with open(self.audit_file_path, "a") as f:
                f.write(json.dumps(audit_entry) + "\n")

            # Log additional info for critical events
            if severity == "critical":
                logger.warning(f"Critical audit event: {event_type} by {user}")

            return True
        except Exception as e:
            logger.error(f"Failed to record audit event: {str(e)}")
            return False

    def get_audit_events(
        self,
        event_type: Optional[str] = None,
        user: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Recupera eventos de auditoría filtrados

        Args:
            event_type: Filtrar por tipo de evento
            user: Filtrar por usuario
            severity: Filtrar por severidad
            limit: Número máximo de eventos a devolver

        Returns:
            List: Lista de eventos de auditoría que cumplen los criterios
        """
        events = []

        try:
            with open(self.audit_file_path, "r") as f:
                for line in f:
                    if line.strip():
                        try:
                            event = json.loads(line)

                            # Aplicar filtros
                            if event_type and event.get("event_type") != event_type:
                                continue

                            if user and event.get("user") != user:
                                continue

                            if severity and event.get("severity") != severity:
                                continue

                            events.append(event)

                            if len(events) >= limit:
                                break

                        except json.JSONDecodeError:
                            logger.error(f"Corrupt audit entry found: {line}")
                            continue
        except Exception as e:
            logger.error(f"Failed to read audit events: {str(e)}")

        return events

    def export_audit_log(self, output_path: str) -> bool:
        """Exporta el registro de auditoría completo a un archivo"""
        try:
            with open(self.audit_file_path, "r") as src, open(output_path, "w") as dst:
                dst.write(src.read())
            return True
        except Exception as e:
            logger.error(f"Failed to export audit log: {str(e)}")
            return False


# Instancia global de la herramienta de auditoría
audit_tool = SheilyLocalAuditTool()
