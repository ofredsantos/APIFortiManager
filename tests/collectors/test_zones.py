"""
Testes para o coletor de Zones (Requisito 7)
"""
from src.collectors.zones import collect_zones


def test_zones_no_soc(mock_zones_no_soc):
    result = collect_zones(mock_zones_no_soc)
    assert result.number == 7
    assert result.status == "❌ Ausente"


def test_zones_with_soc(mock_zones_with_soc):
    result = collect_zones(mock_zones_with_soc)
    assert result.number == 7
    assert result.status == "✅ OK"