# Docker Setup

Este proyecto está configurado para ejecutarse en Docker con PostgreSQL.

## Requisitos

- Docker
- Docker Compose

## Instalación rápida

### 1. Clonar/preparar el proyecto

```bash
cd /home/edmingo/workspaces/python
```

### 2. Construir las imágenes

```bash
docker-compose build
```

### 3. Iniciar los servicios

```bash
docker-compose up -d
```

La aplicación estará disponible en `http://localhost:8500`

## Comandos útiles

### Ver logs
```bash
docker-compose logs -f api
```

### Detener servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (limpiar todo)
```bash
docker-compose down -v
```

### Reconstruir la imagen
```bash
docker-compose build --no-cache
```

### Ejecutar migraciones o comandos en el contenedor
```bash
docker-compose exec api python -c "your_command_here"
```

### Acceder a la consola PostgreSQL
```bash
docker-compose exec postgres psql -U appuser -d appdb
```

## Estructura

- **Dockerfile**: Imagen para la aplicación FastAPI
- **docker-compose.yml**: Orquestación de servicios (API, PostgreSQL)
- **.dockerignore**: Archivos excluidos del build
- **.env.example**: Variables de entorno de ejemplo

## Variables de entorno

Copia `.env.example` a `.env` si necesitas personalizar valores:

```bash
cp .env.example .env
```

## Desarrollo

Para desarrollo con hot-reload, descomenta la línea en `docker-compose.yml`:

```yaml
volumes:
  - ./api:/app
```

Luego reinicia con `docker-compose up`

## Problemas comunes

### Puerto 8500 en uso
```bash
docker-compose up -p python-
```

### Base de datos no inicializa
```bash
docker-compose down -v
docker-compose up
```

### Logs de error
```bash
docker-compose logs api
```

## Notas

- PostgreSQL está en `localhost:5432` desde el host
- La carpeta `/home/edmingo/Movimientos` está mapeada en el contenedor
