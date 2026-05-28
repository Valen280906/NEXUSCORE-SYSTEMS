from abc import ABC, abstractmethod
from typing import Dict, Any


class OptimizadorBase(ABC):
    """
    Clase base abstracta para todos los motores de optimización matemática.
    Aplica el principio de POO: cada algoritmo concreto hereda esta interfaz
    y está obligado a implementar el método 'resolver()'.
    De esta forma se garantiza una estructura coherente en todo el proyecto.
    """

    def __init__(self, nombre: str):
        # Nombre descriptivo del optimizador (para identificación en reportes)
        self.nombre: str = nombre
        # Diccionario donde se guardarán los resultados luego de invocar resolver()
        self.resultado: Dict[str, Any] = {}

    @abstractmethod
    def resolver(self) -> Dict[str, Any]:
        """
        Método abstracto que ejecuta el algoritmo de optimización.
        Cada subclase concreta debe sobreescribir este método con su lógica.
        Debe retornar un diccionario con la solución óptima y el detalle
        de los pasos seguidos.
        """
        pass

    def obtener_resultado(self) -> Dict[str, Any]:
        """
        Retorna el diccionario de resultados calculados previamente por resolver().
        """
        return self.resultado
