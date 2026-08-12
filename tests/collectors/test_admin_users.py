"""
Testes para o coletor de Admin Users (Requisito 4)
"""
from src.collectors.admin_users import collect_admin_users


def test_admin_users_no_standard(mock_admin_users_no_standard):
    result = collect_admin_users(mock_admin_users_no_standard)
    assert result.number == 4
    assert result.status == "❌ Ausente"


def test_admin_users_with_standard(mock_admin_users_with_standard):
    result = collect_admin_users(mock_admin_users_with_standard)
    assert result.number == 4
    assert result.status == "✅ OK"