from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import optimization_router, ai_router

app = FastAPI(
    title=settings.PROJECT_NAME,
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

# Registrar enrutadores de la API con su prefijo
app.include_router(optimization_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": f"Bienvenido a la API del {settings.PROJECT_NAME}",
        "documentation": "/docs"
    }
