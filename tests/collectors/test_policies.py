"""
Testes para o coletor de Firewall Policies (Requisito 9)
"""
from src.collectors.policies import collect_policies


def test_policies_no_mgmt(mock_policies_no_mgmt):
    result = collect_policies(mock_policies_no_mgmt)
    assert result.number == 9
    assert result.status == "❌ Ausente"


def test_policies_with_mgmt(mock_policies_with_mgmt):
    result = collect_policies(mock_policies_with_mgmt)
    assert result.number == 9
    assert result.status == "✅ OK"