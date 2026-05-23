from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseOptimizer(ABC):
    """
    Clase base abstracta para los motores de optimización.
    Sigue el principio de diseño orientado a objetos para garantizar
    una interfaz común para todos los resolvedores.
    """

    def __init__(self, name: str):
        self.name = name
        self.result: Dict[str, Any] = {}

    @abstractmethod
    def solve(self) -> Dict[str, Any]:
        """
        Ejecuta el algoritmo de optimización matemática.
        Debe devolver un diccionario con la solución óptima y detalles de los pasos.
        """
        pass

    def get_result(self) -> Dict[str, Any]:
        """
        Retorna los resultados previamente calculados.
        """
        return self.result
