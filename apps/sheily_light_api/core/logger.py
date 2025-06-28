"""Módulo de logging centralizado para la aplicación."""
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# Configuración de directorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "sheily.log"

# Crear directorio de logs si no existe
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Configura y retorna un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger (generalmente __name__)
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configurado
    """
    # Obtener el logger
    logger = logging.getLogger(name)
    
    # Evitar múltiples manejadores si el logger ya está configurado
    if logger.handlers:
        return logger
    
    # Nivel de logging
    level = getattr(logging, log_level or os.getenv("LOG_LEVEL", "INFO").upper())
    logger.setLevel(level)
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Manejador para archivo (rotativo)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Manejador para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Añadir manejadores al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger por defecto
logger = setup_logger(__name__)
