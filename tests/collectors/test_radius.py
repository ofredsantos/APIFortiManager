"""
Testes para o coletor de RADIUS (Requisito 10)
"""
from src.collectors.radius import collect_radius


def test_radius_no_server(mock_radius_no_server):
    result = collect_radius(mock_radius_no_server)
    assert result.number == 10
    assert result.status == "❌ Ausente"


def test_radius_with_server(mock_radius_with_server):
    result = collect_radius(mock_radius_with_server)
    assert result.number == 10
    assert result.status == "✅ OK"