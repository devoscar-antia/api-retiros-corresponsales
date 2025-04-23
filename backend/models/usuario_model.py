import re
import bcrypt
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, validates
from .base_model import Base
from globals.retiro_vars import USUARIO_MINUTOS_BLOQUEO


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    clave = Column(String(60), nullable=False)
    bloqueado_hasta = Column(DateTime(timezone=True), nullable=True)
    intentos_fallidos = Column(Integer, default=0)

    @validates("nombre")
    def validate_nombre(self, key, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder los 100 caracteres")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
        return nombre

    @validates("correo")
    def validate_email(self, key, correo):
        if not correo:
            raise ValueError("El correo electrónico no puede estar vacío")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise ValueError("Formato de correo electrónico inválido")
        return correo

    @validates("clave")
    # Nota: Este decorador apunta a la tabla usuarios a la columna clave
    # y se activa cuando se inserta o actualiza un valor en la columna clave
    def validate_clave(self, key, clave):
        if not clave:
            raise ValueError("La clave no puede estar vacía")
        if len(clave) < 8:
            raise ValueError("La clave debe tener al menos 8 caracteres")
        if len(clave) > 72:
            raise ValueError("La clave no puede exceder los 72 caracteres")
        if not any(c.isupper() for c in clave):
            raise ValueError("La clave debe contener al menos una letra mayúscula")
        if not any(c.islower() for c in clave):
            raise ValueError("La clave debe contener al menos una letra minúscula")
        if not any(c.isdigit() for c in clave):
            raise ValueError("La clave debe contener al menos un número")

        # Convertir la contraseña a bytes si es string
        if isinstance(clave, str):
            clave = clave.encode("utf-8")

        # Generar el hash de la contraseña
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(clave, salt)

        # Retornar el hash en formato string
        return hashed.decode("utf-8")

    # Relaciones
    retiros = relationship("RetiroModel", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario {self.nombre}>"

    def puede_intentar_retiro(self):
        """
        Verifica si el usuario puede intentar un nuevo retiro
        """
        if self.bloqueado_hasta and self.bloqueado_hasta > datetime.now(
            self.bloqueado_hasta.tzinfo
        ):
            return False
        return True

    def incrementar_intentos_fallidos(self):
        """
        Incrementa el contador de intentos fallidos y bloquea si es necesario
        """
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 3:
            self.bloqueado_hasta = datetime.now(timezone.utc) + timedelta(
                minutes=USUARIO_MINUTOS_BLOQUEO
            )
            self.intentos_fallidos = 0
            return 3
        return self.intentos_fallidos

    def reiniciar_intentos_fallidos(self):
        """
        Reinicia el contador de intentos fallidos
        """
        self.intentos_fallidos = 0

    def get_tiempo_bloqueo_restante(self):
        """
        Retorna el tiempo restante de bloqueo en minutos y segundos
        """
        if not self.bloqueado_hasta or self.bloqueado_hasta <= datetime.now(
            self.bloqueado_hasta.tzinfo
        ):
            return (0, 0)
        diferencia = self.bloqueado_hasta - datetime.now(self.bloqueado_hasta.tzinfo)
        total_segundos = int(diferencia.total_seconds())
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return (minutos, segundos)
