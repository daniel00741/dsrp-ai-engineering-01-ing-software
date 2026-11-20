from app.schemas import SolicitudIn, ClassificacionOut

PALABRAS_URGENTES = ["urgente", "caido", "caído", "no puedo", "sin servicio", "no funciona"]

def clasificar_solicitud(solicitud: SolicitudIn) -> ClassificacionOut:
    cliente = solicitud.cliente
    mensaje = solicitud.mensaje.lower()
    es_urgente = any(palabra in mensaje for palabra in PALABRAS_URGENTES)
    return ClassificacionOut(
        cliente=cliente,
        categoria="incidente" if es_urgente else "consulta", 
        prioridad="alta" if es_urgente else "normal",
        requiere_atencion=es_urgente,
        metodo="reglas_deterministas"
    )