"""
Testes para o coletor de Accprofile (Requisito 3)
"""
from src.collectors.accprofile import collect_accprofile


def test_accprofile_no_api(mock_accprofile_no_api):
    result = collect_accprofile(mock_accprofile_no_api)
    assert result.number == 3
    assert result.status == "❌ Ausente"


def test_accprofile_with_api(mock_accprofile_with_api):
    result = collect_accprofile(mock_accprofile_with_api)
    assert result.number == 3
    assert result.status == "✅ OK"