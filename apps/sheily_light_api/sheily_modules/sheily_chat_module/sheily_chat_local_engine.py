import re
import os
from typing import Optional
from sheily_modules.sheily_model_inference.ollama_client import OllamaClient

DEFAULT_MODEL = "llama3"
CODE_MODEL = "deepseek-coder:latest"
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "300"))

CODE_KEYWORDS = [
    r"código",
    r"script",
    r"programa",
    r"función",
    r"funciones",
    r"class",
    r"clase",
    r"python",
    r"javascript",
    r"bash",
    r"error",
    r"bug",
    r"traceback",
    r"compilar",
    r"compilador",
    r"ejecutar",
    r"algoritmo",
    r"variable",
    r"constante",
    r"loop",
    r"for",
    r"while",
    r"if",
    r"else",
    r"return",
    r"import",
    r"def",
    r"print",
    r"console",
    r"archivo",
    r"fichero",
    r"archivo.py",
    r"archivo.js",
    r"archivo.sh",
    r"dockerfile",
    r"github",
    r"test",
    r"unittest",
    r"pytest",
    r"assert",
    r"api",
    r"endpoint",
    r"json",
    r"parse",
    r"parsear",
    r"framework",
    r"library",
    r"librería",
    r"package",
    r"paquete",
    r"documentar",
    r"docstring",
    r"documentación",
    r"comentario",
    r"comentarios",
    r"optimizar",
    r"refactor",
    r"lint",
    r"compile",
    r"debug",
    r"debuggear",
    r"automatizar",
    r"automatización",
    r"pipeline",
    r"ci/cd",
    r"deploy",
    r"desplegar",
    r"shell",
    r"cmd",
    r"prompt",
    r"input",
    r"output",
    r"stdin",
    r"stdout",
    r"stderr",
    r"log",
    r"logging",
    r"configuración",
    r"config",
    r"setup",
    r"install",
    r"instalar",
    r"requirements",
    r"version",
    r"versión",
    r"actualizar",
    r"update",
    r"git",
    r"commit",
    r"push",
    r"pull",
    r"branch",
    r"merge",
    r"conflicto",
    r"conflict",
    r"resolver",
    r"resolve",
    r"conda",
    r"virtualenv",
    r"venv",
    r"env",
    r"environment",
    r"entorno",
    r"pip",
    r"poetry",
    r"build",
    r"run",
    r"terminal",
]


def is_code_prompt(prompt: str) -> bool:
    """
    Detecta si el prompt está relacionado con programación/código usando palabras clave.
    """
    for pattern in CODE_KEYWORDS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return True
    return False


def ask_local_ai(prompt: str, model: str = None) -> str:
    """Envía una solicitud al modelo de lenguaje local usando OllamaClient.

    Args:
        prompt: El mensaje del usuario
        model: Nombre del modelo a usar (opcional)

    Returns:
        str: La respuesta del modelo
    """
    if model is None:
        # Selecciona modelo según el tipo de prompt
        model = CODE_MODEL if is_code_prompt(prompt) else DEFAULT_MODEL

    try:
        # Usar el OllamaClient para hacer la solicitud
        with OllamaClient(timeout=OLLAMA_TIMEOUT) as client:
            response = client.generate(
                model=model,
                prompt=prompt,
                stream=False
            )
            return response.strip()

    except Exception as e:
        error_msg = f"Error al consultar Ollama: {str(e)}"
        print(error_msg)  # Para depuración
        raise RuntimeError(error_msg) from e
