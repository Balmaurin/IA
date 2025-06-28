#!/bin/bash
set -e

echo "Configurando replicación..."

# Crear usuario de replicación
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${REPLICATION_USER:-repl_user} WITH REPLICATION ENCRYPTED PASSWORD '${REPLICATION_PASSWORD:-repl_password}';
    ALTER SYSTEM SET wal_level = 'replica';
    ALTER SYSTEM SET max_wal_senders = '10';
    ALTER SYSTEM SET max_replication_slots = '10';
    ALTER SYSTEM SET hot_standby = 'on';
    ALTER SYSTEM SET hot_standby_feedback = 'on';
    ALTER SYSTEM SET wal_keep_segments = '64';
    ALTER SYSTEM SET max_wal_senders = '10';
    ALTER SYSTEM SET synchronous_commit = 'local';
    ALTER SYSTEM SET synchronous_standby_names = '*';
EOSQL

echo "Configuración de replicación completada."
