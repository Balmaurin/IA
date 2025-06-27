import os
import json
import logging
import hashlib
import time
import base64
from cryptography.fernet import Fernet
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger("sheily_backup")

class SheilyBackupManager:
    """
    Gestor de backups cifrados para SHEILY-light que maneja:
    - Exportación/importación de datos de usuario
    - Cifrado seguro con clave derivada de contraseña
    - Integración con el módulo de tokens y autenticación
    """
    
    def __init__(self, vault_dir: str = None):
        if not vault_dir:
            self.vault_dir = os.path.join(os.path.expanduser("~"), ".sheily", "vault")
        else:
            self.vault_dir = vault_dir
            
        self.backup_dir = os.path.join(self.vault_dir, "backups")
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self) -> None:
        """Asegura que el directorio de backups exista"""
        try:
            Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
            logger.info(f"Backup directory ensured at {self.backup_dir}")
        except Exception as e:
            logger.error(f"Failed to create backup directory: {str(e)}")
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Deriva una clave criptográfica segura de la contraseña"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # Número de iteraciones
            dklen=32  # Longitud de la clave
        )
    
    def encrypt_data(self, data: Dict[str, Any], password: str) -> Optional[bytes]:
        """Cifra los datos del backup usando una clave derivada de la contraseña"""
        try:
            # Generar salt aleatorio
            salt = os.urandom(16)
            
            # Derivar clave
            key = self._derive_key(password, salt)
            fernet = Fernet(base64.urlsafe_b64encode(key))
            
            # Serializar y cifrar datos
            json_data = json.dumps(data).encode('utf-8')
            encrypted_data = fernet.encrypt(json_data)
            
            # Combinar salt + datos cifrados
            return salt + encrypted_data
        except Exception as e:
            logger.error(f"Failed to encrypt backup data: {str(e)}")
            return None
    
    def decrypt_data(self, encrypted_data: bytes, password: str) -> Optional[Dict[str, Any]]:
        """Descifra los datos del backup usando la contraseña"""
        try:
            # Extraer salt (primeros 16 bytes)
            salt = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # Derivar clave
            key = self._derive_key(password, salt)
            fernet = Fernet(base64.urlsafe_b64encode(key))
            
            # Descifrar y deserializar
            json_data = fernet.decrypt(ciphertext)
            return json.loads(json_data.decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to decrypt backup data: {str(e)}")
            return None
    
    def create_backup(self, user_data: Dict[str, Any], password: str) -> Optional[str]:
        """
        Crea un backup cifrado de los datos del usuario
        
        Args:
            user_data: Diccionario con datos del usuario (tokens, config, etc)
            password: Contraseña para cifrar el backup
            
        Returns:
            str: Ruta al archivo de backup creado, o None si falla
        """
        try:
            # Cifrar datos
            encrypted_data = self.encrypt_data(user_data, password)
            if not encrypted_data:
                return None
                
            # Crear nombre de archivo único
            timestamp = int(time.time())
            backup_file = os.path.join(self.backup_dir, f"sheily_backup_{timestamp}.enc")
            
            # Guardar backup cifrado
            with open(backup_file, 'wb') as f:
                f.write(encrypted_data)
                
            logger.info(f"Backup created successfully at {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            return None
    
    def restore_backup(self, backup_path: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Restaura un backup cifrado
        
        Args:
            backup_path: Ruta al archivo de backup
            password: Contraseña usada para cifrar el backup
            
        Returns:
            Dict: Datos del usuario restaurados, o None si falla
        """
        try:
            # Leer backup cifrado
            with open(backup_path, 'rb') as f:
                encrypted_data = f.read()
                
            # Descifrar datos
            return self.decrypt_data(encrypted_data, password)
        except Exception as e:
            logger.error(f"Failed to restore backup: {str(e)}")
            return None
    
    def list_backups(self) -> List[Dict[str, str]]:
        """Lista todos los backups disponibles"""
        backups = []
        try:
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.enc'):
                    filepath = os.path.join(self.backup_dir, filename)
                    stats = os.stat(filepath)
                    backups.append({
                        'filename': filename,
                        'path': filepath,
                        'size': stats.st_size,
                        'created': stats.st_ctime
                    })
        except Exception as e:
            logger.error(f"Failed to list backups: {str(e)}")
            
        return sorted(backups, key=lambda x: x['created'], reverse=True)

# Instancia global del gestor de backups
backup_manager = SheilyBackupManager()
