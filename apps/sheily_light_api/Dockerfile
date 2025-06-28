# ---------- SHEILY-light API Dockerfile ----------
# Build stage
FROM python:3.11-slim AS builder

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Working directory inside container
WORKDIR /app

# Install system deps (if any needed later add here)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/sheily_routers

# Copy application code
COPY . .
COPY sheily_routers/ /app/sheily_routers/

# Expose API port
EXPOSE 8000

# Default command
CMD ["uvicorn", "sheily_main_api:app", "--host", "0.0.0.0", "--port", "8000"]
