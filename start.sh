#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando Sheily Light...${NC}"

# Función para limpiar procesos al salir
cleanup() {
  echo -e "\n${GREEN}Deteniendo procesos...${NC}"
  pkill -f "uvicorn main:app" || true
  pkill -f "vite" || true
  exit 0
}

# Capturar la señal de interrupción
trap cleanup SIGINT

# Navegar al directorio del backend y activar el entorno virtual si existe
cd /home/yo/CascadeProyects/sheily-light

# Iniciar el backend en segundo plano
echo -e "${BLUE}Iniciando el backend...${NC}"
(
  cd apps/sheily_light_api
  # Instalar dependencias si es necesario
  pip install -r requirements.txt > /dev/null 2>&1
  # Instalar el paquete en modo desarrollo
  pip install -e /home/yo/CascadeProyects/sheily-light > /dev/null 2>&1
  # Iniciar el servidor
  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
) &


# Esperar un momento a que el backend se inicie
echo -e "${GREEN}Backend iniciado en http://localhost:8000${NC}"
echo -e "${GREEN}Documentación de la API: http://localhost:8000/docs${NC}"

# Iniciar el frontend en segundo plano
echo -e "${BLUE}Iniciando el frontend...${NC}"
(
  cd web
  # Instalar dependencias si es necesario
  npm install > /dev/null 2>&1
  # Iniciar el servidor de desarrollo
  npm run dev
) &

echo -e "${GREEN}Frontend iniciado en http://localhost:5173${NC}"

# Mantener el script en ejecución
wait
