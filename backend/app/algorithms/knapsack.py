from typing import List, Dict, Any
from .base import BaseOptimizer

class Microservice:
    """
    Clase que representa un microservicio crítico a desplegar.
    """
    def __init__(self, id: int, name: str, weight: int, value: int):
        self.id = id
        self.name = name
        self.weight = weight  # Requisito de RAM (wi)
        self.value = value    # Valor de Prioridad de Estabilidad (vi)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "weight": self.weight,
            "value": self.value
        }

class KnapsackOptimizer(BaseOptimizer):
    """
    Resolvedor de Programación Dinámica para el Problema de la Carga de Servidores.
    Maximiza el valor de estabilidad sujeto a un límite de capacidad de RAM (Mochila 0/1).
    """
    def __init__(self, capacity: int, items_data: List[Dict[str, Any]]):
        super().__init__("Knapsack Server Loading Optimizer")
        self.capacity = max(0, capacity)
        self.items = [
            Microservice(
                id=item.get("id", idx + 1),
                name=item.get("name", f"Microservicio {idx + 1}"),
                weight=max(1, int(item.get("weight", 1))),
                value=max(0, int(item.get("value", 0)))
            )
            for idx, item in enumerate(items_data)
        ]

    def solve(self) -> Dict[str, Any]:
        n = len(self.items)
        # Inicializar tabla de DP de dimensiones (n + 1) x (capacity + 1)
        # dp[i][w] guardará el valor óptimo usando los primeros i elementos con capacidad w
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]

        # Llenar la matriz de DP
        for i in range(1, n + 1):
            item = self.items[i - 1]
            for w in range(self.capacity + 1):
                if item.weight <= w:
                    dp[i][w] = max(
                        dp[i - 1][w],
                        dp[i - 1][w - item.weight] + item.value
                    )
                else:
                    dp[i][w] = dp[i - 1][w]

        # Reconstrucción del conjunto óptimo (Traceback)
        selected_items = []
        w = self.capacity
        for i in range(n, 0, -1):
            # Si el valor cambió en la fila, significa que incluimos el elemento i-1
            if dp[i][w] != dp[i - 1][w]:
                item = self.items[i - 1]
                selected_items.append(item)
                w -= item.weight

        # Revertir la lista para conservar el orden original
        selected_items.reverse()

        # Preparar la matriz paso a paso legible para el reporte y frontend
        # Filas representarán la etapa (incorporación de microservicio i)
        # Columnas serán la capacidad de 0 a capacity
        table_rows = []
        for i in range(n + 1):
            row_label = "Estado Inicial" if i == 0 else f"{self.items[i - 1].name} (+{self.items[i - 1].weight}GB, V:{self.items[i - 1].value})"
            table_rows.append({
                "row_label": row_label,
                "values": dp[i]
            })

        self.result = {
            "capacity": self.capacity,
            "total_items": n,
            "max_value": dp[n][self.capacity],
            "used_weight": sum(item.weight for item in selected_items),
            "selected_items": [item.to_dict() for item in selected_items],
            "step_by_step_table": {
                "headers": [f"{w} GB" for w in range(self.capacity + 1)],
                "rows": table_rows
            }
        }
        return self.result
