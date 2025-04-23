from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./adn.db")

try:
    # Crear engine con configuración específica para SQLite
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
        pool_pre_ping=True,  # Verifica la conexión antes de usarla
        pool_recycle=3600,   # Recicla conexiones cada hora
    )
    
    # Crear sesión local
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    logger.info("Conexión a la base de datos establecida correctamente")
    
except SQLAlchemyError as e:
    logger.error(f"Error al conectar con la base de datos: {str(e)}")
    raise

def get_db():
    """
    Obtiene una sesión de base de datos.
    Se asegura de cerrar la sesión incluso si ocurre un error.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close() 