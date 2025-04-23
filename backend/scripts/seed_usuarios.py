import os
import sys
import logging
from dotenv import load_dotenv

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import UsuarioModel
from db.database import SessionLocal

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_usuarios():
    """Crea usuarios de prueba en la base de datos."""
    db = SessionLocal()
    try:
        logger.info("Creando usuarios de prueba...")

        # Lista de usuarios a crear
        usuarios = [
            {
                "nombre": "Alexandra Chen",
                "correo": "byte.chen@techcorp.com",
                "clave": "Password123a",
            },
            {
                "nombre": "Santiago Rodríguez",
                "correo": "data.rodriguez@analytics.com",
                "clave": "Password123b",
            },
            {
                "nombre": "Luna Martínez",
                "correo": "cloud.martinez@devops.com",
                "clave": "Password123c",
            },
        ]

        for usuario_data in usuarios:
            # Verificar si el usuario ya existe
            existing_usuario = (
                db.query(UsuarioModel)
                .filter(UsuarioModel.correo == usuario_data["correo"])
                .first()
            )

            if existing_usuario:
                logger.info(f"El usuario {usuario_data['correo']} ya existe")
                continue

            # Crear nuevo usuario
            new_usuario = UsuarioModel(
                nombre=usuario_data["nombre"],
                correo=usuario_data["correo"],
                clave=usuario_data["clave"],
            )

            db.add(new_usuario)
            logger.info(f"Usuario {usuario_data['correo']} creado exitosamente")

        db.commit()
        logger.info("Proceso de creación de usuarios completado")

    except Exception as e:
        logger.error(f"Error al crear los usuarios: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_usuarios()
