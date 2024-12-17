# Base image
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Install system dependencies and OpenSSL for certificate generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Generate self-signed certificates
RUN mkdir -p /app/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /app/certs/local.key \
    -out /app/certs/local.crt \
    -subj "/C=US/ST=State/L=City/O=LocalDev/CN=localhost"

# Copy application code
COPY . .

# Expose HTTPS port
EXPOSE 8000

# Start FastAPI with HTTPS
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--ssl-keyfile", "/app/certs/local.key", "--ssl-certfile", "/app/certs/local.crt"]
