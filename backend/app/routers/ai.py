from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, Any
import io

# Importar los servicios de integración IA y exportación PDF
from ..services.groq_service import ServicioGroq
from ..services.pdf_service  import ServicioPdf

# Router con prefijo "/ia" y etiqueta visible en la documentación Swagger
enrutador = APIRouter(
    prefix="/ia",
    tags=["Integración IA y Exportación PDF"]
)


# ============================================================
# MODELOS PYDANTIC — Validación de los datos de entrada
# ============================================================

class SolicitudAnalisis(BaseModel):
    """
    Datos requeridos para solicitar el análisis estratégico del CTO.
    Contiene los tres resultados numéricos de los algoritmos de optimización.
    """
    resultado_mochila:     Dict[str, Any] = Field(..., description="Resultados del Sub-problema A (Mochila de Servidores)")
    resultado_enrutamiento: Dict[str, Any] = Field(..., description="Resultados del Sub-problema B (Ruta por Etapas)")
    resultado_marketing:   Dict[str, Any] = Field(..., description="Resultados de la Parte II (Optimización de Marketing)")


class SolicitudExportarPdf(BaseModel):
    """
    Datos necesarios para generar y descargar el reporte técnico en PDF.
    Incluye los resultados numéricos más el dictamen cualitativo de la IA.
    """
    resultado_mochila:      Dict[str, Any] = Field(..., description="Resultados del optimizador de servidores")
    resultado_enrutamiento:  Dict[str, Any] = Field(..., description="Resultados del optimizador de enrutamiento")
    resultado_marketing:    Dict[str, Any] = Field(..., description="Resultados del optimizador de marketing")
    conclusiones_ia:        str            = Field(..., description="Texto del análisis estratégico del CTO (formato Markdown)")


# ============================================================
# ENDPOINTS DE LA API
# ============================================================

@enrutador.post("/analizar", status_code=status.HTTP_200_OK)
async def analizar_resultados(solicitud: SolicitudAnalisis):
    """
    Envía los resultados cuantitativos a la API de Groq y retorna
    un análisis cualitativo y estratégico en rol de CTO.
    Se ejecuta de forma asíncrona para no bloquear el servidor.
    """
    try:
        conclusiones = await ServicioGroq.obtener_analisis_estrategico(
            resultado_mochila      = solicitud.resultado_mochila,
            resultado_enrutamiento = solicitud.resultado_enrutamiento,
            resultado_marketing    = solicitud.resultado_marketing
        )
        return {"conclusiones": conclusiones}

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el análisis con Groq: {str(error)}"
        )


@enrutador.post("/exportar-pdf")
def exportar_reporte_pdf(solicitud: SolicitudExportarPdf):
    """
    Genera el reporte técnico formal en PDF con todos los resultados y conclusiones,
    y lo retorna como un archivo binario descargable.
    """
    try:
        bytes_pdf = ServicioPdf.generar_reporte(
            resultado_mochila      = solicitud.resultado_mochila,
            resultado_enrutamiento = solicitud.resultado_enrutamiento,
            resultado_marketing    = solicitud.resultado_marketing,
            conclusiones_ia        = solicitud.conclusiones_ia
        )

        # Retornar el PDF como streaming de bytes para descarga directa en el navegador
        return StreamingResponse(
            io.BytesIO(bytes_pdf),
            media_type="application/pdf",
            headers={
                "Content-Disposition":         "attachment; filename=NexusCore_Reporte_Optimizacion.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar el reporte PDF: {str(error)}"
        )
