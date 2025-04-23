import os
import sys
import logging
from dotenv import load_dotenv

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base
from db.database import engine

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Inicializa la base de datos creando todas las tablas necesarias."""
    try:
        confirmacion = input("¡ADVERTENCIA! Esto borrará todas las tablas existentes. ¿Desea continuar? (si/n/no): ")
        if confirmacion.lower() != 'si':
            logger.info("Operación cancelada por el usuario")
            return
            
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 