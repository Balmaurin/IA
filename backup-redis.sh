#!/bin/bash
# Script para respaldar Redis
set -e

# Cargar variables de entorno
if [ -f .env.ha ]; then
    source .env.ha
fi

# Configuración
BACKUP_DIR="/home/yo/CascadeProyects/sheily-light/backups/redis/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Respaldar Redis
echo "[$(date)] Iniciando respaldo de Redis..."
redis-cli -a "$REDIS_PASSWORD" --rdb "$BACKUP_DIR/dump.rdb"

# Comprimir
tar -czf "$BACKUP_DIR.tgz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"
rm -rf "$BACKUP_DIR"

# Rotar respaldos
find /home/yo/CascadeProyects/sheily-light/backups/redis -name "*.tgz" -mtime +7 -delete

echo "[$(date)] Respaldo de Redis completado: $BACKUP_DIR.tgz"
