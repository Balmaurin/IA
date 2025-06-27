# SHEILY-light – Referencia de API

## Endpoints principales (FastAPI)

### Autenticación
- `POST /api/auth/register` – Registro de usuario local y sincronización central
- `POST /api/auth/login` – Login local y remoto
- `POST /api/auth/logout` – Logout
- `POST /api/auth/backup` – Exportar backup cifrado
- `POST /api/auth/restore` – Restaurar desde backup o central

### Tokens
- `GET /api/tokens` – Consultar saldo y movimientos
- `POST /api/tokens/add` – Añadir tokens locales
- `POST /api/tokens/sync` – Sincronizar con central
- `POST /api/tokens/backup` – Exportar backup tokens
- `POST /api/tokens/restore` – Restaurar tokens

### Chat
- `POST /api/chat` – Preguntar al motor local, fallback a central si es necesario

### Tareas
- `POST /api/tasks/run` – Ejecutar tareas locales (scan, limpieza, etc)

### Logs y auditoría
- `GET /api/logs` – Consultar logs
- `POST /api/logs/export` – Exportar logs

### Configuración
- `GET /api/config` – Obtener configuración
- `POST /api/config/update` – Actualizar preferencias

### Estado y salud
- `GET /api/status` – Estado del nodo, healthcheck, sincronización

## Seguridad
- Todas las rutas requieren autenticación JWT salvo registro/login
- Comunicación TLS obligatoria

## Ejemplo de uso
Consulta los tests en `sheily_tests/` y el manual para ejemplos de llamadas API.
