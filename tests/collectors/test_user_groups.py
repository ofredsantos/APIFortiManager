"""
Testes para o coletor de User Groups (Requisito 11)
"""
from src.collectors.user_groups import collect_user_groups


def test_user_groups_no_radius(mock_user_groups_no_radius):
    result = collect_user_groups(mock_user_groups_no_radius)
    assert result.number == 11
    assert result.status == "❌ Ausente"


def test_user_groups_with_radius(mock_user_groups_with_radius):
    result = collect_user_groups(mock_user_groups_with_radius)
    assert result.number == 11
    assert result.status == "✅ OK"