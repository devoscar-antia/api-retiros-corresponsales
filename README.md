# 🏦 Backend ADN Project

## 📝 Descripción

Backend del proyecto ADN, implementado con FastAPI.

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
