from datetime import time

ERROR_MESSAGE_7AMPM = "Los retiros solo están permitidos entre 7:00 AM y 7:00 PM"
ERROR_MESSAGE_MONTO = "El monto debe estar entre 10,000 y 1,000,000 COP"

RETIRO_PERMITIDO_DESDE = time(7, 0, 0)
RETIRO_PERMITIDO_HASTA = time(19, 0, 0)

RETIRO_RANGO_DESDE = time(0, 0, 0)
RETIRO_RANGO_HASTA = time(23, 59, 59, 999999)

USUARIO_MINUTOS_BLOQUEO = 1
