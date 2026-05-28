from typing import Dict, Any, List
from .base import OptimizadorBase


class OptimizadorNoLineal(OptimizadorBase):
    """
    Resuelve la Parte II (Presupuesto de Marketing) mediante Optimización No Lineal.

    Problema:
        Maximizar:  f(x1, x2) = c1·x1 + c2·x2 - a1·x1² - a2·x2²
        Sujeto a:   x1 + x2 ≤ B    (restricción de presupuesto)
                    x1, x2 ≥ 0     (no negatividad)

    Donde x1 = inversión en Creadores de Contenido y x2 = inversión en Anuncios Programáticos.
    La función es cuadrática (cóncava) gracias a los términos -a1·x1² y -a2·x2², que modelan
    la saturación del mercado (rendimientos marginales decrecientes).

    Se implementan tres técnicas del contenido programático de la unidad:
      1. Derivación Parcial  → Puntos estacionarios (máximo irrestricto)
      2. Método de Lagrange  → Multiplicadores de Lagrange con restricción activa
      3. Método de Gradiente → Ascenso de gradiente proyectado (iterativo)

    Hereda de OptimizadorBase e implementa el método resolver().
    """

    def __init__(self, presupuesto: float, c1: float, c2: float, a1: float, a2: float):
        super().__init__("Optimizador No Lineal - Presupuesto de Marketing")
        # Presupuesto total disponible en miles de $ (ej: 10.0 = $10,000)
        self.presupuesto = max(0.0, presupuesto)
        # Coeficiente lineal de la campaña de Creadores de Contenido (x1)
        self.c1 = c1
        # Coeficiente lineal de los Anuncios Programáticos (x2)
        self.c2 = c2
        # Coeficiente cuadrático de saturación para Creadores (x1)
        self.a1 = a1
        # Coeficiente cuadrático de saturación para Anuncios (x2)
        self.a2 = a2

    def evaluar(self, x1: float, x2: float) -> float:
        """
        Evalúa la función objetivo f(x1, x2) en el punto (x1, x2).
        Representa la adquisición mensual de usuarios (en miles de jugadores).
        """
        return self.c1 * x1 + self.c2 * x2 - self.a1 * (x1 ** 2) - self.a2 * (x2 ** 2)

    def metodo_lagrange(self) -> Dict[str, Any]:
        """
        Resuelve la optimización con la restricción activa (x1 + x2 = B)
        usando el Método de Multiplicadores de Lagrange.

        Planteamiento formal:
            Lagrangiano: L(x1, x2, λ) = f(x1,x2) - λ·g(x1,x2)
                         donde g(x1,x2) = x1 + x2 - B (restricción de igualdad)

        Condiciones de Primer Orden (KKT para igualdad activa):
            ∂L/∂x1 = c1 - 2·a1·x1 - λ = 0  →  x1* = (c1 - λ) / (2·a1)
            ∂L/∂x2 = c2 - 2·a2·x2 - λ = 0  →  x2* = (c2 - λ) / (2·a2)
            ∂L/∂λ  = -(x1 + x2 - B)  = 0   →  x1 + x2 = B

        Sustituyendo x1* y x2* en la restricción x1 + x2 = B:
            (c1 - λ)/(2·a1) + (c2 - λ)/(2·a2) = B
            Despejando λ:
            λ = [(c1/(2·a1) + c2/(2·a2)) - B] / [1/(2·a1) + 1/(2·a2)]
        """
        # Verificar que los coeficientes cuadráticos sean distintos de cero
        if self.a1 == 0 or self.a2 == 0:
            return {"error": "Los coeficientes a1 y a2 deben ser > 0 para aplicar Lagrange."}

        # ---- PASO 1: Calcular el multiplicador de Lagrange λ ----
        numerador_lam   = (self.c1 / (2 * self.a1) + self.c2 / (2 * self.a2)) - self.presupuesto
        denominador_lam = 1 / (2 * self.a1) + 1 / (2 * self.a2)
        lambda_val      = numerador_lam / denominador_lam

        # ---- PASO 2: Calcular x1* y x2* con la restricción activa ----
        x1_lagrange = (self.c1 - lambda_val) / (2 * self.a1)
        x2_lagrange = (self.c2 - lambda_val) / (2 * self.a2)

        # ---- PASO 3: Proyectar al dominio factible [0, B] ----
        x1_lagrange = max(0.0, min(self.presupuesto, x1_lagrange))
        x2_lagrange = self.presupuesto - x1_lagrange

        # ---- PASO 4: Evaluar la función objetivo en el punto Lagrange ----
        valor_lagrange = self.evaluar(x1_lagrange, x2_lagrange)

        return {
            "multiplicador_lambda": round(lambda_val, 6),
            "x1_optimo":            round(x1_lagrange, 4),
            "x2_optimo":            round(x2_lagrange, 4),
            "valor_optimo":         round(valor_lagrange, 4),
            "interpretacion": (
                f"λ = {lambda_val:.4f}: Por cada unidad adicional de presupuesto B, "
                f"el valor óptimo f* aumenta aproximadamente {lambda_val:.4f} miles de usuarios."
            ),
            "pasos_detalle": {
                "lagrangiano":       f"L = {self.c1}x₁ + {self.c2}x₂ - {self.a1}x₁² - {self.a2}x₂² - λ(x₁ + x₂ - {self.presupuesto})",
                "condicion_x1":     f"∂L/∂x₁ = {self.c1} - {2*self.a1}x₁ - λ = 0  →  x₁* = ({self.c1} - λ) / {2*self.a1}",
                "condicion_x2":     f"∂L/∂x₂ = {self.c2} - {2*self.a2}x₂ - λ = 0  →  x₂* = ({self.c2} - λ) / {2*self.a2}",
                "condicion_lambda":  f"∂L/∂λ = -(x₁ + x₂ - {self.presupuesto}) = 0  →  x₁ + x₂ = {self.presupuesto}",
                "calculo_lambda":    f"λ = {round(numerador_lam,4)} / {round(denominador_lam,4)} = {round(lambda_val,4)}"
            }
        }

    def metodo_gradiente(
        self,
        tasa_aprendizaje: float = 0.01,
        max_iteraciones:  int   = 1000,
        tolerancia:       float = 1e-6
    ) -> Dict[str, Any]:
        """
        Resuelve el problema mediante Ascenso de Gradiente Proyectado (iterativo).

        Algoritmo:
            1. Iniciar en el punto central: x1 = x2 = B/2
            2. Calcular el gradiente ∇f:
               ∂f/∂x1 = c1 - 2·a1·x1
               ∂f/∂x2 = c2 - 2·a2·x2
            3. Actualizar posición: x1 += α·∂f/∂x1 ;  x2 += α·∂f/∂x2
            4. Proyectar sobre el dominio factible {x1+x2 ≤ B, x1,x2 ≥ 0}
            5. Repetir hasta que ||∇f|| < tolerancia o se alcancen max_iteraciones.

        Retorna la trayectoria de convergencia para su visualización.
        """
        # Punto de inicio: centro del presupuesto
        x1 = self.presupuesto / 2.0
        x2 = self.presupuesto / 2.0

        historial: List[Dict] = []  # Guarda la trayectoria de convergencia
        num_iter  = 0
        convergido = False

        for num_iter in range(max_iteraciones):
            # ---- Calcular derivadas parciales (componentes del gradiente) ----
            grad_x1 = self.c1 - 2 * self.a1 * x1   # ∂f/∂x1
            grad_x2 = self.c2 - 2 * self.a2 * x2   # ∂f/∂x2
            norma_gradiente = (grad_x1 ** 2 + grad_x2 ** 2) ** 0.5

            # Registrar en historial (primeras 10 iteraciones y luego cada 50)
            if num_iter < 10 or num_iter % 50 == 0:
                historial.append({
                    "iteracion":       num_iter,
                    "x1":              round(x1, 4),
                    "x2":              round(x2, 4),
                    "valor":           round(self.evaluar(x1, x2), 4),
                    "norma_gradiente": round(norma_gradiente, 6)
                })

            # ---- Verificar criterio de convergencia ----
            if norma_gradiente < tolerancia:
                convergido = True
                break

            # ---- Paso de ascenso de gradiente ----
            x1_nuevo = x1 + tasa_aprendizaje * grad_x1
            x2_nuevo = x2 + tasa_aprendizaje * grad_x2

            # ---- Proyección sobre el dominio factible ----
            # Garantizar no negatividad
            x1_nuevo = max(0.0, x1_nuevo)
            x2_nuevo = max(0.0, x2_nuevo)

            # Si se viola la restricción de presupuesto, proyectar sobre la frontera
            if x1_nuevo + x2_nuevo > self.presupuesto:
                proporcion = self.presupuesto / (x1_nuevo + x2_nuevo)
                x1_nuevo  *= proporcion
                x2_nuevo  *= proporcion

            x1 = x1_nuevo
            x2 = x2_nuevo

        # Agregar el punto final al historial
        historial.append({
            "iteracion":       num_iter,
            "x1":              round(x1, 4),
            "x2":              round(x2, 4),
            "valor":           round(self.evaluar(x1, x2), 4),
            "norma_gradiente": 0.0
        })

        return {
            "x1_optimo":          round(x1, 4),
            "x2_optimo":          round(x2, 4),
            "valor_optimo":       round(self.evaluar(x1, x2), 4),
            "iteraciones_totales": num_iter + 1,
            "convergido":          convergido,
            "tasa_aprendizaje":    tasa_aprendizaje,
            "historial":           historial
        }

    def resolver(self) -> Dict[str, Any]:
        """
        Orquesta los tres métodos de optimización no lineal y retorna
        los resultados consolidados de cada técnica.

        Flujo:
            1. Derivación Parcial  → Hallar el punto estacionario irrestricto
            2. Restricción activa  → Verificar si la restricción presupuestaria es activa
            3. Método de Lagrange  → Resolver con multiplicadores λ (si la restricción es activa)
            4. Método de Gradiente → Ascenso iterativo proyectado (siempre)
            5. Puntos de gráfica   → Curva g(x1) sobre la frontera del presupuesto
        """
        # ----------------------------------------------------------------
        # PASO 1: Derivación Parcial — Máximo Irrestricto (Punto Estacionario)
        # ∂f/∂x1 = c1 - 2·a1·x1 = 0  →  x1* = c1 / (2·a1)
        # ∂f/∂x2 = c2 - 2·a2·x2 = 0  →  x2* = c2 / (2·a2)
        # ----------------------------------------------------------------
        x1_irrestricto = self.c1 / (2 * self.a1) if self.a1 != 0 else float('inf')
        x2_irrestricto = self.c2 / (2 * self.a2) if self.a2 != 0 else float('inf')

        # Evaluar la función en el punto irrestricto (si es finito)
        if x1_irrestricto != float('inf') and x2_irrestricto != float('inf'):
            valor_irrestricto = self.evaluar(x1_irrestricto, x2_irrestricto)
        else:
            valor_irrestricto = 0.0

        # ----------------------------------------------------------------
        # PASO 2: Verificar si la restricción presupuestaria es activa
        # ----------------------------------------------------------------
        restriccion_activa = not (
            x1_irrestricto >= 0 and
            x2_irrestricto >= 0 and
            (x1_irrestricto + x2_irrestricto) <= self.presupuesto
        )

        # ----------------------------------------------------------------
        # PASO 3: Calcular el óptimo bajo la restricción activa (sustitución)
        # Si x1 + x2 = B → x2 = B - x1 → sustituir en f(x1, B-x1) = g(x1)
        # g'(x1) = c1 - c2 + 2·a2·B - 2·(a1+a2)·x1 = 0
        # ----------------------------------------------------------------
        if not restriccion_activa:
            # El máximo irrestricto es factible: usarlo directamente
            x1_optimo = x1_irrestricto
            x2_optimo = x2_irrestricto
        else:
            # Despejar x1 de la condición g'(x1) = 0
            denominador = 2 * (self.a1 + self.a2)
            if denominador != 0:
                x1_candidato = (self.c1 - self.c2 + 2 * self.a2 * self.presupuesto) / denominador
                # Proyectar al intervalo [0, B] para garantizar factibilidad
                x1_optimo = max(0.0, min(self.presupuesto, x1_candidato))
                x2_optimo = self.presupuesto - x1_optimo
            else:
                # Caso degenerado: sin solución analítica diferenciada
                x1_optimo = 0.0
                x2_optimo = self.presupuesto

        valor_optimo = self.evaluar(x1_optimo, x2_optimo)

        # ----------------------------------------------------------------
        # PASO 4: Método de Lagrange (solo si la restricción está activa)
        # ----------------------------------------------------------------
        if restriccion_activa:
            resultado_lagrange = self.metodo_lagrange()
        else:
            resultado_lagrange = {
                "multiplicador_lambda": 0.0,
                "nota": (
                    "La restricción presupuestaria NO está activa. "
                    "El óptimo irrestricto es factible y coincide con el máximo global."
                )
            }

        # ----------------------------------------------------------------
        # PASO 5: Método de Gradiente Proyectado (iterativo, siempre se ejecuta)
        # ----------------------------------------------------------------
        resultado_gradiente = self.metodo_gradiente()

        # ----------------------------------------------------------------
        # PASO 6: Generar puntos para graficar g(x1) en la frontera del presupuesto
        # Se evalúa f(x1, B-x1) para x1 ∈ [0, B] con 50 puntos
        # ----------------------------------------------------------------
        puntos_grafica = []
        num_puntos = 50
        for i in range(num_puntos + 1):
            x1_val = (self.presupuesto / num_puntos) * i
            x2_val = self.presupuesto - x1_val
            puntos_grafica.append({
                "x1":          round(x1_val, 2),
                "x2":          round(x2_val, 2),
                "adquisicion": round(self.evaluar(x1_val, x2_val), 3)
            })

        # ----------------------------------------------------------------
        # Guardar y retornar el resultado completo
        # ----------------------------------------------------------------
        self.resultado = {
            "presupuesto":   self.presupuesto,
            "coeficientes":  {"c1": self.c1, "c2": self.c2, "a1": self.a1, "a2": self.a2},
            "optimo_irrestricto": {
                "x1":    round(x1_irrestricto, 4) if x1_irrestricto != float('inf') else "inf",
                "x2":    round(x2_irrestricto, 4) if x2_irrestricto != float('inf') else "inf",
                "valor": round(valor_irrestricto, 4)
            },
            "optimo_restringido": {
                "x1":    round(x1_optimo, 4),
                "x2":    round(x2_optimo, 4),
                "valor": round(valor_optimo, 4)
            },
            "restriccion_activa": restriccion_activa,
            "metodo_lagrange":    resultado_lagrange,
            "metodo_gradiente":   resultado_gradiente,
            "puntos_grafica":     puntos_grafica
        }
        return self.resultado
