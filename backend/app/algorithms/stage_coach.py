from typing import List, Dict, Any, Tuple
from .base import OptimizadorBase


class OptimizadorRutaPorEtapas(OptimizadorBase):
    """
    Resuelve el Sub-problema B (Red de Distribución de Datos) mediante
    Programación Dinámica Backward (hacia atrás).

    Recorre la red etapa por etapa desde el nodo destino hasta el nodo origen,
    calculando en cada estado el costo óptimo restante f*(s) y la decisión
    óptima d*(s) que lo alcanza. Al finalizar, reconstruye la ruta de menor
    latencia total.

    Hereda de OptimizadorBase e implementa el método resolver().
    """

    def __init__(self, etapas: List[List[str]], conexiones: Dict[str, Dict[str, float]]):
        super().__init__("Optimizador de Ruta por Etapas - DP Backward")
        # Lista ordenada de etapas: cada etapa es una lista de nodos (ej: [["A"],["B","C"],["D"]])
        self.etapas    = etapas
        # Grafo dirigido de latencias: {nodo_origen: {nodo_destino: costo_ms}}
        self.conexiones = conexiones
        # Número de transiciones entre etapas consecutivas
        self.num_etapas = len(etapas) - 1

    def validar_conectividad(self) -> Tuple[bool, str]:
        """
        Verifica que la topología de la red sea mínimamente válida para
        poder calcular el camino crítico de manera correcta.

        Reglas que se validan:
          1. Deben existir al menos 2 etapas (origen y destino).
          2. Cada nodo en una etapa debe tener al menos una conexión
             hacia algún nodo de la etapa siguiente.

        Retorna:
          - (True, "")                → La red es válida.
          - (False, mensaje_error)    → Hay un problema en la conectividad.
        """
        # Verificar cantidad mínima de etapas
        if len(self.etapas) < 2:
            return False, "La red debe tener al menos 2 etapas (origen y destino)."

        # Verificar que cada nodo (excepto los del último nivel) tenga salida válida
        for idx_etapa in range(self.num_etapas):
            nodos_origen   = self.etapas[idx_etapa]
            nodos_destino  = self.etapas[idx_etapa + 1]

            for nodo in nodos_origen:
                # Buscar si existe al menos una arista válida hacia la siguiente etapa
                tiene_conexion_valida = any(
                    self.conexiones.get(nodo, {}).get(destino) is not None
                    for destino in nodos_destino
                )
                if not tiene_conexion_valida:
                    return False, (
                        f"El nodo '{nodo}' (Etapa {idx_etapa + 1}) no tiene conexiones "
                        f"hacia la Etapa {idx_etapa + 2}. Verifique la topología de la red."
                    )

        return True, ""

    def resolver(self) -> Dict[str, Any]:
        """
        Ejecuta la Programación Dinámica Backward para hallar la ruta de menor costo.

        Algoritmo (Etapa por Etapa, de atrás hacia adelante):
            1. f*(nodo_destino) = 0  (costo desde el final hasta sí mismo es 0)
            2. Para cada etapa n (desde la última hasta la primera):
               f*(s) = min  { costo(s → d) + f*(d) }
                       d ∈ etapa_n+1
            3. Reconstruir la ruta óptima siguiendo las decisiones d*(s).
        """
        # Validar la conectividad de la red antes de resolver
        es_valida, mensaje_error = self.validar_conectividad()
        if not es_valida:
            raise ValueError(f"Red no válida para el algoritmo: {mensaje_error}")

        # f_optimo[nodo] = (costo_minimo_hasta_destino, mejor_decision_desde_nodo)
        f_optimo: Dict[str, Tuple[float, Any]] = {}

        # El nodo destino (último de la última etapa) tiene costo 0 y no hay decisión posterior
        nodo_destino = self.etapas[-1][0]
        f_optimo[nodo_destino] = (0.0, None)

        # Tabla de datos por etapa para el reporte y el frontend
        tablas_por_etapa: Dict[int, Dict] = {}

        # ----------------------------------------------------------------
        # RECORRIDO BACKWARD: desde la penúltima etapa hasta la primera
        # ----------------------------------------------------------------
        for num_etapa in range(self.num_etapas, 0, -1):
            nodos_actuales   = self.etapas[num_etapa - 1]  # Nodos de la etapa actual
            nodos_siguientes = self.etapas[num_etapa]       # Nodos de la siguiente etapa

            tabla_etapa: Dict[str, Dict] = {}

            for nodo in nodos_actuales:
                # Inicializar con valores "imposibles"
                mejor_costo    = float('inf')
                mejor_decision = None
                costos_por_destino: Dict[str, float] = {}

                # Evaluar cada decisión posible (aristas hacia nodos de la siguiente etapa)
                for destino in nodos_siguientes:
                    costo_arista = self.conexiones.get(nodo, {}).get(destino)

                    if costo_arista is not None:
                        # Costo acumulado = latencia de la arista + costo óptimo futuro
                        costo_futuro = f_optimo.get(destino, (float('inf'), None))[0]
                        costo_total  = costo_arista + costo_futuro
                        costos_por_destino[destino] = costo_total

                        # Actualizar el mínimo si encontramos un camino mejor
                        if costo_total < mejor_costo:
                            mejor_costo    = costo_total
                            mejor_decision = destino
                    else:
                        # Sin arista disponible: costo infinito (nodo inaccesible)
                        costos_por_destino[destino] = float('inf')

                # Guardar el resultado óptimo para este nodo
                f_optimo[nodo] = (mejor_costo, mejor_decision)
                tabla_etapa[nodo] = {
                    "costos_por_destino": costos_por_destino,
                    "mejor_decision":     mejor_decision,
                    "costo_optimo":       mejor_costo
                }

            tablas_por_etapa[num_etapa] = tabla_etapa

        # ----------------------------------------------------------------
        # RECONSTRUCCIÓN DE LA RUTA ÓPTIMA (Forward desde el origen)
        # ----------------------------------------------------------------
        nodo_inicial = self.etapas[0][0]
        ruta_optima  = [nodo_inicial]
        costo_total  = f_optimo.get(nodo_inicial, (float('inf'), None))[0]

        nodo_actual = nodo_inicial
        while True:
            # Seguir la cadena de decisiones óptimas
            _, siguiente = f_optimo.get(nodo_actual, (0.0, None))
            if siguiente is None:
                break
            ruta_optima.append(siguiente)
            nodo_actual = siguiente

        # ----------------------------------------------------------------
        # FORMATEAR TABLAS para el reporte (en orden normal: Etapa 1 → N)
        # ----------------------------------------------------------------
        tablas_formateadas = []
        for num_etapa in range(self.num_etapas, 0, -1):
            nodos_etapa      = self.etapas[num_etapa - 1]
            nodos_siguientes = self.etapas[num_etapa]

            # Encabezados: [Estado s, nodos siguientes, f*(s), d*(s)]
            encabezados = (
                ["Estado s"]
                + nodos_siguientes
                + ["f*(s) Costo Óptimo", "d*(s) Decisión"]
            )

            filas = []
            for nodo in nodos_etapa:
                info = tablas_por_etapa[num_etapa][nodo]
                fila = [nodo]

                # Agregar el costo hacia cada nodo siguiente (o "-" si no hay conexión)
                for sig in nodos_siguientes:
                    val = info["costos_por_destino"].get(sig, float('inf'))
                    fila.append(f"{val:.1f}" if val != float('inf') else "-")

                fila.append(f"{info['costo_optimo']:.1f}")
                fila.append(str(info["mejor_decision"]))
                filas.append(fila)

            tablas_formateadas.append({
                "etapa":        num_etapa,
                "descripcion":  f"Etapa {num_etapa} — Nodos {nodos_etapa} → {nodos_siguientes}",
                "encabezados":  encabezados,
                "filas":        filas
            })

        # Las tablas están en orden Backward; invertimos para mostrar de Etapa 1 a N
        tablas_formateadas.reverse()

        # ----------------------------------------------------------------
        # Guardar y retornar el resultado completo
        # ----------------------------------------------------------------
        self.resultado = {
            "nodo_inicial":       nodo_inicial,
            "nodo_destino":       nodo_destino,
            "costo_minimo":       costo_total,
            "ruta_optima":        ruta_optima,
            "etapas_datos":       self.etapas,
            "conexiones_datos":   self.conexiones,
            "tablas_paso_a_paso": tablas_formateadas
        }
        return self.resultado
