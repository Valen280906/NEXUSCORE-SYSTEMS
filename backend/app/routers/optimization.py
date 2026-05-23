from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from ..algorithms.knapsack import KnapsackOptimizer
from ..algorithms.stage_coach import StagecoachOptimizer
from ..algorithms.non_linear import NonLinearOptimizer

router = APIRouter(
    prefix="/optimize",
    tags=["Optimization Engines"]
)

# ----------------------------------------------------
# 1. Pydantic Models for Knapsack (Sub-problema A)
# ----------------------------------------------------
class MicroserviceInput(BaseModel):
    id: int = Field(..., description="ID único del microservicio")
    name: str = Field(..., description="Nombre identificativo")
    weight: int = Field(..., gt=0, description="Requisito de RAM (wi) en GB")
    value: int = Field(..., ge=0, description="Valor de prioridad de estabilidad (vi)")

class KnapsackRequest(BaseModel):
    capacity: int = Field(16, ge=1, le=128, description="Capacidad máxima de RAM del servidor maestro")
    items: List[MicroserviceInput] = Field(..., min_items=1, description="Lista de microservicios disponibles")

# ----------------------------------------------------
# 2. Pydantic Models for Stagecoach (Sub-problema B)
# ----------------------------------------------------
class StagecoachRequest(BaseModel):
    stages: List[List[str]] = Field(
        ...,
        min_items=2,
        description="Lista ordenada de etapas y sus nodos. Ej: [['A'], ['B','C'], ['D']]"
    )
    connections: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Grafo de latencias. Estructura: {nodo_origen: {nodo_destino: costo}}"
    )

# ----------------------------------------------------
# 3. Pydantic Models for Non-Linear (Parte II)
# ----------------------------------------------------
class NonLinearRequest(BaseModel):
    budget: float = Field(10.0, ge=0.1, description="Presupuesto disponible (unidades de mil, ej. 10.0 = $10,000)")
    c1: float = Field(4.0, description="Coeficiente lineal para creadores (x1)")
    c2: float = Field(5.0, description="Coeficiente lineal para anuncios programáticos (x2)")
    a1: float = Field(0.2, ge=0.0, description="Coeficiente cuadrático de saturación para creadores (x1)")
    a2: float = Field(0.3, ge=0.0, description="Coeficiente cuadrático de saturación para anuncios programáticos (x2)")

# ----------------------------------------------------
# Endpoints
# ----------------------------------------------------

@router.post("/knapsack", status_code=status.HTTP_200_OK)
def optimize_knapsack(payload: KnapsackRequest):
    """
    Resuelve el Sub-problema A: Mochila (Carga de Servidores).
    Maximiza la estabilidad total bajo restricción de RAM.
    """
    try:
        items_dict_list = [item.model_dump() for item in payload.items]
        optimizer = KnapsackOptimizer(capacity=payload.capacity, items_data=items_dict_list)
        result = optimizer.solve()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar optimización de servidores: {str(e)}"
        )

@router.post("/stagecoach", status_code=status.HTTP_200_OK)
def optimize_stagecoach(payload: StagecoachRequest):
    """
    Resuelve el Sub-problema B: Grafo por Etapas (Ruta de Latencia Mínima).
    Calcula el camino crítico mediante Programación Dinámica Backward.
    """
    try:
        # Validaciones de consistencia
        if not payload.stages[0]:
            raise HTTPException(status_code=400, detail="La primera etapa no puede estar vacía.")
        if not payload.stages[-1]:
            raise HTTPException(status_code=400, detail="La última etapa (destino) no puede estar vacía.")
            
        optimizer = StagecoachOptimizer(stages=payload.stages, connections=payload.connections)
        result = optimizer.solve()
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar enrutamiento en red: {str(e)}"
        )

@router.post("/non-linear", status_code=status.HTTP_200_OK)
def optimize_nonlinear(payload: NonLinearRequest):
    """
    Resuelve la Parte II: Optimización No Lineal (Marketing Budget).
    Asignación de presupuesto maximizando el retorno con rendimientos decrecientes.
    """
    try:
        optimizer = NonLinearOptimizer(
            budget=payload.budget,
            c1=payload.c1,
            c2=payload.c2,
            a1=payload.a1,
            a2=payload.a2
        )
        result = optimizer.solve()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al optimizar presupuesto de marketing: {str(e)}"
        )
