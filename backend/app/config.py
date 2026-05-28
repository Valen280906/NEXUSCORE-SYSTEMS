import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Configuracion:
    """
    Configuración global del sistema.
    Almacena variables de entorno, claves de API y constantes del proyecto.
    """
    NOMBRE_PROYECTO: str = "Sistema de Optimización NEXUSCORE"
    PREFIJO_API_V1:  str = "/api/v1"

    # API Keys y endpoints
    # Si no existe en el entorno, será una cadena vacía
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_URL_API: str = "https://api.groq.com/openai/v1/chat/completions"

    # Modelo de Groq recomendado por el PDF para este proyecto
    GROQ_MODELO:  str = "llama3-8b-8192"

# Instancia global de configuración
configuracion = Configuracion()
