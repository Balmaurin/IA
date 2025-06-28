#!/bin/bash
set -e

# Cargar variables de entorno
if [ -f .env.ha ]; then
    export $(grep -v '^#' .env.ha | xargs)
else
    echo "Error: .env.ha no encontrado"
    exit 1
fi

# Verificar si estamos en modo Swarm
if ! docker node ls &> /dev/null; then
    echo "Inicializando Docker Swarm..."
    docker swarm init --advertise-addr $(hostname -I | awk '{print $1}')
fi

# Crear red overlay si no existe
if ! docker network ls | grep -q "traefik-public"; then
    echo "Creando red traefik-public..."
    docker network create --driver=overlay --attachable traefik-public
fi

# Desplegar servicios de seguridad
echo "Desplegando servicios de seguridad..."
docker-compose -f security/docker-compose.security.yml up -d

# Desplegar servicios de alta disponibilidad
echo "Desplegando servicios de alta disponibilidad..."
docker stack deploy -c docker-compose.ha.yml sheily-ha

echo "Esperando a que los servicios estén disponibles..."
sleep 30

echo "Verificando el estado de los servicios..."
docker service ls | grep sheily-ha

echo "Despliegue completado. Acceso a los servicios:"
echo "- API: http://localhost:8000"
echo "- Wazuh Dashboard: https://localhost:5601"
echo "- PgPool Admin: http://localhost:5432"

echo "Recuerda configurar tus DNS o /etc/hosts para acceder a los servicios por nombre de dominio."
