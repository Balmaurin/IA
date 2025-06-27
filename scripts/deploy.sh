#!/usr/bin/env bash
# SHEILY-light deployment script
# Usage: ./scripts/deploy.sh [environment]
# If no environment is provided, defaults to "production" which expects docker-compose.production.yml
# Other common option: "dev" which expects docker-compose.dev.yml
# The script builds images, starts containers, and runs DB migrations for the API.

set -euo pipefail

ENVIRONMENT="${1:-production}"
COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

# Determine docker compose command
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
elif docker compose version >/dev/null 2>&1; then
  DC="docker compose"
else
  echo "[deploy.sh] ERROR: Neither 'docker-compose' nor 'docker compose' is available. Install Docker Compose v1 or v2." >&2
  exit 1
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "[deploy.sh] ERROR: File $COMPOSE_FILE not found. Make sure the compose file exists in the project root."
  exit 1
fi

# Build containers
printf "\n[deploy.sh] Building Docker images for '%s' environment...\n" "$ENVIRONMENT"
$DC -f "$COMPOSE_FILE" build

# Start containers in detached mode
printf "\n[deploy.sh] Starting Docker services...\n"
$DC -f "$COMPOSE_FILE" up -d

# Wait for database to be ready (simple health-check loop)
printf "[deploy.sh] Waiting for Postgres to be ready..."
RETRIES=20
until $DC -f "$COMPOSE_FILE" exec -T db pg_isready -U "${POSTGRES_USER:-sheily}" >/dev/null 2>&1 || [ "$RETRIES" -eq 0 ]; do
  printf '.'
  sleep 2
  RETRIES=$((RETRIES-1))
done
if [ "$RETRIES" -eq 0 ]; then
  echo "\n[deploy.sh] ERROR: Postgres did not become ready in time." >&2
  exit 1
fi
printf " done\n"

# Run migrations inside the API container (if Alembic is present)
printf "\n[deploy.sh] Running database migrations...\n"
if $DC -f "$COMPOSE_FILE" exec -T api bash -c "command -v alembic >/dev/null 2>&1"; then
  $DC -f "$COMPOSE_FILE" exec -T api alembic upgrade head
  printf "[deploy.sh] Migrations applied.\n"
else
  printf "[deploy.sh] Alembic not found — skipping migrations.\n"
fi

printf "\n[deploy.sh] SHEILY-light is deployed and running!\n"
