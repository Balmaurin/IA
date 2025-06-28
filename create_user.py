"""Script para crear un usuario en la base de datos SQLite."""
import os
import sys
from datetime import datetime
from passlib.context import CryptContext

# Añadir el directorio raíz al path para que Python pueda encontrar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.sheily_light_api.core.database import SessionLocal, Base, engine
from apps.sheily_light_api.models import User

# Configurar el contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(username: str, password: str):
    """Crea un nuevo usuario en la base de datos."""
    db = SessionLocal()
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"El usuario '{username}' ya existe.")
            return False
        
        # Crear el nuevo usuario
        hashed_password = pwd_context.hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        print(f"Usuario '{username}' creado exitosamente.")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al crear el usuario: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Crear el usuario hugoyvera
    username = "hugoyvera"
    password = "hugoyvera2025"
    
    if create_user(username, password):
        print(f"\nPuedes iniciar sesión con:\nUsuario: {username}\nContraseña: {password}")
    else:
        print("No se pudo crear el usuario. Por favor, verifica los mensajes de error.")
