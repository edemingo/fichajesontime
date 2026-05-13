# Etapa 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY api/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Etapa 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Instalar solo las dependencias de runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias de Python desde el builder
COPY --from=builder /root/.local /root/.local

# Copiar la aplicación
COPY api/ .
COPY main.py /workspace/main.py

# Variables de entorno
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Puerto por defecto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()"

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
