import httpx
from typing import Dict, Any
from ..config import settings

class GroqService:
    """
    Servicio de integración con la API de Groq para obtener
    conclusiones de negocio estratégicas tipo CTO.
    """
    
    @staticmethod
    async def get_strategic_analysis(
        knapsack_res: Dict[str, Any],
        routing_res: Dict[str, Any],
        marketing_res: Dict[str, Any]
    ) -> str:
        """
        Envía los resultados cuantitativos a la API de Groq y recibe
        un análisis cualitativo simulando el rol de un CTO.
        """
        
        # Estructurar el prompt formal
        prompt = f"""
Actúa como el Chief Technology Officer (CTO) de NexusCore Systems.
Analiza críticamente la viabilidad de negocio y técnica de los siguientes resultados de optimización cuantitativa obtenidos para nuestra plataforma interna:

1. CARGA DE SERVIDORES (OPTIMIZACIÓN DE DESPLIEGUE - PROGRAMACIÓN DINÁMICA):
   - Microservicios seleccionados para despliegue: {', '.join([item['name'] for item in knapsack_res.get('selected_items', [])])}
   - RAM total consumida: {knapsack_res.get('used_weight', 0)} GB de un límite máximo de {knapsack_res.get('capacity', 0)} GB
   - Valor de estabilidad total obtenido: {knapsack_res.get('max_value', 0)}

2. RED DE DISTRIBUCIÓN DE DATOS (ENRUTAMIENTO CRÍTICO - PROGRAMACIÓN DINÁMICA BACKWARD):
   - Ruta crítica óptima de menor latencia: {' -> '.join(routing_res.get('optimal_path', []))}
   - Latencia acumulada total: {routing_res.get('min_cost', 0.0)} ms

3. PRESUPUESTO DE MARKETING DE LANZAMIENTO (OPTIMIZACIÓN NO LINEAL):
   - Presupuesto óptimo asignado a Campañas de Creadores de Contenido (x1): ${marketing_res.get('constrained_optimum', {}).get('x1', 0.0) * 1000:,.2f}
   - Presupuesto óptimo asignado a Anuncios Programáticos (x2): ${marketing_res.get('constrained_optimum', {}).get('x2', 0.0) * 1000:,.2f}
   - Retorno estimado de nuevos usuarios mensuales: {marketing_res.get('constrained_optimum', {}).get('value', 0.0) * 1000:,.0f} usuarios

Por favor, estructura tu respuesta formal de negocio bajo las siguientes pautas:
- Escribe una introducción profesional y analítica sobre el rendimiento general del sistema.
- Evalúa si la latencia de {routing_res.get('min_cost', 0.0)} ms es competitiva y suficiente para la industria de desarrollo de software global actual y redes de distribución de contenido.
- Evalúa el riesgo de la distribución de memoria seleccionada ({knapsack_res.get('used_weight', 0)} GB utilizados de {knapsack_res.get('capacity', 0)} GB) en términos de estabilidad de infraestructura ante picos de demanda.
- Realiza un análisis financiero/comercial sobre el retorno de inversión (ROI) en marketing digital basándote en la asignación óptima calculada, considerando rendimientos decrecientes por saturación de mercado.
- Cierra con recomendaciones de cara a la implementación de estas decisiones estratégicas en NexusCore Systems.

Escribe la respuesta directamente en español, estructurada formalmente con títulos limpios y formato Markdown.
"""

        # Verificar que la API key esté presente y no sea el placeholder predeterminado
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY.strip() == "" or settings.GROQ_API_KEY == "tu_clave_de_api_aqui":
            raise ValueError(
                "La clave de API de Groq (GROQ_API_KEY) no está configurada en el archivo .env. "
                "Para obtener una de forma gratuita, regístrese en la consola oficial: https://console.groq.com/, "
                "genere una clave de API (comienza con 'gsk_') y agréguela a su archivo .env como GROQ_API_KEY=tu_clave"
            )

        # Si la API key está disponible, realizamos la llamada HTTP real a Groq
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": settings.GROQ_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3
                }
                
                response = await client.post(settings.GROQ_API_URL, json=data, headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    return response_json["choices"][0]["message"]["content"]
                else:
                    return f"""### ⚠️ Error de Comunicación con Groq (Código HTTP {response.status_code})
El servidor de Groq respondió con un error. A continuación se detalla el mensaje devuelto:

```
{response.text}
```

*Por favor, verifique que su clave `GROQ_API_KEY` en el archivo `.env` sea válida.*
"""
        except Exception as e:
            return f"""### ⚠️ Error de Conexión de Red
No se pudo establecer conexión con los servidores de Groq. 

*Detalle del error*: `{str(e)}`

*Verifique su conexión a internet y la configuración de red local.*
"""
