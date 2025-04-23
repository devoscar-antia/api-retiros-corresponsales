# 🏦 ADN Project

## ⚙️ Configuración Inicial

Antes de desplegar el proyecto, es necesario configurar las variables de entorno:

1. Crear el archivo `.env` en el directorio `backend/`:

```bash
cd backend
cp .env.example .env
```

> Nota: Configurar las variables en el archivo `.env`

## 🐳 Ejecutar Scripts de Semillas (Docker)

Si estás usando Docker, para ejecutar todos los scripts de semillas:

1. Accede al contenedor del backend:

```bash
docker exec -it adn_backend bash
```

2. Dentro del contenedor:

```bash
cd scripts
chmod +x seed_all.sh
./seed_all.sh
```

#### 👤 Usuarios de Prueba

Los siguientes usuarios están disponibles para pruebas:

| Correo                       | Contraseña   |
| ---------------------------- | ------------ |
| byte.chen@techcorp.com       | Password123a |
| data.rodriguez@analytics.com | Password123b |
| cloud.martinez@devops.com    | Password123c |

## 🚀 Despliegue Rápido con Docker

Para desplegar todo el proyecto (backend, frontend y base de datos) con un solo comando:

```bash
docker-compose up --build
```

Este comando construirá y ejecutará:

- Backend en http://localhost:8000
- Frontend en http://localhost:3000
- PgAdmin en http://localhost:8080
- Base de datos PostgreSQL en localhost:5432

## 📝 Descripción

Proyecto ADN implementado con FastAPI en el backend y React + TypeScript en el frontend.

## 🖥️ Frontend

<details>
<summary>Ver mas</summary>

El frontend está desarrollado con:

- React
- TypeScript
- Vite
- ESLint para linting
- Nginx para producción

### 📋 Requisitos

- Node.js 18+
- pnpm (recomendado) o npm

### ⚙️ Instalación

1. Instalar dependencias:

```bash
cd frontend
pnpm install
```

2. Iniciar en modo desarrollo:

```bash
pnpm dev
```

3. Construir para producción:

```bash
pnpm build
```

### 🐳 Docker

El frontend se puede ejecutar en un contenedor Docker:

```bash
docker-compose up frontend
```

</details>

## 📋 Requisitos

<details>
<summary>Ver mas</summary>

- Python 3.11+
- pip

## ⚙️ Instalación

1. Crear un entorno virtual:

```bash
python -m venv venv
```

2. Activar el entorno virtual:

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

</details>

## 💾 Base de Datos

<details>
<summary>Ver mas</summary>

### 🔄 Migraciones con Alembic

Para manejar las migraciones de la base de datos:

1. Crear una nueva migración:

```bash
alembic revision --autogenerate -m "descripción del cambio"
```

2. Aplicar las migraciones:

```bash
alembic upgrade head
```

3. Revertir la última migración:

```bash
alembic downgrade -1
```

4. Ver el historial de migraciones:

```bash
alembic history
```

5. Ver el estado actual de las migraciones:

```bash
alembic current
```

### 🌱 Semillas de Datos

#### 👥 Corresponsales

Para crear los corresponsales de prueba:

```bash
python backend/scripts/seed_corresponsales.py
```

#### ⚠️ Reset de Base de Datos (Opcional)

⚠️ **ADVERTENCIA**: Este comando eliminará todas las tablas existentes.

```bash
python backend/scripts/seed_reset.py
```

#### 💰 Retiros Aleatorios (Opcional)

Para crear retiros aleatorios de prueba:

```bash
python backend/scripts/seed_retiros.py
```

#### 🐳 Ejecutar todos los scripts de semillas (Docker)

Si estás usando Docker, primero accede al contenedor del backend:

```bash
docker exec -it adn_backend bash
```

Luego, dentro del contenedor:

```bash
cd scripts
chmod +x seed_all.sh
./seed_all.sh
```

</details>

## 🧪 Tests

<details>
<summary>Ver mas</summary>

### 🏃‍♂️ Ejecutar todos los tests

```bash
pytest
```

### 📊 Tests específicos

#### ⏰ Validación de horarios de retiro

Para probar la validación de horarios de retiro y generar un log detallado:

> Con archivo de salida:

```bash
pytest -s tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v1 > test_validar_multiples_horas_v1.log
```

```bash
pytest -s tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v2 > test_validar_multiples_horas_v2.log
```

> Sin archivo de salida:

```bash
pytest tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v1
```

```bash
pytest tests/test_retiro.py::TestRetiroGroup::test_validar_multiples_horas_v2
```

> Todos los test para retiro:

```bash
pytest tests/test_retiro.py
```

</details>
