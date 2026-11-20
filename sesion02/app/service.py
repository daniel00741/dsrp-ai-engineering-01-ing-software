import unicodedata
from typing import Protocol
from app.schemas import SolicitudIn, ClassificacionOut

PALABRAS_URGENTES = ["urgente", "caido", "caído", "no puedo", "sin servicio", "no funciona"]

def normalizar(texto: str) -> str:
    """Minuscuulas y sin marcas de acentos para comparar expresiones"""
    texto=unicodedata.normalize('NFKD', texto.casefold())
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))

class Clasificador(Protocol):
    def clasificar(self, solicitud: SolicitudIn) -> ClassificacionOut: ...

class ClasificadorReglas:
    def clasificar(self, solicitud: SolicitudIn) -> ClassificacionOut:
        mensaje = normalizar(solicitud.mensaje)
        es_urgente = any(palabra in mensaje for palabra in PALABRAS_URGENTES)
        return ClassificacionOut(
            cliente=solicitud.cliente,
            categoria="incidente" if es_urgente else "consulta",
            prioridad="alta" if es_urgente else "normal",
            requiere_atencion=es_urgente,
            metodo="reglas deterministas"
        )
    
def obtener_clasificador() -> Clasificador:
    """punto de extension para un clasificador LLM en proximos cursos"""
    return ClasificadorReglas()
        
def clasificar_solicitud(solicitud: SolicitudIn) -> ClassificacionOut:
    return ClasificadorReglas().clasificar(solicitud)