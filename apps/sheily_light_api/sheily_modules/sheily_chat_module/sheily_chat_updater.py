from typing import Dict, Union
from sheily_modules.sheily_model_inference.ollama_client import OllamaClient


def download_model(model_name: str) -> Dict[str, str]:
    """Descarga un modelo de Ollama.

    Args:
        model_name: Nombre del modelo a descargar

    Returns:
        Dict[str, str]: Diccionario con el estado de la operación o un mensaje de error
    """
    try:
        with OllamaClient() as client:
            # Usar el cliente para hacer la solicitud de descarga
            response = client._client.post(
                "/api/pull",
                json={"name": model_name},
                timeout=600
            )
            response.raise_for_status()
            return {"status": "downloaded", "model": model_name}
    except Exception as e:
        error_msg = f"Error al descargar el modelo {model_name}: {str(e)}"
        print(error_msg)  # Para depuración
        return {"error": error_msg}
