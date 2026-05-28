from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar configuración global
from .config import configuracion

# Importar los enrutadores (routers) ya renombrados a español
from .routers import enrutador_optimizacion, enrutador_ia

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=configuracion.NOMBRE_PROYECTO,
    description="Motor de Optimización Cuantitativa y Análisis CTO con IA para NexusCore Systems",
    version="1.0.0"
)

# Configurar middleware CORS
# Permite que el frontend cargado de forma local (ej: abriendo index.html en el navegador)
# o desde servidores de desarrollo realice peticiones sin restricciones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los enrutadores de la API con el prefijo global definido en la configuración
app.include_router(enrutador_optimizacion, prefix=configuracion.PREFIJO_API_V1)
app.include_router(enrutador_ia,           prefix=configuracion.PREFIJO_API_V1)

@app.get("/")
def raiz_api():
    """Endpoint raíz para comprobar el estado de la API."""
    return {
        "estado": "en_linea",
        "mensaje": f"Bienvenido a la API del {configuracion.NOMBRE_PROYECTO}",
        "documentacion": "/docs"
    }
