from typing import List, Dict, Any
from .base import BaseOptimizer

class StagecoachOptimizer(BaseOptimizer):
    """
    Resolvedor de Programación Dinámica Backward para redes organizadas por etapas.
    Encuentra la ruta crítica de menor costo (latencia) entre un nodo origen y un destino.
    """
    def __init__(self, stages: List[List[str]], connections: Dict[str, Dict[str, float]]):
        super().__init__("Stagecoach Routing Optimizer")
        self.stages = stages  # Lista de etapas, ej: [["A"], ["B","C","D"], ["E","F","G"], ["H","I"], ["J"]]
        self.connections = connections  # Grafo, ej: {"A": {"B": 4, "C": 6, "D": 3}, ...}
        self.num_stages = len(stages) - 1

    def solve(self) -> Dict[str, Any]:
        # f_optimo[(nodo)] = (costo_min, decision_optima)
        f_optimo: Dict[str, tuple] = {}
        
        # El destino final (última etapa) tiene costo 0 y decisión None
        destino_final = self.stages[-1][0]
        f_optimo[destino_final] = (0.0, None)
        
        # Estructura para guardar las tablas paso a paso de cada etapa
        # etapas_tablas[n] guardará la información de la etapa n (1-indexed)
        etapas_tablas = {}

        # Programación dinámica hacia atrás (de la última etapa a la primera)
        for n in range(self.num_stages, 0, -1):
            estados_etapa = self.stages[n - 1]
            destinos_posibles = self.stages[n]
            
            tabla_etapa = {}
            for estado in estados_etapa:
                mejor_costo = float('inf')
                mejor_decision = None
                detalles_estado = {}
                
                # Para cada estado, evaluamos todas las decisiones (destinos en la siguiente etapa)
                for destino in destinos_posibles:
                    # Validar si existe conexión
                    costo_conexion = self.connections.get(estado, {}).get(destino, None)
                    if costo_conexion is not None:
                        # Costo acumulado = Costo de conexión + Costo óptimo a partir del destino
                        costo_futuro = f_optimo.get(destino, (float('inf'), None))[0]
                        costo_total = costo_conexion + costo_futuro
                        
                        detalles_estado[destino] = costo_total
                        
                        # Buscamos el mínimo
                        if costo_total < mejor_costo:
                            mejor_costo = costo_total
                            mejor_decision = destino
                    else:
                        # Si no hay conexión, el costo es infinito o nulo
                        detalles_estado[destino] = float('inf')
                
                # Guardar el óptimo para este estado
                f_optimo[estado] = (mejor_costo, mejor_decision)
                
                # Guardar detalles para la visualización en la tabla de la etapa
                tabla_etapa[estado] = {
                    "decisiones": detalles_estado,
                    "mejor_decision": mejor_decision,
                    "mejor_costo": mejor_costo
                }
                
            etapas_tablas[n] = tabla_etapa

        # Reconstrucción de la ruta óptima desde el nodo inicial (primer estado de la etapa 1)
        nodo_inicial = self.stages[0][0]
        ruta_optima = [nodo_inicial]
        costo_total = f_optimo.get(nodo_inicial, (float('inf'), None))[0]
        
        nodo_actual = nodo_inicial
        while True:
            _, siguiente_nodo = f_optimo.get(nodo_actual, (0.0, None))
            if siguiente_nodo is None:
                break
            ruta_optima.append(siguiente_nodo)
            nodo_actual = siguiente_nodo

        # Dar formato a las tablas para el reporte PDF y el frontend
        tablas_formateadas = []
        for n in range(self.num_stages, 0, -1):
            nodos_etapa = self.stages[n - 1]
            nodos_siguientes = self.stages[n]
            
            headers = ["Estado s"] + nodos_siguientes + ["Costo f* (s)", "Decisión d*(s)"]
            rows = []
            
            for estado in nodos_etapa:
                info = etapas_tablas[n][estado]
                row = [estado]
                for sig in nodos_siguientes:
                    val = info["decisiones"].get(sig, float('inf'))
                    val_str = f"{val:.1f}" if val != float('inf') else "-"
                    row.append(val_str)
                
                row.append(f"{info['mejor_costo']:.1f}")
                row.append(str(info["mejor_decision"]))
                rows.append(row)
                
            tablas_formateadas.append({
                "etapa": n,
                "descripcion": f"Etapa {n} - Nodos {nodos_etapa} a {nodos_siguientes}",
                "headers": headers,
                "rows": rows
            })
            
        # Revertir para mostrar de Etapa 1 a Etapa N (orden de flujo)
        tablas_formateadas.reverse()

        self.result = {
            "start_node": nodo_inicial,
            "end_node": destino_final,
            "min_cost": costo_total,
            "optimal_path": ruta_optima,
            "stages_data": self.stages,
            "connections_data": self.connections,
            "step_by_step_tables": tablas_formateadas
        }
        return self.result
