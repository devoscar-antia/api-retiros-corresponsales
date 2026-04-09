"""
Traduce respuestas 422 de Pydantic v2 al español (mensajes mostrados en el cliente).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, List

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _fmt_cop(ge: Any) -> str:
    """Formatea un entero como miles con punto (estilo COP)."""
    try:
        v = int(Decimal(str(ge)))
        return f"{v:,}".replace(",", ".")
    except (ValueError, ArithmeticError, TypeError):
        return str(ge)


def _ultimo_campo(loc: tuple[Any, ...] | List[Any]) -> str | None:
    if not loc:
        return None
    return str(loc[-1])


def _error_respuesta_cliente(localizado: dict) -> dict:
    """Solo campos útiles para la API pública (sin url de docs ni input/ctx)."""
    out: dict = {}
    if "loc" in localizado:
        out["loc"] = localizado["loc"]
    if "msg" in localizado:
        out["msg"] = localizado["msg"]
    if "type" in localizado:
        out["type"] = localizado["type"]
    return out


def localizar_errores_validacion(errors: list) -> list:
    """Devuelve la misma estructura que exc.errors() con msg en español."""
    salida: list = []
    for err in errors:
        e = {**err}
        tipo = e.get("type", "")
        ctx = e.get("ctx") or {}
        loc = e.get("loc") or ()
        campo = _ultimo_campo(loc)

        if tipo == "greater_than_equal":
            ge = ctx.get("ge")
            if campo == "monto":
                e["msg"] = f"El monto debe ser mayor o igual a {_fmt_cop(ge)} COP"
            else:
                e["msg"] = f"El valor debe ser mayor o igual a {ge}"

        elif tipo == "less_than_equal":
            le = ctx.get("le")
            e["msg"] = f"El valor debe ser menor o igual a {le}"

        elif tipo == "decimal_max_places":
            dp = ctx.get("decimal_places", 2)
            if campo == "monto":
                e["msg"] = (
                    f"El monto admite como máximo {dp} decimales "
                    "(use el punto solo para centavos; ej. 50000.50)."
                )
            else:
                e["msg"] = f"Como máximo {dp} decimales permitidos"

        elif tipo == "decimal_parsing":
            if campo == "monto":
                e["msg"] = (
                    "Ingrese un monto válido: solo números y, si aplica, un punto "
                    "para decimales (ej. 50000 o 50000.50)."
                )
            else:
                e["msg"] = "El valor debe ser un número decimal válido"

        elif tipo in ("datetime_parsing", "date_from_datetime_parsing"):
            if campo == "fecha_hora":
                e["msg"] = (
                    "La fecha y hora no son válidas. Use el formato "
                    "AAAA-MM-DDTHH:MM o seleccione desde el calendario."
                )
            else:
                e["msg"] = "La fecha u hora no tienen un formato válido"

        elif tipo == "int_parsing":
            if campo == "corresponsal_id":
                e["msg"] = "El corresponsal debe indicarse con un número entero válido"
            elif campo == "monto":
                e["msg"] = "El monto debe ser un número válido"
            else:
                e["msg"] = "Debe ser un número entero válido"

        elif "Input should be greater than or equal to" in (e.get("msg") or ""):
            ge = ctx.get("ge")
            if campo == "monto":
                e["msg"] = f"El monto debe ser mayor o igual a {_fmt_cop(ge)} COP"
            else:
                e["msg"] = f"El valor debe ser mayor o igual a {ge}"

        elif "Input should be less than or equal to" in (e.get("msg") or ""):
            le = ctx.get("le")
            e["msg"] = f"El valor debe ser menor o igual a {le}"

        elif "Decimal input should have no more than" in (e.get("msg") or ""):
            dp = ctx.get("decimal_places", 2)
            if campo == "monto":
                e["msg"] = (
                    f"El monto admite como máximo {dp} decimales "
                    "(use el punto solo para centavos)."
                )

        salida.append(_error_respuesta_cliente(e))
    return salida


async def manejador_request_validation(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": localizar_errores_validacion(exc.errors())},
    )
