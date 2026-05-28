from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Importar los optimizadores desde el paquete de algoritmos
from ..algorithms.knapsack    import OptimizadorMochila
from ..algorithms.stage_coach import OptimizadorRutaPorEtapas
from ..algorithms.optimizador_no_lineal  import OptimizadorNoLineal

# Router con prefijo "/optimizar" y etiqueta visible en la documentación de la API
enrutador = APIRouter(
    prefix="/optimizar",
    tags=["Motores de Optimización Matemática"]
)

# ============================================================
# MODELOS PYDANTIC — Validación de los datos de entrada
# ============================================================

class EntradaMicroservicio(BaseModel):
    """Modelo de un microservicio individual enviado por el usuario."""
    id:     int   = Field(..., description="Identificador único del microservicio")
    nombre: str   = Field(..., description="Nombre descriptivo del microservicio")
    peso:   int   = Field(..., gt=0, description="Requisito de RAM en GB (debe ser > 0)")
    valor:  int   = Field(..., ge=0, description="Valor de prioridad de estabilidad (≥ 0)")


class SolicitudMochila(BaseModel):
    """Parámetros de entrada para el problema de Carga de Servidores (Mochila 0/1)."""
    capacidad:  int                      = Field(16, ge=1, le=128, description="Capacidad máxima de RAM del servidor en GB")
    elementos:  List[EntradaMicroservicio] = Field(..., min_items=1, description="Lista de microservicios candidatos")


class SolicitudRutaEtapas(BaseModel):
    """Parámetros de entrada para el enrutamiento por etapas (DP Backward)."""
    etapas:    List[List[str]]            = Field(
        ..., min_items=2,
        description="Lista de etapas ordenadas. Ej: [['A'], ['B','C'], ['D']]"
    )
    conexiones: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Grafo de latencias. Estructura: {nodo_origen: {nodo_destino: costo_ms}}"
    )


class SolicitudNoLineal(BaseModel):
    """Parámetros de entrada para la optimización no lineal de presupuesto de marketing."""
    presupuesto: float = Field(10.0, ge=0.1, description="Presupuesto máximo disponible (en miles de $)")
    c1:          float = Field(4.0,           description="Coeficiente lineal para Creadores de Contenido (x1)")
    c2:          float = Field(5.0,           description="Coeficiente lineal para Anuncios Programáticos (x2)")
    a1:          float = Field(0.2, ge=0.0,   description="Coeficiente cuadrático de saturación para x1")
    a2:          float = Field(0.3, ge=0.0,   description="Coeficiente cuadrático de saturación para x2")


# ============================================================
# ENDPOINTS DE LA API
# ============================================================

@enrutador.post("/mochila", status_code=status.HTTP_200_OK)
def optimizar_mochila(solicitud: SolicitudMochila):
    """
    Resuelve el Sub-problema A: Carga de Servidores (Mochila 0/1).
    Maximiza el valor de estabilidad del sistema bajo la restricción de RAM del servidor.
    """
    try:
        # Convertir la lista de modelos Pydantic a lista de diccionarios
        lista_elementos = [elem.model_dump() for elem in solicitud.elementos]

        # Instanciar y ejecutar el optimizador
        optimizador = OptimizadorMochila(
            capacidad=solicitud.capacidad,
            datos_elementos=lista_elementos
        )
        resultado = optimizador.resolver()
        return resultado

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la Mochila de Servidores: {str(error)}"
        )


@enrutador.post("/ruta-etapas", status_code=status.HTTP_200_OK)
def optimizar_ruta_etapas(solicitud: SolicitudRutaEtapas):
    """
    Resuelve el Sub-problema B: Red de Distribución de Datos (DP Backward).
    Calcula el camino crítico de menor latencia acumulada entre el nodo origen y destino.
    """
    try:
        # Validaciones básicas de la estructura de etapas
        if not solicitud.etapas[0]:
            raise HTTPException(status_code=400, detail="La primera etapa no puede estar vacía.")
        if not solicitud.etapas[-1]:
            raise HTTPException(status_code=400, detail="La última etapa (destino) no puede estar vacía.")

        # Instanciar el optimizador (la validación de conectividad ocurre dentro de resolver())
        optimizador = OptimizadorRutaPorEtapas(
            etapas=solicitud.etapas,
            conexiones=solicitud.conexiones
        )
        resultado = optimizador.resolver()
        return resultado

    except HTTPException as exc_http:
        # Re-lanzar errores HTTP explícitos (como 400)
        raise exc_http
    except ValueError as exc_val:
        # Errores de validación de conectividad generados por el algoritmo
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc_val))
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al calcular la ruta crítica por etapas: {str(error)}"
        )


@enrutador.post("/no-lineal", status_code=status.HTTP_200_OK)
def optimizar_no_lineal(solicitud: SolicitudNoLineal):
    """
    Resuelve la Parte II: Optimización No Lineal de Presupuesto de Marketing.
    Aplica derivación parcial, Método de Lagrange y Método de Gradiente.
    """
    try:
        # Instanciar y ejecutar el optimizador no lineal
        optimizador = OptimizadorNoLineal(
            presupuesto=solicitud.presupuesto,
            c1=solicitud.c1,
            c2=solicitud.c2,
            a1=solicitud.a1,
            a2=solicitud.a2
        )
        resultado = optimizador.resolver()
        return resultado

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al optimizar el presupuesto de marketing: {str(error)}"
        )
