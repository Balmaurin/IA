"""Script simplificado para iniciar el servidor FastAPI."""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import requests
import json


# Crear la aplicación FastAPI
app = FastAPI(title="Sheily Light API", version="0.1.0")

# Configuración de CORS
# Obtener orígenes permitidos de variables de entorno o usar valores por defecto para desarrollo
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Agregar aquí otros orígenes permitidos en producción
    # "https://tudominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Length", "X-Foo", "X-Bar"],
    max_age=600,  # Tiempo de caché para las opciones preflight (en segundos)
)


@app.get("/")
async def root():
    """Ruta de prueba para verificar que el servidor está funcionando."""
    return {"message": "¡Bienvenido a Sheily Light!"}



class User(BaseModel):
    """Modelo para los datos de usuario."""
    username: str
    password: str



class Token(BaseModel):
    """Modelo para la respuesta del token."""
    access_token: str
    token_type: str



# Base de datos simulada
fake_users_db = {
    "hugoyvera": {
        "username": "hugoyvera",
        "password": "hugoyvera2025",  # En producción, usa contraseñas hasheadas
    }
}



def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario de la base de datos simulada."""
    return fake_users_db.get(username)


@app.post("/api/auth/login", response_model=Token)
async def login(user_data: User):
    """Endpoint para el inicio de sesión de usuarios."""
    user = get_user(user_data.username)
    
    if not user or user["password"] != user_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": f"token_simulado_para_{user_data.username}",
        "token_type": "bearer"
    }


def get_token_from_header(authorization: str = None) -> Optional[str]:
    """Extrae el token del encabezado de autorización."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    return authorization.split(" ")[1]



@app.get("/api/protected")
async def protected_route(request: Request):
    """Ruta protegida que requiere autenticación."""
    token = get_token_from_header(request.headers.get("Authorization"))

    if not token or not token.startswith("token_simulado_para_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "¡Acceso concedido!"}


class ChatMessage(BaseModel):
    """Modelo para los mensajes del chat."""
    role: str = Field(..., description="El rol del mensaje (usuario, asistente, sistema)")
    content: str = Field(..., description="El contenido del mensaje")


class ChatRequest(BaseModel):
    """Modelo para las solicitudes de chat."""
    messages: List[ChatMessage] = Field(..., description="Lista de mensajes del chat")
    model: str = Field(default="llama3", description="Modelo de IA a utilizar")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Temperatura para la generación")


@app.post("/api/chat/chat/")
async def chat_with_ai(chat_request: ChatRequest):
    """
    Endpoint para interactuar con el modelo de IA local.
    
    Args:
        chat_request (ChatRequest): La solicitud de chat con los mensajes y configuración.
        
    Returns:
        Dict: Respuesta del modelo de IA.
    """
    try:
        # Preparar los mensajes para el modelo
        messages = [{"role": msg.role, "content": msg.content} for msg in chat_request.messages]
        
        # Determinar el modelo a usar
        model = chat_request.model
        
        # Llamar al modelo local a través de Ollama
        ollama_url = "http://localhost:11434/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "options": {
                "temperature": chat_request.temperature
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        
        # Procesar la respuesta
        result = response.json()
        return {
            "response": result.get("message", {}).get("content", ""),
            "model": model,
            "usage": {
                "prompt_tokens": 0,  # Ollama no proporciona estos datos
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error al conectar con el servicio de IA: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )



if __name__ == "__main__":
    uvicorn.run("run_simple:app", host="0.0.0.0", port=8001, reload=True)
