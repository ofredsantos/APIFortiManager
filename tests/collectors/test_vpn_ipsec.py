"""
Testes para o coletor de VPN IPsec (Requisito 1)
"""
from src.collectors.vpn_ipsec import collect_vpn_ipsec


def test_vpn_ipsec_empty(mock_vpn_ipsec_empty):
    """Nenhum túnel IPsec configurado"""
    result = collect_vpn_ipsec("FGT-ATACAREJO-01", mock_vpn_ipsec_empty)
    assert result.number == 1
    assert result.status == "❌ Ausente"
    assert "Nenhum túnel" in result.current_config
    assert "Criar 2 túneis" in result.suggestion


def test_vpn_ipsec_with_tunnels(mock_vpn_ipsec_with_tunnels):
    """Túneis IPsec já configurados"""
    result = collect_vpn_ipsec("FGT-ATACAREJO-01", mock_vpn_ipsec_with_tunnels)
    assert result.number == 1
    assert result.status == "✅ OK"
    assert "to_soc_wan1" in result.current_config
    assert "to_soc_wan2" in result.current_config
    assert "Nenhuma ação" in result.suggestion


def test_vpn_ipsec_single_tunnel():
    """Apenas um túnel configurado (deveria ter 2)"""
    response = {
        "id": 1,
        "result": [
            {
                "data": [
                    {
                        "name": "to_soc_wan1",
                        "interface": "wan1",
                        "remote-gw": "200.200.200.1",
                    },
                ],
                "status": {"code": 0, "message": "OK"},
            }
        ],
    }
    result = collect_vpn_ipsec("FGT-ATACAREJO-01", response)
    assert result.number == 1
    assert result.status == "⚠️ Parcial"
    assert "Apenas 1 túnel" in result.current_config