from typing import List, Dict, Any
from .base import OptimizadorBase


class Microservicio:
    """
    Clase que modela un microservicio crítico candidato a desplegarse en el servidor maestro.
    Cada instancia representa un elemento del problema de la Mochila 0/1:
      - peso  → Requisito de RAM en GB (wi)
      - valor → Valor de Prioridad de Estabilidad del sistema (vi)
    """

    def __init__(self, id: int, nombre: str, peso: int, valor: int):
        # Identificador único del microservicio
        self.id     = id
        # Nombre descriptivo del servicio
        self.nombre = nombre
        # Requisito de RAM que consume (en GB)
        self.peso   = peso
        # Valor de estabilidad que aporta al sistema
        self.valor  = valor

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa el microservicio a un diccionario JSON-compatible para el reporte."""
        return {
            "id":     self.id,
            "nombre": self.nombre,
            "peso":   self.peso,
            "valor":  self.valor
        }


class OptimizadorMochila(OptimizadorBase):
    """
    Resuelve el Sub-problema A (Carga de Servidores) mediante Programación Dinámica.
    Algoritmo de la Mochila 0/1: decide qué microservicios incluir para maximizar
    el valor total de estabilidad sin exceder la capacidad de RAM del servidor maestro.

    Hereda de OptimizadorBase e implementa el método resolver().
    """

    def __init__(self, capacidad: int, datos_elementos: List[Dict[str, Any]]):
        super().__init__("Optimizador de Carga de Servidores - Mochila 0/1")
        # Capacidad máxima de RAM del servidor en GB (mínimo 0 para evitar negativos)
        self.capacidad = max(0, capacidad)

        # Construir la lista de objetos Microservicio validando y normalizando los datos de entrada
        # Se aceptan tanto claves en español (nombre/peso/valor) como en inglés (name/weight/value)
        # para mantener compatibilidad durante la transición
        self.elementos: List[Microservicio] = [
            Microservicio(
                id     = elem.get("id",     idx + 1),
                nombre = elem.get("nombre", elem.get("name", f"Microservicio {idx + 1}")),
                peso   = max(1, int(elem.get("peso",  elem.get("weight", 1)))),
                valor  = max(0, int(elem.get("valor", elem.get("value",  0))))
            )
            for idx, elem in enumerate(datos_elementos)
        ]

    def resolver(self) -> Dict[str, Any]:
        """
        Ejecuta el algoritmo de Programación Dinámica (Mochila 0/1).

        Recurrencia de Bellman:
            Si peso_i <= w:
                tabla_dp[i][w] = max(tabla_dp[i-1][w],  tabla_dp[i-1][w-peso_i] + valor_i)
            Si peso_i > w:
                tabla_dp[i][w] = tabla_dp[i-1][w]

        Al terminar, tabla_dp[n][capacidad] contiene el valor de estabilidad máximo alcanzable.
        """
        num_elementos = len(self.elementos)

        # ----------------------------------------------------------------
        # PASO 1: Inicializar la tabla DP de dimensiones (n+1) x (capacidad+1)
        # tabla_dp[i][w] = valor óptimo usando los primeros i elementos con capacidad w GB
        # ----------------------------------------------------------------
        tabla_dp = [
            [0 for _ in range(self.capacidad + 1)]
            for _ in range(num_elementos + 1)
        ]

        # ----------------------------------------------------------------
        # PASO 2: Llenar la tabla aplicando la recurrencia de Bellman
        # ----------------------------------------------------------------
        for i in range(1, num_elementos + 1):
            elem = self.elementos[i - 1]
            for w in range(self.capacidad + 1):
                if elem.peso <= w:
                    # OPCIÓN A: incluir el elemento → tomamos el mejor de incluirlo o no
                    # OPCIÓN B: no incluir el elemento → heredamos el valor anterior
                    tabla_dp[i][w] = max(
                        tabla_dp[i - 1][w],                              # No incluir
                        tabla_dp[i - 1][w - elem.peso] + elem.valor      # Incluir
                    )
                else:
                    # El elemento pesa más de lo que queda de capacidad: no puede incluirse
                    tabla_dp[i][w] = tabla_dp[i - 1][w]

        # ----------------------------------------------------------------
        # PASO 3: Reconstrucción del conjunto óptimo (Traceback o Rastreo)
        # Recorremos la tabla de abajo hacia arriba para identificar qué elementos se eligieron
        # ----------------------------------------------------------------
        seleccionados: List[Microservicio] = []
        capacidad_restante = self.capacidad

        for i in range(num_elementos, 0, -1):
            # Si el valor cambió en la fila i respecto a i-1, el elemento i-1 fue incluido
            if tabla_dp[i][capacidad_restante] != tabla_dp[i - 1][capacidad_restante]:
                elem = self.elementos[i - 1]
                seleccionados.append(elem)
                capacidad_restante -= elem.peso  # Reducir la capacidad disponible

        # Invertir para mostrar en orden de incorporación (de arriba hacia abajo)
        seleccionados.reverse()

        # ----------------------------------------------------------------
        # PASO 4: Formatear la tabla DP paso a paso para el reporte y el frontend
        # Cada fila corresponde a la incorporación de un microservicio adicional
        # ----------------------------------------------------------------
        filas_tabla = []
        for i in range(num_elementos + 1):
            if i == 0:
                etiqueta = "Estado Inicial (sin microservicios)"
            else:
                elem = self.elementos[i - 1]
                etiqueta = f"{elem.nombre} (+{elem.peso}GB, V:{elem.valor})"

            filas_tabla.append({
                "etiqueta_fila": etiqueta,
                "valores":       tabla_dp[i]   # Lista de valores para w = 0..capacidad
            })

        # ----------------------------------------------------------------
        # Guardar y retornar el resultado completo
        # ----------------------------------------------------------------
        self.resultado = {
            "capacidad":          self.capacidad,
            "total_elementos":    num_elementos,
            "valor_maximo":       tabla_dp[num_elementos][self.capacidad],
            "peso_utilizado":     sum(e.peso for e in seleccionados),
            "elementos_elegidos": [e.a_diccionario() for e in seleccionados],
            "tabla_paso_a_paso": {
                "encabezados": [f"{w} GB" for w in range(self.capacidad + 1)],
                "filas":       filas_tabla
            }
        }
        return self.resultado
