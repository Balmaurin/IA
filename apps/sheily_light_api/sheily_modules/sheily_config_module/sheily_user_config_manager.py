import os
import yaml
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("sheily_config")


class SheilyUserConfigManager:
    """
    Gestor de configuración de usuario para SHEILY-light que maneja
    preferencias, opciones y configuraciones personalizadas.
    """

    def __init__(self, config_dir: str = None):
        if not config_dir:
            self.config_dir = os.path.join(os.path.expanduser("~"), ".sheily", "config")
        else:
            self.config_dir = config_dir

        self.config_file = os.path.join(self.config_dir, "user_config.yaml")
        self.default_config = {
            "ai": {"model": "llama3", "temperature": 0.7, "context_window": 4096, "max_tokens": 1024},
            "backup": {"auto_backup": True, "backup_frequency_days": 7, "encrypt_backups": True},
            "ui": {"theme": "light", "language": "es", "font_size": "medium", "notifications_enabled": True},
            "privacy": {"telemetry_enabled": False, "share_usage_data": False, "federated_learning": False},
            "network": {"auto_sync": True, "sync_frequency_hours": 24, "use_central_fallback": True},
            "updates": {"auto_update": True, "update_channel": "stable", "check_frequency_days": 1},
        }
        self.config = self.default_config.copy()
        self.ensure_config_dir()
        self.load_config()

    def ensure_config_dir(self) -> None:
        """Asegura que el directorio de configuración exista"""
        try:
            Path(self.config_dir).mkdir(parents=True, exist_ok=True)
            logger.info(f"Config directory ensured at {self.config_dir}")
        except Exception as e:
            logger.error(f"Failed to create config directory: {str(e)}")

    def load_config(self) -> bool:
        """Carga la configuración del archivo. Si no existe, usa los valores predeterminados."""
        if not os.path.exists(self.config_file):
            logger.info(f"No config file found at {self.config_file}, using defaults")
            self.save_config()  # Guardar configuración predeterminada
            return True

        try:
            with open(self.config_file, "r") as f:
                user_config = yaml.safe_load(f)

            # Merge with defaults (to ensure all keys exist)
            if user_config:
                self._deep_update(self.config, user_config)

            logger.info("User configuration loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            return False

    def save_config(self) -> bool:
        """Guarda la configuración actual en el archivo"""
        try:
            with open(self.config_file, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)
            logger.info("User configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            return False

    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene la configuración completa o una sección específica

        Args:
            section: Nombre de la sección a obtener (None para toda la config)

        Returns:
            Dict: La configuración solicitada
        """
        if section:
            return self.config.get(section, {})
        return self.config

    def update_config(self, updates: Dict[str, Any], section: Optional[str] = None) -> bool:
        """
        Actualiza la configuración con nuevos valores

        Args:
            updates: Diccionario con actualizaciones
            section: Sección a actualizar (None para actualizar en la raíz)

        Returns:
            bool: True si la actualización fue exitosa
        """
        try:
            if section:
                if section not in self.config:
                    self.config[section] = {}
                self._deep_update(self.config[section], updates)
            else:
                self._deep_update(self.config, updates)

            self.save_config()
            return True
        except Exception as e:
            logger.error(f"Failed to update configuration: {str(e)}")
            return False

    def reset_to_defaults(self, section: Optional[str] = None) -> bool:
        """
        Restablece la configuración a sus valores predeterminados

        Args:
            section: Sección a restablecer (None para toda la config)

        Returns:
            bool: True si se restableció correctamente
        """
        try:
            if section:
                if section in self.default_config:
                    self.config[section] = self.default_config[section].copy()
            else:
                self.config = self.default_config.copy()

            self.save_config()
            return True
        except Exception as e:
            logger.error(f"Failed to reset configuration: {str(e)}")
            return False

    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Actualización profunda de diccionarios anidados"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def export_config(self, export_path: str) -> bool:
        """Exporta la configuración a un archivo en la ruta especificada"""
        try:
            with open(export_path, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            logger.error(f"Failed to export configuration: {str(e)}")
            return False

    def import_config(self, import_path: str) -> bool:
        """Importa configuración desde un archivo"""
        try:
            with open(import_path, "r") as f:
                imported_config = yaml.safe_load(f)

            if imported_config:
                # Reset to defaults first
                self.config = self.default_config.copy()
                # Then apply imported settings
                self._deep_update(self.config, imported_config)
                self.save_config()

            return True
        except Exception as e:
            logger.error(f"Failed to import configuration: {str(e)}")
            return False


# Instancia global del gestor de configuración
config_manager = SheilyUserConfigManager()

# Helper functions for routers expecting module-level access


def get_config(section: str | None = None):
    """Return config or section via global manager."""
    return config_manager.get_config(section)


def update_config(updates: dict, section: str | None = None):
    """Update config via global manager and return success bool."""
    success = config_manager.update_config(updates, section)
    return {"success": success}
