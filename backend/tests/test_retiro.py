from datetime import datetime, time
import pytest
from fastapi import HTTPException
from functions.retiro_validate import raise_validar_hora_retiro_v1, raise_validar_hora_retiro_v2, ERROR_MESSAGE_7AMPM
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRetiroGroup:
    def test_simple_comparison(self):
        # Arrange
        valor_esperado = 'A'
        
        # Act
        valor_actual = 'A'
        
        # Assert
        assert valor_actual == valor_esperado 
        
    def test_validar_hora_retiro_v1(self):
        # Arrange
        hora_actual = datetime.combine(datetime.now().date(), time(19, 0, 1))
        
        # Act & Assert
        with pytest.raises(HTTPException) as excinfo:
            raise_validar_hora_retiro_v1(hora_actual)
        
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == ERROR_MESSAGE_7AMPM
        
    def test_validar_hora_retiro_v2(self):
        # Arrange
        hora_actual = datetime.combine(datetime.now().date(), time(19, 0, 1))
        
        # Act & Assert
        with pytest.raises(HTTPException) as excinfo:
            raise_validar_hora_retiro_v2(hora_actual)
       
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == ERROR_MESSAGE_7AMPM
        
    def test_validar_multiples_horas_v1(self):
        # Arrange
        hora = 0
        minuto = 0
        segundo = 0
        print(f"\nProbando horarios de retiro v1\n")

        # Act & Assert
        while hora < 24:
            hora_actual = datetime.combine(
                datetime.now().date(),
                time(hora, minuto, segundo)
            )
            
            print(f"Probando hora: {hora_actual.strftime('%H:%M:%S')}")
            
            if 7 <= hora < 19 or (hora == 19 and minuto == 0 and segundo == 0):
                # No debería lanzar excepción entre 7:00 AM y 7:00 PM
                try:
                    raise_validar_hora_retiro_v1(hora_actual)
                    print("[OK] Permitido")
                except HTTPException:
                    assert False, f"No debería lanzar error a las {hora:02d}:{minuto:02d}:{segundo:02d}"
            else:
                # Debería lanzar excepción fuera del horario permitido
                with pytest.raises(HTTPException) as excinfo:
                    raise_validar_hora_retiro_v1(hora_actual)
                
                assert excinfo.value.status_code == 400
                assert excinfo.value.detail == ERROR_MESSAGE_7AMPM
                print("[ERROR] Denegado")
            
            segundo += 1
            if segundo == 60:
                segundo = 0
                minuto += 1
            if minuto == 60:
                minuto = 0
                hora += 1

    def test_validar_multiples_horas_v2(self):
        # Arrange
        hora = 0
        minuto = 0
        segundo = 0
        print(f"\nProbando horarios de retiro v2\n")

        # Act & Assert
        while hora < 24:
            hora_actual = datetime.combine(
                datetime.now().date(),
                time(hora, minuto, segundo)
            )
            
            print(f"Probando hora: {hora_actual.strftime('%H:%M:%S')}")
            
            if 7 <= hora < 19 or (hora == 19 and minuto == 0 and segundo == 0):
                # No debería lanzar excepción entre 7:00 AM y 7:00 PM
                try:
                    raise_validar_hora_retiro_v2(hora_actual)
                    print("[OK] Permitido")
                except HTTPException:
                    assert False, f"No debería lanzar error a las {hora:02d}:{minuto:02d}:{segundo:02d}"
            else:
                # Debería lanzar excepción fuera del horario permitido
                with pytest.raises(HTTPException) as excinfo:
                    raise_validar_hora_retiro_v2(hora_actual)
                
                assert excinfo.value.status_code == 400
                assert excinfo.value.detail == ERROR_MESSAGE_7AMPM
                print("[ERROR] Denegado")
            
            segundo += 1
            if segundo == 60:
                segundo = 0
                minuto += 1
            if minuto == 60:
                minuto = 0
                hora += 1

