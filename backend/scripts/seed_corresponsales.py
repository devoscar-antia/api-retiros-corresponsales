import os
import sys
import logging
from decimal import Decimal
from dotenv import load_dotenv

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import CorresponsalModel
from db.database import SessionLocal

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Formula investigada para entender como funciona el tope maximo:
b: es la precisión total del numero
s: es la precisión decimal del numero

b = 10
s = 2
Math.pow(b, b-s) - Math.pow(b, -s)

10^8 - 10^-2 = 99_999_999.99

Si colocamos base 11 en vez de base 10, ya podemos ingresar directamente los 100 millones sin problema
"""


def create_corresponsales():
    """Crea corresponsales de prueba en la base de datos."""
    db = SessionLocal()
    try:
        logger.info("Creando corresponsales de prueba...")

        # Lista de corresponsales a crear con nombres colombianos y montos en COP
        corresponsales = [
            {"nombre": "Chapinero", "tope_diario": Decimal("75_000_000.00")},
            {"nombre": "Poblado", "tope_diario": Decimal("100_000_000.00")},
            {"nombre": "San Andresito", "tope_diario": Decimal("50_000_000.00")},
            {"nombre": "Centro Histórico", "tope_diario": Decimal("85_000_000.00")},
            {"nombre": "Bocagrande", "tope_diario": Decimal("95_000_000.00")},
            {"nombre": "Usaquen", "tope_diario": Decimal("2_000_000.00")},
            {"nombre": "Kennedy", "tope_diario": Decimal("3_000_000.00")},
        ]

        for corresponsal_data in corresponsales:
            # Verificar si el corresponsal ya existe
            existing_corresponsal = (
                db.query(CorresponsalModel)
                .filter(CorresponsalModel.nombre == corresponsal_data["nombre"])
                .first()
            )

            if existing_corresponsal:
                logger.info(f"El corresponsal {corresponsal_data['nombre']} ya existe")
                continue

            # Crear nuevo corresponsal
            new_corresponsal = CorresponsalModel(
                nombre=corresponsal_data["nombre"],
                tope_diario=corresponsal_data["tope_diario"],
            )

            db.add(new_corresponsal)
            logger.info(f"{corresponsal_data['nombre']} creado exitosamente")

        db.commit()
        logger.info("Proceso de creación de corresponsales completado")

    except Exception as e:
        logger.error(f"Error al crear los corresponsales: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_corresponsales()
