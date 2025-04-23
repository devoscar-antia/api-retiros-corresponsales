import os
import sys
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import RetiroModel, CorresponsalModel
from db.database import SessionLocal

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_corresponsal_id():
    """Solicita el ID del corresponsal y verifica su existencia."""
    while True:
        try:
            corresponsal_id = int(input("\nIngrese el ID del corresponsal: "))

            # Verificar si el corresponsal existe
            db = SessionLocal()
            corresponsal = (
                db.query(CorresponsalModel)
                .filter(CorresponsalModel.id == corresponsal_id)
                .first()
            )
            db.close()

            if not corresponsal:
                print(f"Error: No existe un corresponsal con ID {corresponsal_id}")
                continue

            return corresponsal_id
        except ValueError:
            print("Error: Por favor ingrese un número válido")
        except Exception as e:
            print(f"Error: {str(e)}")


def get_num_retiros():
    """Solicita el número de retiros a crear."""
    while True:
        try:
            response = input(
                "\n¿Cuántos retiros desea crear? (Enter para usar 100 por defecto): "
            ).strip()
            if not response:
                return 100
            num_retiros = int(response)
            if num_retiros <= 0:
                print("Error: El número de retiros debe ser mayor que 0")
                continue
            return num_retiros
        except ValueError:
            print("Error: Por favor ingrese un número válido")


def confirm_action(corresponsal_id: int, num_retiros: int):
    """Solicita confirmación al usuario."""
    while True:
        response = input(
            f"\n¿Desea crear {num_retiros} retiros aleatorios para el corresponsal ID {corresponsal_id}? (s/n): "
        ).lower()
        if response in ["s", "n"]:
            return response == "s"
        print("Por favor, responda 's' para sí o 'n' para no.")


def create_retiros():
    """Crea retiros de prueba para el corresponsal especificado."""

    # Obtener el ID del corresponsal
    corresponsal_id = get_corresponsal_id()

    # Obtener el número de retiros
    num_retiros = get_num_retiros()

    if not confirm_action(corresponsal_id, num_retiros):
        logger.info("Operación cancelada por el usuario.")
        return

    db = SessionLocal()
    try:
        logger.info("Creando retiros de prueba...")

        # Obtener la fecha actual
        today = datetime.now().date()

        # Crear los retiros
        for i in range(num_retiros):
            # Generar monto aleatorio entre 10,000 y 20,000
            monto = random.randint(10_000, 20_000)

            # Generar hora aleatoria entre 7 AM y 7 PM
            random_hour = random.randint(7, 19)  # 19 = 7 PM
            random_minute = random.randint(0, 59)

            # Si es 7 PM (19), asegurarse de que los minutos sean 0
            if random_hour == 19:
                random_minute = 0

            # Crear datetime con la fecha actual y la hora aleatoria
            fecha_hora = datetime.combine(
                today,
                datetime.min.time().replace(hour=random_hour, minute=random_minute),
            )

            # Crear nuevo retiro
            new_retiro = RetiroModel(
                corresponsal_id=corresponsal_id,
                monto=monto,
                fecha_hora=fecha_hora,
                usuario_id=1,
            )

            db.add(new_retiro)
            logger.info(
                f"Retiro #{i+1} creado: {monto} pesos - {fecha_hora.strftime('%Y-%m-%d %H:%M')}"
            )

        db.commit()
        logger.info("Proceso de creación de retiros completado")

    except Exception as e:
        logger.error(f"Error al crear los retiros: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_retiros()
