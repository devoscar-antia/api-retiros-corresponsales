import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from routers import auth_router, usuario_router, retiro_router, corresponsal_router
from validation_locale import manejador_request_validation

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="ADN Project API", description="API para el proyecto ADN", version="0.0.1"
)

app.add_exception_handler(RequestValidationError, manejador_request_validation)

# Configuración del esquema de seguridad
app.openapi_schema = None  # Necesario para poder modificar el esquema
app.swagger_ui_init_oauth = {}

# Configuración de CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",  # Vite dev server (puerto alterno)
    "http://localhost:3000",  # React dev server
    "http://localhost:8000",  # FastAPI dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Definir el esquema de seguridad
security = HTTPBearer()

# El resto de la configuración de seguridad se puede simplificar a:
app.openapi_components = {
    "securitySchemes": {
        "Bearer": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
}

# Incluir los routers
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(retiro_router)
app.include_router(corresponsal_router)


@app.get("/", tags=["inicio"])
def read_root():
    return HTMLResponse("<h2>Mi Server</h2>")
