import httpx
from typing import Dict, Any
from ..config import configuracion


class ServicioGroq:
    """
    Servicio de integración con la API de Groq.
    Construye el prompt formal, lo envía al modelo LLM y retorna
    el análisis cualitativo en rol de CTO (Chief Technology Officer).
    """

    @staticmethod
    async def obtener_analisis_estrategico(
        resultado_mochila:      Dict[str, Any],
        resultado_enrutamiento:  Dict[str, Any],
        resultado_marketing:    Dict[str, Any]
    ) -> str:
        """
        Envía los resultados numéricos de los tres algoritmos a la API de Groq
        y retorna un dictamen estratégico en texto (formato Markdown).

        Si la clave de API no está configurada, retorna un mensaje instructivo
        formateado en Markdown en lugar de lanzar una excepción.
        """

        # ----------------------------------------------------------------
        # Extraer valores clave de cada resultado para armar el prompt
        # ----------------------------------------------------------------
        # Mochila
        servicios_elegidos = ', '.join([
            item['nombre'] for item in resultado_mochila.get('elementos_elegidos', [])
        ])
        ram_usada   = resultado_mochila.get('peso_utilizado', 0)
        ram_total   = resultado_mochila.get('capacidad', 0)
        estabilidad = resultado_mochila.get('valor_maximo', 0)

        # Enrutamiento
        ruta_critica = ' → '.join(resultado_enrutamiento.get('ruta_optima', []))
        latencia_ms  = resultado_enrutamiento.get('costo_minimo', 0.0)

        # Marketing
        opt_marketing = resultado_marketing.get('optimo_restringido', {})
        x1_inversion  = opt_marketing.get('x1', 0.0)
        x2_inversion  = opt_marketing.get('x2', 0.0)
        retorno_users = opt_marketing.get('valor', 0.0)

        # Info de Lagrange (si está disponible)
        lagrange = resultado_marketing.get('metodo_lagrange', {})
        lambda_val = lagrange.get('multiplicador_lambda', 'N/A')

        # ----------------------------------------------------------------
        # Construir el prompt estructurado para el rol de CTO
        # ----------------------------------------------------------------
        prompt = f"""
Actúa como el Chief Technology Officer (CTO) de NexusCore Systems, empresa líder en infraestructura de software distribuido.
Analiza críticamente la viabilidad técnica y de negocio de los siguientes resultados de optimización cuantitativa:

## 1. CARGA DE SERVIDORES (Programación Dinámica - Mochila 0/1)
- Microservicios seleccionados para despliegue: {servicios_elegidos}
- RAM consumida: {ram_usada} GB de {ram_total} GB disponibles
- Índice de Estabilidad Total obtenido: {estabilidad}

## 2. RED DE DISTRIBUCIÓN DE DATOS (DP Backward - Ruta Crítica)
- Ruta de menor latencia calculada: {ruta_critica}
- Latencia acumulada total: {latencia_ms} ms

## 3. PRESUPUESTO DE MARKETING (Optimización No Lineal + Método de Lagrange)
- Inversión óptima en Creadores de Contenido (x1): ${x1_inversion * 1000:,.2f}
- Inversión óptima en Anuncios Programáticos (x2): ${x2_inversion * 1000:,.2f}
- Retorno estimado (nuevos usuarios/mes): {retorno_users * 1000:,.0f} usuarios
- Multiplicador de Lagrange (λ): {lambda_val}

Por favor, estructura tu análisis con los siguientes puntos:
1. **Evaluación de la latencia**: ¿Es {latencia_ms} ms competitivo para una red de distribución de software a escala global? ¿Cómo se compara con los estándares de la industria (CDN, microservicios cloud)?
2. **Riesgo de infraestructura**: Analiza el riesgo de usar {ram_usada} GB de {ram_total} GB de RAM ante picos de demanda. ¿Existe margen de escalabilidad?
3. **ROI de Marketing**: Evalúa la distribución del presupuesto y el retorno de {retorno_users * 1000:,.0f} usuarios considerando los rendimientos marginales decrecientes modelados. ¿Es eficiente la asignación?
4. **Interpretación del multiplicador λ = {lambda_val}**: ¿Qué significa este valor para la toma de decisiones de expansión de presupuesto?
5. **Recomendaciones estratégicas**: Acciones concretas para optimizar la infraestructura y el retorno de inversión de NexusCore Systems.

Escribe directamente en español formal, con títulos en Markdown (##) y formato profesional de informe ejecutivo.
"""

        # ----------------------------------------------------------------
        # Verificar que la clave de API esté configurada correctamente
        # ----------------------------------------------------------------
        clave_invalida = (
            not configuracion.GROQ_API_KEY or
            configuracion.GROQ_API_KEY.strip() == "" or
            configuracion.GROQ_API_KEY == "tu_clave_de_api_aqui"
        )

        if clave_invalida:
            # Retornar un mensaje instructivo en lugar de lanzar una excepción,
            # de modo que el frontend lo muestre como texto formateado
            return """## ⚠️ Clave de API de Groq No Configurada

El módulo de análisis estratégico con IA requiere una clave de API válida de **Groq**.

### ¿Cómo obtener tu clave gratuita?

1. Visita la consola oficial: **[https://console.groq.com/](https://console.groq.com/)**
2. Crea una cuenta gratuita o inicia sesión.
3. Ve a la sección **"API Keys"** y genera una nueva clave (comienza con `gsk_...`).
4. En la raíz del proyecto `backend/`, crea un archivo llamado **`.env`** con el siguiente contenido:

```
GROQ_API_KEY=gsk_tu_clave_aqui
```

5. Reinicia el servidor backend con `python run.py` y vuelve a ejecutar el análisis.

### ¿Por qué Groq?
Groq ofrece acceso **gratuito y de alta velocidad** al modelo `llama3-8b-8192`, ideal para análisis cuantitativos en tiempo real.

---
*Nota: Los resultados matemáticos de optimización ya están calculados y disponibles en las secciones anteriores.*
"""

        # ----------------------------------------------------------------
        # Realizar la llamada asíncrona a la API de Groq
        # ----------------------------------------------------------------
        try:
            async with httpx.AsyncClient(timeout=30.0) as cliente_http:
                encabezados = {
                    "Authorization": f"Bearer {configuracion.GROQ_API_KEY}",
                    "Content-Type":  "application/json"
                }
                cuerpo_solicitud = {
                    "model": configuracion.GROQ_MODELO,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                }

                respuesta = await cliente_http.post(
                    configuracion.GROQ_URL_API,
                    json=cuerpo_solicitud,
                    headers=encabezados
                )

                if respuesta.status_code == 200:
                    datos_respuesta = respuesta.json()
                    return datos_respuesta["choices"][0]["message"]["content"]
                else:
                    # Respuesta de error del servidor de Groq
                    return f"""## ⚠️ Error de Comunicación con Groq (HTTP {respuesta.status_code})

El servidor de Groq respondió con un código de error. Detalle:

```
{respuesta.text}
```

**Causas comunes:**
- La clave `GROQ_API_KEY` en el archivo `.env` no es válida o expiró.
- Se superó el límite de solicitudes gratuitas del plan.
- Problema temporal del servicio de Groq.

Verifique su clave en [console.groq.com](https://console.groq.com/) y vuelva a intentarlo.
"""

        except Exception as error_conexion:
            # Error de red o de conexión al intentar contactar a Groq
            return f"""## ⚠️ Error de Conexión de Red

No se pudo establecer comunicación con los servidores de Groq.

**Detalle técnico:** `{str(error_conexion)}`

**Verifique:**
- Su conexión a Internet esté activa.
- El servidor backend tenga acceso a redes externas.
- El firewall o proxy no esté bloqueando peticiones a `api.groq.com`.
"""
