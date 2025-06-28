"""Módulo de autenticación y seguridad JWT."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings


# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña

    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera un hash de la contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso.

    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración del token

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def get_credentials_exception():
    """Crea una excepción de credenciales inválidas."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_token(token: str):
    """Verifica y decodifica un token JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        str: Nombre de usuario extraído del token

    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise get_credentials_exception()
        return username
    except JWTError as exc:
        raise get_credentials_exception() from exc


# Mover la dependencia a un valor por defecto de módulo para evitar llamadas a función en la firma
_oauth2_scheme = oauth2_scheme


def get_current_user(token: str = Depends(_oauth2_scheme)):
    """Obtiene el usuario actual a partir del token.

    Args:
        token: Token JWT obtenido del encabezado de autorización

    Returns:
        str: Nombre de usuario extraído del token

    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    return verify_token(token)
