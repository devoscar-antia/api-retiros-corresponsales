# ADN Project

Sistema de corresponsales bancarios: registro de retiros con validación de montos, horarios y topes diarios.

## Autor y repositorio

- **GitHub:** [devoscar-antia](https://github.com/devoscar-antia)
- **Correo:** oscar.antia00@gmail.com
- **Repositorio:** [api-retiros-corresponsales](https://github.com/devoscar-antia/api-retiros-corresponsales)

## Stack

| Capa | Tecnología |
|------|------------|
| API | FastAPI, SQLAlchemy, Alembic, JWT (bcrypt) |
| Cliente | React 19, TypeScript, Vite, Material UI, Day.js |
| Base de datos | PostgreSQL (producción / Docker); SQLite posible en desarrollo local |

## Características destacadas

- Interfaz **responsive** (móvil y escritorio) y formulario de retiros con formato de **monto en español (COP)** (miles con punto, decimales con coma).
- Mensajes de **error de validación (HTTP 422) en español** y cuerpo de respuesta reducido (sin enlaces ni metadatos internos de Pydantic).
- **Documentación interactiva** de la API en `/docs` cuando el backend está en marcha.
- Semillas de datos para corresponsales y usuarios de prueba.

## Configuración inicial

### Backend (`backend/.env`)

Copia el ejemplo y ajusta valores (especialmente `SECRET_KEY` y `DATABASE_URL`):

```bash
cd backend
cp .env.example .env
```

- **Docker:** en `DATABASE_URL` usa `POSTGRES_HOST=db` (nombre del servicio en `docker-compose`).
- **PostgreSQL en tu máquina:** usa `POSTGRES_HOST=localhost` y la URL acorde.
- **SQLite (solo desarrollo):** puedes usar por ejemplo `DATABASE_URL=sqlite:///./adn.db` y crear tablas con los scripts de semilla o con Alembic según tu flujo.

### Docker Compose (archivo `.env` en la **raíz** del repositorio)

Para que `docker compose` levante Postgres y PgAdmin, crea un `.env` **junto a** `docker-compose.yml` con al menos:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=adn_corresponsal
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

Los valores deben ser coherentes con `backend/.env` cuando uses el stack con contenedores.

> El archivo `.env` no debe subirse al repositorio (está listado en `.gitignore`).

## Despliegue rápido con Docker

```bash
docker compose up --build
```

Servicios habituales:

- API: http://localhost:8000 (documentación: http://localhost:8000/docs)
- Frontend (contenedor): http://localhost:3000
- PgAdmin: http://localhost:8080
- PostgreSQL: `localhost:5432`

## Desarrollo local sin Docker

### Backend

Desde la carpeta `backend/`:

```bash
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Requisitos recomendados: **Python 3.11+** (el proyecto puede ejecutarse también en 3.9 con las dependencias actuales).

En Windows, si `pip install` falla al compilar `greenlet`, instala antes una versión con rueda precompilada, por ejemplo: `pip install "greenlet>=3.0.3,<3.2"`, o instala las [herramientas de compilación de Visual C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite suele servir la app en **http://localhost:5173** (o el siguiente puerto libre). La API por defecto se asume en `http://localhost:8000`. Puedes definir otra base con:

```env
# frontend/.env.local (opcional)
VITE_API_URL=http://localhost:8000
```

### Usuarios de prueba

| Correo | Contraseña |
|--------|------------|
| byte.chen@techcorp.com | Password123a |
| data.rodriguez@analytics.com | Password123b |
| cloud.martinez@devops.com | Password123c |

## Ejecutar scripts de semillas (Docker)

1. Entra al contenedor del backend:

```bash
docker exec -it adn_backend bash
```

2. Dentro del contenedor:

```bash
cd scripts
chmod +x seed_all.sh
./seed_all.sh
```

## Frontend (detalle)

<details>
<summary>Ver más</summary>

- React, TypeScript, Vite, ESLint
- Material UI y calendario localizado (español)
- Nginx en la imagen de producción del frontend

**Requisitos:** Node.js 18+ y npm o pnpm.

**Solo frontend en Docker:**

```bash
docker compose up frontend
```

</details>

## Backend (detalle)

<details>
<summary>Ver más</summary>

**Instalación de dependencias** (siempre desde `backend/`):

```bash
pip install -r requirements.txt
```

### Migraciones (Alembic)

Ejecuta los comandos **desde la carpeta `backend/`**, con el entorno virtual activado y `DATABASE_URL` definida en `.env`:

```bash
cd backend
alembic revision --autogenerate -m "descripción del cambio"
alembic upgrade head
alembic downgrade -1
alembic history
alembic current
```

### Semillas sin Docker

```bash
python backend/scripts/seed_corresponsales.py
python backend/scripts/seed_usuarios.py
python backend/scripts/seed_retiros.py
```

**Reset destructivo de tablas** (pide confirmación):

```bash
python backend/scripts/seed_reset.py
```

</details>

## Tests

<details>
<summary>Ver más</summary>

Desde la carpeta `backend/` con el venv activado:

```bash
cd backend
pytest
pytest tests/test_retiro.py
```

Ejemplos con salida a archivo:

```bash
pytest -s tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v1 > test_validar_multiples_horas_v1.log
pytest -s tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v2 > test_validar_multiples_horas_v2.log
```

</details>

## Estructura resumida

```
api-retiros-corresponsales/
├── backend/           # API FastAPI, modelos, scripts, Alembic
├── frontend/          # SPA React + Vite
├── docker-compose.yml
└── README.md
```
