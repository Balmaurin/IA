"""Módulo para limitación de tasa de solicitudes."""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
import time
from typing import Dict, Tuple, List
from functools import wraps

# Almacén en memoria para los contadores de solicitudes
request_counts: Dict[str, List[float]] = {}

class RateLimiter:
    """Implementa rate limiting basado en IP."""
    
    def __init__(self, requests: int = 100, window: int = 60):
        """
        Inicializa el rate limiter.
        
        Args:
            requests: Número máximo de peticiones permitidas
            window: Ventana de tiempo en segundos
        """
        self.requests = requests
        self.window = window
    
    async def __call__(self, request: Request):
        """Verifica si se ha excedido el límite de peticiones."""
        client_ip = request.client.host
        current_time = time.time()
        
        # Filtrar solicitudes fuera de la ventana de tiempo
        if client_ip in request_counts:
            request_counts[client_ip] = [
                t for t in request_counts[client_ip] 
                if current_time - t < self.window
            ]
        else:
            request_counts[client_ip] = []
        
        # Verificar límite
        if len(request_counts[client_ip]) >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Too many requests",
                    "retry_after": int(self.window - (current_time - request_counts[client_ip][0]))
                }
            )
        
        # Registrar la solicitud actual
        request_counts[client_ip].append(current_time)
        return True

def rate_limit(requests: int = 100, window: int = 60):
    """Decorador para aplicar rate limiting a endpoints específicos."""
    limiter = RateLimiter(requests, window)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            await limiter(request)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
