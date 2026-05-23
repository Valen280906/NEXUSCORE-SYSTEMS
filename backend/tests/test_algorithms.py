import pytest
from app.algorithms.knapsack import KnapsackOptimizer
from app.algorithms.stage_coach import StagecoachOptimizer
from app.algorithms.non_linear import NonLinearOptimizer

def test_knapsack_optimizer():
    """
    Verifica que el resolvedor de la mochila 0/1 maximice correctamente la estabilidad
    utilizando los datos del problema académico (Capacidad: 16 GB).
    """
    capacity = 16
    items = [
        {"id": 1, "name": "Autenticación", "weight": 3, "value": 5},
        {"id": 2, "name": "Matchmaking", "weight": 4, "value": 7},
        {"id": 3, "name": "Estado", "weight": 7, "value": 11},
        {"id": 4, "name": "Caché", "weight": 5, "value": 8}
    ]
    
    optimizer = KnapsackOptimizer(capacity=capacity, items_data=items)
    result = optimizer.solve()
    
    # La solución óptima es seleccionar Matchmaking, Estado y Caché
    # RAM utilizada: 4 + 7 + 5 = 16 GB
    # Estabilidad total: 7 + 11 + 8 = 26
    assert result["max_value"] == 26
    assert result["used_weight"] == 16
    
    selected_names = [item["name"] for item in result["selected_items"]]
    assert "Matchmaking" in selected_names
    assert "Estado" in selected_names
    assert "Caché" in selected_names
    assert "Autenticación" not in selected_names

def test_stagecoach_optimizer():
    """
    Verifica que el resolvedor por etapas encuentre el camino crítico de menor latencia
    según los datos del problema del PDF (Latencia mínima = 16.0 ms).
    """
    stages = [
        ["A"],
        ["B", "C", "D"],
        ["E", "F", "G"],
        ["H", "I"],
        ["J"]
    ]
    
    connections = {
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
    
    optimizer = StagecoachOptimizer(stages=stages, connections=connections)
    result = optimizer.solve()
    
    # Latencia mínima óptima = 16.0 ms
    assert result["min_cost"] == 16.0
    
    # Los caminos óptimos válidos son:
    # A -> B -> F -> H -> J (4 + 5 + 3 + 4 = 16)
    # A -> D -> F -> H -> J (3 + 6 + 3 + 4 = 16)
    path = result["optimal_path"]
    assert path[0] == "A"
    assert path[-1] == "J"
    assert path == ["A", "B", "F", "H", "J"] or path == ["A", "D", "F", "H", "J"]

def test_non_linear_optimizer():
    """
    Verifica que el resolvedor no lineal asigne el presupuesto de marketing óptimo
    exactamente en el punto óptimo analítico (B=10 => x1=5, x2=5, Retorno=32.5).
    """
    budget = 10.0
    c1, c2 = 4.0, 5.0
    a1, a2 = 0.2, 0.3
    
    optimizer = NonLinearOptimizer(budget=budget, c1=c1, c2=c2, a1=a1, a2=a2)
    result = optimizer.solve()
    
    opt = result["constrained_optimum"]
    assert pytest.approx(opt["x1"], 0.01) == 5.0
    assert pytest.approx(opt["x2"], 0.01) == 5.0
    assert pytest.approx(opt["value"], 0.01) == 32.5
    assert result["is_budget_active"] is True
