#!/bin/bash
# Script para respaldar bases de datos PostgreSQL
set -e

# Cargar variables de entorno
if [ -f .env.ha ]; then
    source .env.ha
fi

# Configuración
BACKUP_DIR="/home/yo/CascadeProyects/sheily-light/backups/postgres/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Respaldar cada base de datos
echo "[$(date)] Iniciando respaldo de PostgreSQL..."
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h localhost -U $POSTGRES_USER -F c -b -v -f "$BACKUP_DIR/sheily_db.backup" $POSTGRES_DB

# Comprimir
tar -czf "$BACKUP_DIR.tgz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"
rm -rf "$BACKUP_DIR"

# Rotar respaldos (mantener últimos 7 días)
find /home/yo/CascadeProyects/sheily-light/backups/postgres -name "*.tgz" -mtime +7 -delete

echo "[$(date)] Respaldo completado: $BACKUP_DIR.tgz"
