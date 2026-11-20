import pytest
from app.schemas import SolicitudIn
from app.service import ClasificadorReglas, normalizar

@pytest.mark.parametrize("mensaje",[
    "Mi sistema esta CAÍDO",
    "El servicio está caído",
    "No puedo facturar",
    "Estamos sin servicio",
    "Es urgente resolverlo",
])

def test_mensaje_urgentes(mensaje: str) -> None:
    solicitud = SolicitudIn(cliente="empresa abc", mensaje=mensaje, canal="web")
    resultado = ClasificadorReglas().clasificar(solicitud)
    assert resultado.prioridad == "alta"
    assert resultado.categoria == "incidente"

def test_consulta_normal() -> None:
    solicitud = SolicitudIn(cliente="empresa abc", mensaje="necesito consultar mi estado", canal="correo")
    resultado = ClasificadorReglas().clasificar(solicitud)
    assert resultado.prioridad == "normal"
    assert resultado.requiere_atencion is False

def test_normalizar_acentos() -> None:
    assert normalizar("Caído") == "caido"