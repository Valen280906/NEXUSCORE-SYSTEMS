from typing import Dict, Any, List
from .base import BaseOptimizer

class NonLinearOptimizer(BaseOptimizer):
    """
    Resolvedor de Optimización No Lineal para la asignación de presupuesto de Marketing.
    Maximiza f(x1, x2) = c1*x1 + c2*x2 - a1*x1^2 - a2*x2^2 sujeto a x1 + x2 <= B y x1, x2 >= 0.
    """
    def __init__(self, budget: float, c1: float, c2: float, a1: float, a2: float):
        super().__init__("Non-Linear Marketing Budget Optimizer")
        self.budget = max(0.0, budget)
        self.c1 = c1
        self.c2 = c2
        self.a1 = a1
        self.a2 = a2

    def evaluate(self, x1: float, x2: float) -> float:
        """
        Evalúa la función de adquisición de usuarios f(x1, x2).
        """
        return self.c1 * x1 + self.c2 * x2 - self.a1 * (x1 ** 2) - self.a2 * (x2 ** 2)

    def solve(self) -> Dict[str, Any]:
        # 1. Calcular el máximo irrestricto (punto donde el gradiente es cero)
        # df/dx1 = c1 - 2*a1*x1 = 0 => x1 = c1 / (2*a1)
        # df/dx2 = c2 - 2*a2*x2 = 0 => x2 = c2 / (2*a2)
        
        x1_unconstrained = self.c1 / (2 * self.a1) if self.a1 != 0 else float('inf')
        x2_unconstrained = self.c2 / (2 * self.a2) if self.a2 != 0 else float('inf')
        
        val_unconstrained = self.evaluate(x1_unconstrained, x2_unconstrained) if (x1_unconstrained != float('inf') and x2_unconstrained != float('inf')) else 0.0

        # Verificar si el máximo irrestricto cumple con la restricción de presupuesto
        if x1_unconstrained >= 0 and x2_unconstrained >= 0 and (x1_unconstrained + x2_unconstrained) <= self.budget:
            x1_opt = x1_unconstrained
            x2_opt = x2_unconstrained
            is_budget_active = False
        else:
            # La restricción x1 + x2 = B está activa.
            # Sustituimos x2 = B - x1 en f(x1, x2) obteniendo g(x1).
            # g(x1) = c1*x1 + c2*(B - x1) - a1*x1^2 - a2*(B - x1)^2
            # Tomamos la derivada g'(x1) = 0:
            # g'(x1) = c1 - c2 - 2*a1*x1 + 2*a2*(B - x1) = 0
            # c1 - c2 + 2*a2*B - 2*(a1 + a2)*x1 = 0
            # x1 = (c1 - c2 + 2*a2*B) / (2*(a1 + a2))
            denominador = 2 * (self.a1 + self.a2)
            if denominador != 0:
                x1_candidate = (self.c1 - self.c2 + 2 * self.a2 * self.budget) / denominador
                # Proyectamos al intervalo válido [0, B]
                x1_opt = max(0.0, min(self.budget, x1_candidate))
                x2_opt = self.budget - x1_opt
            else:
                x1_opt = 0.0
                x2_opt = self.budget
            is_budget_active = True

        max_val = self.evaluate(x1_opt, x2_opt)

        # 2. Generar puntos de la curva para graficar en el frontend (visualización del comportamiento)
        # Realizamos un escaneo de 50 puntos sobre la frontera de presupuesto para graficar g(x1)
        chart_points = []
        steps = 50
        for i in range(steps + 1):
            x1_val = (self.budget / steps) * i
            x2_val = self.budget - x1_val
            y_val = self.evaluate(x1_val, x2_val)
            chart_points.append({
                "x1": round(x1_val, 2),
                "x2": round(x2_val, 2),
                "acquisition": round(y_val, 3)
            })

        self.result = {
            "budget": self.budget,
            "coefficients": {
                "c1": self.c1,
                "c2": self.c2,
                "a1": self.a1,
                "a2": self.a2
            },
            "unconstrained_optimum": {
                "x1": round(x1_unconstrained, 4) if x1_unconstrained != float('inf') else "inf",
                "x2": round(x2_unconstrained, 4) if x2_unconstrained != float('inf') else "inf",
                "value": round(val_unconstrained, 4)
            },
            "constrained_optimum": {
                "x1": round(x1_opt, 4),
                "x2": round(x2_opt, 4),
                "value": round(max_val, 4)
            },
            "is_budget_active": is_budget_active,
            "chart_points": chart_points
        }
        return self.result
