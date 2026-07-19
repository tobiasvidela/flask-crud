# SGI | Sistema de Gestión Integral

SGI es un proyecto de ejemplo para gestionar usuarios mediante una aplicación sencilla de tres capas: un backend en Flask, un frontend de escritorio en Tkinter y una base de datos PostgreSQL. Su propósito es mostrar de forma clara cómo construir un CRUD completo, desde la API hasta la interfaz gráfica.

## ¿Qué hace este proyecto?

Permite realizar operaciones básicas sobre usuarios:

- Crear un usuario
- Listar todos los usuarios
- Consultar un usuario por ID
- Actualizar datos de un usuario
- Eliminar un usuario

La información se guarda en una base de datos relacional y se accede a través de una API REST.

## Arquitectura del proyecto

- Backend: está en la carpeta [backend](backend). Aquí se implementa la API con Flask y SQLAlchemy.
- Frontend: está en la carpeta [frontend](frontend). Aquí se desarrolla la interfaz gráfica con Tkinter.
- Base de datos: se gestiona con PostgreSQL y se levanta con Docker Compose.

## Estructura principal

- [backend/app.py](backend/app.py): define la API y los modelos de datos.
- [frontend/main.py](frontend/main.py): inicia la interfaz gráfica.
- [frontend/views](frontend/views): contiene las vistas y formularios del cliente desktop.
- [docker-compose.yml](docker-compose.yml): levanta el backend y la base de datos en contenedores.

## Requisitos

- Docker y Docker Compose
- Python 3.x (opcional, si se desea ejecutar el frontend localmente)

## Variables de entorno

Crea un archivo .env en la raíz del proyecto con variables como estas:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DB_URL=postgresql://postgres:postgres@flask_db:5432/postgres
```

## Ejecutar el proyecto

### 1. Levantar backend y base de datos

```bash
docker compose up --build
```

Esto iniciará:

- la API en http://localhost:4000
- la base de datos en el puerto 5432

> [!Warning] Recuerda: 
>  - Levantar el servicio docker (`sudo systemctl enable --now docker`)
>  - Usar `newgrp docker` y luego `docker ps` para comprobar

### 2. Ejecutar la interfaz gráfica

En otra terminal:

```bash
python frontend/main.py
```

## Endpoints de la API

La API expone estos endpoints:

- GET /users: obtener todos los usuarios
- POST /users: crear un usuario
- GET /users/<id>: obtener un usuario por ID
- PUT /users/<id>: actualizar un usuario
- DELETE /users/<id>: eliminar un usuario

## Propósito del proyecto

Este repositorio sirve como una base sencilla para aprender o practicar el flujo completo de una aplicación web con frontend, API y base de datos, usando herramientas modernas y fáciles de ejecutar localmente.
