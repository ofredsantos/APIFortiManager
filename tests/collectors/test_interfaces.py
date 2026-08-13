"""
Testes para o coletor de Interfaces (Requisitos 5 e 6)
"""
from src.collectors.interfaces import collect_loopback, collect_tunnel_naming


def test_loopback_empty(mock_interfaces_no_loopback):
    result = collect_loopback(mock_interfaces_no_loopback)
    assert result.number == 5
    assert result.status == "❌ Ausente"


def test_loopback_with(mock_interfaces_with_loopback):
    result = collect_loopback(mock_interfaces_with_loopback)
    assert result.number == 5
    assert result.status == "✅ OK"


def test_tunnels_wrong_names(mock_tunnels_wrong_names):
    result = collect_tunnel_naming(mock_tunnels_wrong_names)
    assert result.number == 6
    assert result.status == "❌ Ausente"


def test_tunnels_standard_names(mock_tunnels_standard_names):
    result = collect_tunnel_naming(mock_tunnels_standard_names)
    assert result.number == 6
    assert result.status == "✅ OK"