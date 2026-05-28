# Exportaciones públicas del paquete de routers
# Se importa la variable 'enrutador' de cada módulo para registrarla en main.py
from .optimization import enrutador as enrutador_optimizacion
from .ai           import enrutador as enrutador_ia

__all__ = [
    "enrutador_optimizacion",
    "enrutador_ia"
]
