from typing import List, Optional
from sheily_modules.sheily_model_inference.ollama_client import OllamaClient


def check_ollama_health() -> bool:
    """Verifica si el servicio de Ollama está disponible.

    Returns:
        bool: True si el servicio está disponible, False en caso contrario.
    """
    try:
        with OllamaClient() as client:
            # Intenta obtener los tags para verificar la conexión
            client._client.get("/api/tags")
            return True
    except Exception as e:
        print(f"Error verificando salud de Ollama: {e}")
        return False


def list_available_models() -> List[str]:
    """Obtiene la lista de modelos disponibles en Ollama.

    Returns:
        List[str]: Lista de nombres de modelos disponibles.
    """
    try:
        with OllamaClient() as client:
            response = client._client.get("/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        print(f"Error listando modelos de Ollama: {e}")
        return []
