#!/bin/bash

# Script de inicio completo para SHEILY-light
# Inicia todos los servicios en el orden correcto con tiempos de espera adecuados

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes de estado
status() {
    echo -e "${GREEN}[*]${NC} $1"
    sleep 1
}

echo -e "${GREEN}[*]${NC} Iniciando SHEILY-light..."

# Verificar si Docker está en ejecución
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}[!] Docker no está en ejecución. Iniciando Docker...${NC}"
    sudo systemctl start docker
    sleep 5
fi

# 1. Iniciar la base de datos
echo -e "${GREEN}[*]${NC} Iniciando base de datos PostgreSQL..."
docker-compose -f docker-compose.prod.yml up -d db

# Esperar a que la base de datos esté lista
echo -e "${GREEN}[*]${NC} Esperando a que la base de datos esté lista (30 segundos)..."
sleep 30

# 2. Iniciar el servicio de Ollama
echo -e "${GREEN}[*]${NC} Iniciando servicio Ollama..."
docker run -d --name ollama -p 11434:11434 -v ollama_data:/root/.ollama ollama/ollama

# Esperar a que Ollama esté listo
echo -e "${GREEN}[*]${NC} Esperando a que Ollama esté listo (20 segundos)..."
sleep 20

# 3. Descargar e instalar los modelos de IA
echo -e "${GREEN}[*]${NC} Descargando modelos de IA (esto puede tomar varios minutos)..."

# Descargar Llama 3 (versión 8B para ahorrar recursos)
echo -e "${GREEN}[*]${NC} Descargando modelo Llama 3..."
docker exec -d ollama ollama pull llama3:8b

# Descargar Deepseek Coder (versión 6.7B para desarrollo)
echo -e "${GREEN}[*]${NC} Descargando modelo Deepseek Coder..."
docker exec -d ollama ollama pull deepseek-coder:6.7b

# 4. Iniciar la API de SHEILY-light
echo -e "${GREEN}[*]${NC} Iniciando la API de SHEILY-light..."
docker-compose -f docker-compose.prod.yml up -d api

# 5. Iniciar el frontend web
echo -e "${GREEN}[*]${NC} Iniciando la interfaz web..."
docker-compose -f docker-compose.prod.yml up -d web

# 6. Verificar el estado de los servicios
echo -e "${GREEN}[*]${NC} Verificando el estado de los servicios..."
docker ps --format "table {{.Names}}\t{{.Status}}"

# Mostrar mensaje de finalización
echo -e "\n${GREEN}[+] ¡SHEILY-light se ha iniciado correctamente!${NC}"
echo -e "Accede a la interfaz web en: ${YELLOW}http://localhost:3000${NC}"
echo -e "API disponible en: ${YELLOW}http://localhost:8000${NC}"
echo -e "Ollama disponible en: ${YELLOW}http://localhost:11434${NC}"

# Mostrar logs de los servicios en tiempo real
echo -e "\n${YELLOW}Mostrando logs (presiona Ctrl+C para salir)...${NC}"
docker-compose -f docker-compose.prod.yml logs -f
