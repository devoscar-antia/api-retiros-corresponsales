from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import UsuarioModel
from schemas.responses.usuario_schema import UsuarioCreateSchema


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db

    def get_usuarios(self, skip: int = 0, limit: int = 10) -> List[UsuarioModel]:
        """
        Obtiene la lista de usuarios.
        - skip: número de registros a saltar (paginación)
        - limit: número máximo de registros a retornar
        """
        return self.db.query(UsuarioModel).offset(skip).limit(limit).all()

    def get_usuario_by_id(self, usuario_id: int) -> UsuarioModel:
        """
        Obtiene un usuario por su ID
        """
        usuario = (
            self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        )
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario

    def get_current_user_data(self, current_user: UsuarioModel) -> UsuarioModel:
        """
        Obtiene los datos actualizados del usuario autenticado
        """
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id == current_user.id)
            .first()
        )
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario

    def create_usuario(self, usuario: UsuarioCreateSchema) -> UsuarioModel:
        """
        Registra un nuevo usuario
        """
        # Verificar si el correo ya existe
        db_usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.correo == usuario.correo)
            .first()
        )
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado",
            )

        try:
            # Crear el nuevo usuario
            db_usuario = UsuarioModel(
                nombre=usuario.nombre, correo=usuario.correo, clave=usuario.clave
            )

            self.db.add(db_usuario)
            self.db.commit()
            self.db.refresh(db_usuario)
            return db_usuario

        except ValueError as e:
            # Capturar errores de validación específicos del modelo
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor",
            )
