import logging
from time import perf_counter
from fastapi import FastAPI, Depends, HTTPException
from app.schemas import SolicitudIn, ClassificacionOut
from app.service import clasificar_solicitud, obtener_clasificador
from app.config import modo_mantenimiento

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app=FastAPI(title="AI Service Desk", description="este es un ejemplo", version="1.0.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# @app.post("/classificar", response_model=ClassificacionOut)
# def classificar(solicitud: SolicitudIn) -> ClassificacionOut:
#     logger.info(f"clasificando solicitud de {solicitud.cliente}")
#     return clasificar_solicitud(solicitud)

@app.post("/classificar", response_model=ClassificacionOut)
def classificar(solicitud: SolicitudIn, clasificador = Depends(obtener_clasificador)) -> ClassificacionOut:
    if modo_mantenimiento():
        raise HTTPException(status_code=503, detail="Servicio en mantenimiento")
    inicio = perf_counter()
    resultado = clasificador.clasificar(solicitud)
    fin = perf_counter()
    logger.info(f"clasificando solicitud de {solicitud.cliente} en {fin-inicio} segundos")
    return resultado