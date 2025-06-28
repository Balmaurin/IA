# Inicio de SHEILY-light

Este documento explica cómo iniciar todos los servicios de SHEILY-light en el orden correcto.

## Requisitos previos

- Docker instalado y en ejecución
- Docker Compose instalado
- Al menos 16GB de RAM recomendados para ejecutar los modelos de IA
- Alrededor de 20GB de espacio en disco para los modelos

## Servicios incluidos

1. **Base de datos PostgreSQL**
   - Puerto: 5432
   - Volumen: `sheily_postgres_data`

2. **Ollama (para modelos de IA)**
   - Puerto: 11434
   - Volumen: `ollama_data`
   - Modelos incluidos:
     - Llama 3 (8B parámetros)
     - Deepseek Coder (6.7B parámetros)

3. **API de SHEILY-light**
   - Puerto: 8000
   - Depende de: Base de datos

4. **Frontend Web**
   - Puerto: 3000
   - Interfaz de usuario de SHEILY-light

## Iniciar todos los servicios

1. Asegúrate de tener permisos de ejecución:
   ```bash
   chmod +x start-all.sh
   ```

2. Ejecuta el script de inicio:
   ```bash
   ./start-all.sh
   ```

## Acceso a los servicios

- **Interfaz web**: http://localhost:3000
- **API REST**: http://localhost:8000
- **Ollama API**: http://localhost:11434
- **Base de datos**: localhost:5432
  - Usuario: sheily
  - Base de datos: sheily

## Notas importantes

- La primera vez que se ejecute, la descarga de los modelos de IA puede tardar varios minutos dependiendo de tu conexión a internet.
- Los modelos se almacenan en un volumen de Docker para no tener que volver a descargarlos en reinicios posteriores.
- Para detener todos los servicios, usa `docker-compose -f docker-compose.prod.yml down`.

## Solución de problemas

- Si algún servicio no inicia correctamente, revisa los logs con:
  ```bash
  docker-compose -f docker-compose.prod.yml logs -f
  ```
- Para reiniciar un servicio específico:
  ```bash
  docker-compose -f docker-compose.prod.yml restart <nombre_servicio>
  ```

## Configuración avanzada

Puedes modificar las variables de entorno en `.env.production` para personalizar la configuración de los servicios.
