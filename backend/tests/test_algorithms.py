import pytest
from app.algorithms.knapsack    import OptimizadorMochila
from app.algorithms.stage_coach import OptimizadorRutaPorEtapas
from app.algorithms.optimizador_no_lineal  import OptimizadorNoLineal

def test_optimizador_mochila():
    """
    Verifica que el resolvedor de la mochila 0/1 maximice correctamente la estabilidad
    utilizando los datos del problema académico (Capacidad: 16 GB).
    """
    capacidad = 16
    elementos = [
        {"id": 1, "nombre": "Autenticación", "peso": 3, "valor": 5},
        {"id": 2, "nombre": "Matchmaking",   "peso": 4, "valor": 7},
        {"id": 3, "nombre": "Estado",        "peso": 7, "valor": 11},
        {"id": 4, "nombre": "Caché",         "peso": 5, "valor": 8}
    ]

    optimizador = OptimizadorMochila(capacidad=capacidad, datos_elementos=elementos)
    resultado = optimizador.resolver()

    # La solución óptima es seleccionar Matchmaking, Estado y Caché
    # RAM utilizada: 4 + 7 + 5 = 16 GB
    # Estabilidad total: 7 + 11 + 8 = 26
    assert resultado["valor_maximo"]   == 26
    assert resultado["peso_utilizado"] == 16

    nombres_seleccionados = [item["nombre"] for item in resultado["elementos_elegidos"]]
    assert "Matchmaking"   in nombres_seleccionados
    assert "Estado"        in nombres_seleccionados
    assert "Caché"         in nombres_seleccionados
    assert "Autenticación" not in nombres_seleccionados


def test_optimizador_ruta_etapas():
    """
    Verifica que el resolvedor por etapas encuentre el camino crítico de menor latencia
    según los datos del problema del PDF (Latencia mínima = 16.0 ms).
    """
    etapas = [
        ["A"],
        ["B", "C", "D"],
        ["E", "F", "G"],
        ["H", "I"],
        ["J"]
    ]

    conexiones = {
        "A": {"B": 4, "C": 6, "D": 3},
        "B": {"E": 7, "F": 5},
        "C": {"E": 3, "F": 8, "G": 4},
        "D": {"F": 6, "G": 9},
        "E": {"H": 5, "I": 6},
        "F": {"H": 3, "I": 5},
        "G": {"H": 8, "I": 2},
        "H": {"J": 4},
        "I": {"J": 7}
    }

    optimizador = OptimizadorRutaPorEtapas(etapas=etapas, conexiones=conexiones)
    resultado = optimizador.resolver()

    # Latencia mínima óptima = 16.0 ms
    assert resultado["costo_minimo"] == 16.0

    # Los caminos óptimos válidos son:
    # A -> B -> F -> H -> J (4 + 5 + 3 + 4 = 16)
    # A -> D -> F -> H -> J (3 + 6 + 3 + 4 = 16)
    ruta = resultado["ruta_optima"]
    assert ruta[0]  == "A"
    assert ruta[-1] == "J"
    assert ruta == ["A", "B", "F", "H", "J"] or ruta == ["A", "D", "F", "H", "J"]


def test_optimizador_no_lineal():
    """
    Verifica que el resolvedor no lineal asigne el presupuesto de marketing óptimo
    exactamente en el punto óptimo analítico (B=10 => x1=5, x2=5, Retorno=32.5).
    """
    presupuesto = 10.0
    c1, c2 = 4.0, 5.0
    a1, a2 = 0.2, 0.3

    optimizador = OptimizadorNoLineal(presupuesto=presupuesto, c1=c1, c2=c2, a1=a1, a2=a2)
    resultado = optimizador.resolver()

    opt = resultado["optimo_restringido"]
    assert pytest.approx(opt["x1"], 0.01)    == 5.0
    assert pytest.approx(opt["x2"], 0.01)    == 5.0
    assert pytest.approx(opt["valor"], 0.01) == 32.5
    assert resultado["restriccion_activa"] is True
