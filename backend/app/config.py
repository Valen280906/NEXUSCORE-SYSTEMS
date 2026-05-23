import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Settings:
    """
    Configuración global del sistema.
    """
    PROJECT_NAME: str = "NexusCore Systems Operational Optimizer"
    API_V1_STR: str = "/api/v1"
    
    # API Keys y endpoints
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    
    # Modelo de Groq recomendado por el PDF
    GROQ_MODEL: str = "llama3-8b-8192"

settings = Settings()
