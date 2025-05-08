# API de Notas con FastAPI y Docker

Una aplicación sencilla para gestionar notas, construida con FastAPI y SQLite, desplegada con Docker.

## ¿Qué hace esta aplicación?

Esta API permite:
- Crear y guardar notas con título y contenido
- Consultar todas las notas guardadas
- Mantener los datos incluso después de reiniciar los contenedores (persistencia real)

## Cómo ejecutar la aplicación

### Opción 1: Local con Docker Desktop

```bash
# Clona el repositorio
git clone https://github.com/AndruTellesR/fastapi-docker.git
cd fastapi-docker

# Construye y ejecuta los contenedores
docker compose up --build
```

La aplicación estará disponible en: http://localhost:8000

### Opción 2: Con Play-with-Docker (PWD)

1. Inicia sesión en https://labs.play-with-docker.com
2. Crea una instancia nueva
3. Clona el repositorio: `git clone https://github.com/AndruTellesR/fastapi-docker.git`
4. Entra al directorio: `cd fastapi-docker`
5. Ejecuta: `docker compose up --build`
6. Usa la URL pública que te proporciona PWD para acceder a la API

## Cómo probar la API

### 1. Verificar que la aplicación está funcionando

Abre en el navegador o usa curl:
```
http://localhost:8000
```

Deberías ver un mensaje de bienvenida.

### 2. Crear una nueva nota

Envía un POST a `/notes` con los datos de la nota:

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera nota",
    "content": "Esta es una nota de prueba"
  }'
```

También puedes usar herramientas como Postman o ThunderClient en VS Code.

### 3. Obtener todas las notas

```bash
curl http://localhost:8000/notes
```

### 4. Comprobar la persistencia de datos

Para verificar que los datos persisten entre reinicios:

1. Crea algunas notas como se muestra arriba
2. Detén los contenedores (Ctrl+C en la terminal donde ejecutaste docker compose)
3. Inicia los contenedores nuevamente: `docker compose up`
4. Consulta las notas: `curl http://localhost:8000/notes`

¡Todas tus notas deberían seguir allí! Esto demuestra que la persistencia funciona correctamente.

## Estructura del Proyecto

- `app/main.py`: Implementación de la API con FastAPI (endpoints)
- `app/database.py`: Configuración de SQLite y modelo de datos
- `app/schemas.py`: Esquemas de Pydantic para validación de datos
- `Dockerfile`: Configuración para construir la imagen Docker
- `docker-compose.yaml`: Configuración de servicios, redes y volúmenes
- `requirements.txt`: Dependencias de Python

## Tecnologías utilizadas

- FastAPI: Framework web de alto rendimiento
- SQLite: Base de datos ligera y portable
- SQLAlchemy: ORM para trabajar con la base de datos
- Docker: Contenedorización de la aplicación
- Pydantic: Validación de datos
