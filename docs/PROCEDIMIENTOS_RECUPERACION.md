# Procedimientos de Recuperación ante Desastres

## Tabla de Contenidos
1. [Restauración de Base de Datos PostgreSQL](#1-restauración-de-base-de-datos-postgresql)
   - [1.1 Restaurar desde un respaldo](#11-restaurar-desde-un-respaldo)
   - [1.2 Restaurar un nodo réplica](#12-restaurar-un-nodo-réplica)
2. [Recuperación de Redis](#2-recuperación-de-redis)
   - [2.1 Restaurar desde respaldo](#21-restaurar-desde-respaldo)
3. [Recuperación de Datos de la Aplicación](#3-recuperación-de-datos-de-la-aplicación)
   - [3.1 Restaurar volúmenes](#31-restaurar-volúmenes)
4. [Procedimiento de Failover](#4-procedimiento-de-failover)
   - [4.1 Failover de PostgreSQL](#41-failover-de-postgresql)
5. [Verificación Post-Recuperación](#5-verificación-post-recuperación)
6. [Contactos de Emergencia](#6-contactos-de-emergencia)

## 1. Restauración de Base de Datos PostgreSQL

### 1.1 Restaurar desde un respaldo

```bash
# Conectarse al servidor de base de datos
ssh usuario@servidor-bd

# Detener la aplicación si es necesario
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml stop app

# Identificar el archivo de respaldo más reciente
LATEST_BACKUP=$(ls -t /home/yo/CascadeProyects/sheily-light/backups/postgres/*.tgz | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No se encontraron respaldos"
    exit 1
fi

echo "Restaurando desde: $LATEST_BACKUP"

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)

# Extraer el respaldo
tar -xzf "$LATEST_BACKUP" -C "$TEMP_DIR" --strip-components=1

# Restaurar la base de datos
DB_CONTAINER=$(docker ps -q -f name=sheily-db)

if [ -z "$DB_CONTAINER" ]; then
    echo "No se encontró el contenedor de la base de datos"
    exit 1
fi

docker cp "$TEMP_DIR/sheily_db.backup" "$DB_CONTAINER:/tmp/backup_file"
docker exec -e PGPASSWORD=$POSTGRES_PASSWORD $DB_CONTAINER \
  pg_restore -U $POSTGRES_USER -d $POSTGRES_DB -c -v "/tmp/backup_file"

# Limpiar
rm -rf "$TEMP_DIR"

# Reiniciar la aplicación si se detuvo
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml start app

echo "Restauración completada exitosamente"
```

### 1.2 Restaurar un nodo réplica

```bash
# Conectarse al nodo réplica
ssh usuario@nodo-replica

# Detener el servicio de réplica
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml stop postgres-replica

# Eliminar directorio de datos (cuidado con este paso)
sudo rm -rf /ruta/a/postgres_replica_data/*

# Reiniciar el servicio de réplica
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml up -d postgres-replica

# Verificar estado de replicación
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml exec postgres-master \
  psql -U $POSTGRES_USER -c "SELECT * FROM pg_stat_replication;"

echo "Réplica reiniciada y sincronizando..."
```

## 2. Recuperación de Redis

### 2.1 Restaurar desde respaldo

```bash
# Conectarse al servidor de Redis
ssh usuario@servidor-redis

# Detener Redis
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml stop redis

# Identificar el archivo de respaldo más reciente
LATEST_BACKUP=$(ls -t /home/yo/CascadeProyects/sheily-light/backups/redis/*.tgz | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No se encontraron respaldos de Redis"
    exit 1
fi

echo "Restaurando Redis desde: $LATEST_BACKUP"

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)

# Extraer el respaldo
tar -xzf "$LATEST_BACKUP" -C "$TEMP_DIR" --strip-components=1

# Mover archivo de respaldo
REDIS_DATA_DIR="/ruta/a/redis_data"
sudo cp "$TEMP_DIR/dump.rdb" "$REDIS_DATA_DIR/"
sudo chown -R 1000:1000 "$REDIS_DATA_DIR"

# Iniciar Redis
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml up -d redis

# Verificar datos
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml exec redis \
  redis-cli -a $REDIS_PASSWORD DBSIZE

# Limpiar
rm -rf "$TEMP_DIR"

echo "Restauración de Redis completada"
```

## 3. Recuperación de Datos de la Aplicación

### 3.1 Restaurar volúmenes

```bash
# Conectarse al servidor de aplicaciones
ssh usuario@servidor-app

# Detener la aplicación
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml down

# Identificar el archivo de respaldo más reciente
LATEST_BACKUP=$(ls -t /backups/volumes/volumes_*.tgz | sort -r | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No se encontraron respaldos de volúmenes"
    exit 1
fi

echo "Restaurando volúmenes desde: $LATEST_BACKUP"

# Restaurar volúmenes
sudo tar -xzf "$LATEST_BACKUP" -C /

# Verificar permisos
VOLUME_DIRS=(
    "/ruta/a/volumenes/postgres"
    "/ruta/a/volumenes/redis"
    "/ruta/a/volumenes/archivos"
)

for dir in "${VOLUME_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        sudo chown -R 1000:1000 "$dir"
        echo "Permisos actualizados para $dir"
    fi
done

# Iniciar la aplicación
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml up -d

echo "Restauración de volúmenes completada"
```

## 4. Procedimiento de Failover

### 4.1 Failover de PostgreSQL

```bash
# Conectarse al nodo réplica que se convertirá en maestro
ssh usuario@nodo-replica

# Promover la réplica a maestro
docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml exec postgres-replica \
  pg_ctl promote -D /var/lib/postgresql/data

# Actualizar configuración de PgPool en todos los nodos
for NODO in nodo1 nodo2 nodo3; do
    ssh usuario@$NODO "
        echo 'backend_hostname0 = \"postgres-replica\"' > /ruta/a/pgpool/conf/backend_conninfo.conf && \
        docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml kill -s HUP pgpool
    "
done

echo "Failover completado. La réplica ahora es el maestro principal."
```

## 5. Verificación Post-Recuperación

Después de cualquier procedimiento de recuperación, realice las siguientes verificaciones:

1. **Verificar servicios en ejecución**:
   ```bash
   docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml ps
   ```

2. **Revisar logs en busca de errores**:
   ```bash
   docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml logs --tail=100
   ```

3. **Probar funcionalidades críticas**:
   - Acceso a la aplicación web
   - Autenticación de usuarios
   - Operaciones CRUD principales
   - Procesos en segundo plano

4. **Verificar réplicas de base de datos**:
   ```bash
   # En el nodo maestro
   docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml exec postgres-master \
     psql -U $POSTGRES_USER -c "SELECT * FROM pg_stat_replication;"
   ```

5. **Verificar métricas de rendimiento**:
   ```bash
   curl -s http://localhost:8000/metrics | grep -v '^#'
   ```

6. **Verificar estado de Redis**:
   ```bash
   docker-compose -f /ruta/al/proyecto/docker-compose.prod.yml exec redis \
     redis-cli -a $REDIS_PASSWORD INFO
   ```

## 6. Contactos de Emergencia

En caso de que los procedimientos anteriores no resuelvan el problema, contacte a:

- **Responsable de Infraestructura**: 
  - Nombre: Juan Pérez
  - Teléfono: +34 600 000 001
  - Email: juan.perez@empresa.com

- **Soporte Técnico 24/7**:
  - Teléfono: +34 900 000 000
  - Email: soporte@empresa.com
  - Slack: #soporte-urgencias

- **Proveedor de Servicios en la Nube**:
  - Soporte AWS: +1-XXX-XXX-XXXX
  - Portal de soporte: https://support.aws.amazon.com/
  - Número de cuenta: XXXX-XXXX-XXXX

**Nota**: Mantenga esta documentación actualizada con cualquier cambio en la infraestructura o procedimientos.
