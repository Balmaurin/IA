# SHEILY-light – Arquitectura General

## 1. Visión
Nodo local seguro, modular, auditable, restaurable y conectado a SHEILY-central.

## 2. Componentes principales
- **Backend Python (FastAPI):**
  - Autenticación local/remota
  - Gestión de tokens y vault cifrado
  - Backup/restore
  - Chat local (Ollama/Llama 3)
  - Sincronización y fallback con central
  - Tareas, logs, orquestador, auditoría
- **Frontend Next.js/React:**
  - Paneles para chat, tokens, logs, backup, restore, settings, ayuda
  - UX accesible, multi-idioma, modo oscuro
- **Vault local:**
  - SQLite cifrado para tokens y credenciales
- **Comunicación segura:**
  - TLS, autenticación, sincronización periódica
- **Auto-actualización y monitoreo:**
  - Actualizador automático, healthchecks

## 3. Flujos críticos
- Registro/login local → sincronización → backup/export/import → restauración tras reinstalación
- Chat local → fallback central
- Ganancia de tokens → sincronización → canje blockchain en central

## 4. Seguridad
- Hash de contraseñas, cifrado de vault, TLS, logs/auditoría, telemetría opt-in

## 5. Instalación de Ollama/Llama 3
- Descarga desde https://ollama.com/ (Linux/Mac/Win)
- Modelos: llama3, codellama, mistral, etc.
- Configura el modelo por defecto en sheily_light_settings.yaml

## 6. Diagrama de carpetas
Consulta el README.md para la estructura completa.

## 7. Recuperación
- Si el usuario borra el nodo pero sincronizó o hizo backup, puede restaurar todo.
- Si nunca sincronizó ni hizo backup, los datos se pierden localmente.
