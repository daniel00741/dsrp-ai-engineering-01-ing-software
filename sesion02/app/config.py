import os

def modo_mantenimiento() -> bool:
    """lee la configuracion del entorno en cada solicitud"""
    valor = os.getenv("MODO_MANTENIMIENTO", "False")
    return valor.casefold() in ("true","1","yes")
