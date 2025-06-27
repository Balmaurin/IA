# Manual de Usuario SHEILY-light

Bienvenido a SHEILY-light, el nodo local de la plataforma SHEILY AI.

## Características principales
- Autenticación local y sincronización con SHEILY-central
- Almacenamiento seguro de tokens provisionales
- Backup y restauración de usuario y tokens
- Chat robusto con fallback a la central
- Tareas locales de seguridad
- Web moderna y accesible
- Auditoría, logs y auto-actualización

## Instalación
1. Instala Python 3.10+ y Node.js 18+
2. Instala Ollama/Llama 3 localmente (consulta la guía en sheily_docs/sheily_architecture_overview.md)
3. Clona este repositorio y navega a la carpeta `sheily-light`
4. Backend:
   ```bash
   cd apps/sheily_light_api
   pip install -r requirements.txt
   uvicorn sheily_main_api:app --reload
   ```
5. Frontend:
   ```bash
   cd web
   npm install
   npm run dev
   ```
6. Accede a la web local en http://localhost:3000

## Registro y acceso
- Crea tu usuario y contraseña desde la web local.
- Toda la actividad queda asociada a tu identidad y se sincroniza con SHEILY-central.

## Backup y restauración
- Desde el panel de configuración puedes exportar un archivo cifrado con tu cuenta y tokens.
- Si reinstalas el nodo, importa el backup o usa tu usuario/contraseña para restaurar desde la central.

## Sincronización
- El nodo sincroniza automáticamente tus tokens y movimientos con SHEILY-central.
- Puedes forzar la sincronización desde el panel de tokens.

## Seguridad
- Todas las contraseñas y tokens se almacenan cifrados.
- La comunicación con la central es siempre segura (TLS).

## Recuperación ante pérdida
- Si pierdes el nodo pero has sincronizado o tienes backup, puedes restaurar todo.
- Si nunca sincronizaste ni hiciste backup, los datos locales se pierden.

## Contacto y soporte
Consulta la sección de ayuda en la web o el archivo sheily_faq.md para más información.
