"""
Testes para o coletor de Rotas Estáticas (Requisito 2)
"""
from src.collectors.routes import collect_routes


def test_routes_empty(mock_routes_empty):
    result = collect_routes("FGT-ATACAREJO-01", mock_routes_empty)
    assert result.number == 2
    assert result.status == "❌ Ausente"


def test_routes_with_soc(mock_routes_with_soc):
    result = collect_routes("FGT-ATACAREJO-01", mock_routes_with_soc)
    assert result.number == 2
    assert result.status == "✅ OK"
    assert "10.10.0.0/16" in result.current_config