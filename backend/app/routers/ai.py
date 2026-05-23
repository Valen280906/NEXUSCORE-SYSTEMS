from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, Any
import io
from ..services.groq_service import GroqService
from ..services.pdf_service import PdfService

router = APIRouter(
    prefix="/ai",
    tags=["AI Integration & Export"]
)

class AnalysisRequest(BaseModel):
    knapsack_result: Dict[str, Any] = Field(..., description="Resultados obtenidos del algoritmo de servidores")
    routing_result: Dict[str, Any] = Field(..., description="Resultados obtenidos del algoritmo de enrutamiento")
    marketing_result: Dict[str, Any] = Field(..., description="Resultados obtenidos del algoritmo de presupuesto")

class ExportPdfRequest(BaseModel):
    knapsack_result: Dict[str, Any] = Field(..., description="Resultados del algoritmo de servidores")
    routing_result: Dict[str, Any] = Field(..., description="Resultados del algoritmo de enrutamiento")
    marketing_result: Dict[str, Any] = Field(..., description="Resultados del algoritmo de presupuesto")
    ai_conclusions: str = Field(..., description="Texto de conclusiones estratégicas del CTO (formato Markdown)")

@router.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze_results(payload: AnalysisRequest):
    """
    Se conecta con la API de Groq para formular y recibir un
    dictamen cualitativo y estratégico en rol de CTO.
    """
    try:
        conclusions = await GroqService.get_strategic_analysis(
            knapsack_res=payload.knapsack_result,
            routing_res=payload.routing_result,
            marketing_res=payload.marketing_result
        )
        return {"conclusions": conclusions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar análisis con Groq: {str(e)}"
        )

@router.post("/export-pdf")
def export_pdf_report(payload: ExportPdfRequest):
    """
    Genera en tiempo real un reporte formal en PDF y
    retorna el archivo binario para descarga directa.
    """
    try:
        pdf_bytes = PdfService.generate_report(
            knapsack_res=payload.knapsack_result,
            routing_res=payload.routing_result,
            marketing_res=payload.marketing_result,
            ai_conclusions=payload.ai_conclusions
        )
        
        # Devolver el archivo binario en streaming directo
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=NexusCore_Optimization_Report.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar reporte a PDF: {str(e)}"
        )
