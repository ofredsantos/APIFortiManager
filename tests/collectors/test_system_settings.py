"""
Testes para o coletor de System Settings (Requisitos 12 e 13)
"""
from src.collectors.system_settings import collect_admintimeout, collect_sync_status


def test_admintimeout_default(mock_system_global_default):
    result = collect_admintimeout(mock_system_global_default)
    assert result.number == 12
    assert result.status == "❌ Ausente"


def test_admintimeout_standard(mock_system_global_standard):
    result = collect_admintimeout(mock_system_global_standard)
    assert result.number == 12
    assert result.status == "✅ OK"


def test_sync_status_ok(mock_sync_status_ok):
    result = collect_sync_status(mock_sync_status_ok)
    assert result.number == 13
    assert result.status == "✅ OK"


def test_sync_status_out_of_sync(mock_sync_status_out_of_sync):
    result = collect_sync_status(mock_sync_status_out_of_sync)
    assert result.number == 13
    assert result.status == "❌ Ausente"