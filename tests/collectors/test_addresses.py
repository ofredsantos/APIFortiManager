"""
Testes para o coletor de Address Objects (Requisito 8)
"""
from src.collectors.addresses import collect_addresses


def test_addresses_no_soc(mock_addresses_no_soc):
    result = collect_addresses(mock_addresses_no_soc)
    assert result.number == 8
    assert result.status == "❌ Ausente"


def test_addresses_with_soc(mock_addresses_with_soc):
    result = collect_addresses(mock_addresses_with_soc)
    assert result.number == 8
    assert result.status == "✅ OK"