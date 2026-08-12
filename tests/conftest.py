"""
Fixtures e dados mockados para os testes dos coletores.
Simula respostas da API JSON RPC do FortiManager.
"""
import pytest


# ─── Dados mockados de devices ───────────────────────────────────────────────

@pytest.fixture
def mock_devices_response():
    """Resposta mockada de /dvmdb/device"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {
                        "name": "FGT-ATACAREJO-01",
                        "serial": "FG1K5C3XY1234567",
                        "hostname": "fgt-atacarejo-01",
                        "version": "FOS 7.4.0",
                        "platform": "FortiGate-100F",
                        "adom": "DOM_ATACAREJO",
                    },
                    {
                        "name": "FGT-ATACAREJO-02",
                        "serial": "FG1K5C3XY7654321",
                        "hostname": "fgt-atacarejo-02",
                        "version": "FOS 7.4.0",
                        "platform": "FortiGate-60F",
                        "adom": "DOM_ATACAREJO",
                    },
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/dvmdb/device",
            }
        ],
    }


# ─── Dados mockados para VPN IPsec (Requisito 1) ────────────────────────────

@pytest.fixture
def mock_vpn_ipsec_empty():
    """Nenhum túnel IPsec configurado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/vpn/ipsec/phase1-interface",
            }
        ],
    }


@pytest.fixture
def mock_vpn_ipsec_with_tunnels():
    """Túneis IPsec já configurados"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {
                        "name": "to_soc_wan1",
                        "interface": "wan1",
                        "remote-gw": "200.200.200.1",
                        "peertype": "any",
                        "proposal": "aes128-sha256",
                        "dpd": "on-demand",
                        "auto-negotiate": "enable",
                    },
                    {
                        "name": "to_soc_wan2",
                        "interface": "wan2",
                        "remote-gw": "200.200.200.2",
                        "peertype": "any",
                        "proposal": "aes128-sha256",
                        "dpd": "on-demand",
                        "auto-negotiate": "enable",
                    },
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/vpn/ipsec/phase1-interface",
            }
        ],
    }


# ─── Dados mockados para Rotas Estáticas (Requisito 2) ──────────────────────

@pytest.fixture
def mock_routes_empty():
    """Nenhuma rota estática para SOC"""
    return {
        "id": 1,
        "result": [
            {
                "data": [],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/vdom/root/router/static",
            }
        ],
    }


@pytest.fixture
def mock_routes_with_soc():
    """Rotas estáticas para SOC já configuradas"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {
                        "dst": "10.10.0.0/16",
                        "gateway": "10.99.0.1",
                        "device": "to_soc_wan1",
                        "status": "enable",
                    },
                    {
                        "dst": "10.20.0.0/16",
                        "gateway": "10.99.0.2",
                        "device": "to_soc_wan2",
                        "status": "enable",
                    },
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/vdom/root/router/static",
            }
        ],
    }


# ─── Dados mockados para Accprofile (Requisito 3) ───────────────────────────

@pytest.fixture
def mock_accprofile_no_api():
    """Nenhum perfil 'API' encontrado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "super_admin", "scope": "vdom"},
                    {"name": "read_only", "scope": "vdom"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/cli/global/system/accprofile",
            }
        ],
    }


@pytest.fixture
def mock_accprofile_with_api():
    """Perfil 'API' já existe"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "super_admin", "scope": "vdom"},
                    {"name": "API", "scope": "vdom"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/cli/global/system/accprofile",
            }
        ],
    }


# ─── Dados mockados para Admin Users (Requisito 4) ──────────────────────────

@pytest.fixture
def mock_admin_users_no_standard():
    """Nenhum admin padrão Algar encontrado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "admin", "accprofile": "super_admin"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/cli/global/system/admin",
            }
        ],
    }


@pytest.fixture
def mock_admin_users_with_standard():
    """Admins padrão Algar já existem"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "admin", "accprofile": "super_admin"},
                    {"name": "algar_ops", "accprofile": "super_admin"},
                    {"name": "algar_soc", "accprofile": "read_only"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/cli/global/system/admin",
            }
        ],
    }


# ─── Dados mockados para Interface Loopback (Requisito 5) ───────────────────

@pytest.fixture
def mock_interfaces_no_loopback():
    """Nenhuma interface loopback configurada"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "wan1", "type": "physical", "ip": "10.0.0.1/24"},
                    {"name": "wan2", "type": "physical", "ip": "10.0.1.1/24"},
                    {"name": "internal", "type": "physical", "ip": "192.168.1.1/24"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/interface",
            }
        ],
    }


@pytest.fixture
def mock_interfaces_with_loopback():
    """Loopback já configurada"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "wan1", "type": "physical", "ip": "10.0.0.1/24"},
                    {"name": "loopback_mgmt", "type": "loopback", "ip": "172.16.0.1/32"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/interface",
            }
        ],
    }


# ─── Dados mockados para Nomenclatura de Túneis (Requisito 6) ───────────────

@pytest.fixture
def mock_tunnels_wrong_names():
    """Túneis com nomes fora do padrão"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "VPN_CLIENTE", "type": "tunnel"},
                    {"name": "VPN_BACKUP", "type": "tunnel"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/interface",
            }
        ],
    }


@pytest.fixture
def mock_tunnels_standard_names():
    """Túneis com nomes no padrão Algar"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "to_soc_wan1", "type": "tunnel"},
                    {"name": "to_soc_wan2", "type": "tunnel"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/interface",
            }
        ],
    }


# ─── Dados mockados para Zone (Requisito 7) ─────────────────────────────────

@pytest.fixture
def mock_zones_no_soc():
    """Nenhuma zone SOC configurada"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "LAN", "interface": ["internal"]},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/zone",
            }
        ],
    }


@pytest.fixture
def mock_zones_with_soc():
    """Zone SOC já configurada com túneis"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "LAN", "interface": ["internal"]},
                    {"name": "SOC", "interface": ["to_soc_wan1", "to_soc_wan2"]},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/zone",
            }
        ],
    }


# ─── Dados mockados para Address Objects (Requisito 8) ──────────────────────

@pytest.fixture
def mock_addresses_no_soc():
    """Nenhum address object do SOC"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "LAN_SUBNET", "subnet": "192.168.1.0/24"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/adom/DOM_ATACAREJO/obj/firewall/address",
            }
        ],
    }


@pytest.fixture
def mock_addresses_with_soc():
    """Address objects do SOC já existem"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "LAN_SUBNET", "subnet": "192.168.1.0/24"},
                    {"name": "SOC_NETWORK", "subnet": "10.10.0.0/16"},
                    {"name": "SOC_MGMT_IP", "subnet": "10.10.0.1/32"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/adom/DOM_ATACAREJO/obj/firewall/address",
            }
        ],
    }


# ─── Dados mockados para Firewall Policies (Requisito 9) ────────────────────

@pytest.fixture
def mock_policies_no_mgmt():
    """Nenhuma policy de gerenciamento SOC"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"policyid": 1, "name": "LAN_ACCESS", "action": "accept"},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/adom/DOM_ATACAREJO/pkg/default/firewall/policy",
            }
        ],
    }


@pytest.fixture
def mock_policies_with_mgmt():
    """Policies de gerenciamento SOC já existem"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"policyid": 1, "name": "LAN_ACCESS", "action": "accept"},
                    {"policyid": 10, "name": "SOC_MGMT", "action": "accept",
                     "srcintf": ["SOC"], "dstintf": ["loopback_mgmt"]},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/adom/DOM_ATACAREJO/pkg/default/firewall/policy",
            }
        ],
    }


# ─── Dados mockados para RADIUS (Requisito 10) ──────────────────────────────

@pytest.fixture
def mock_radius_no_server():
    """Nenhum servidor RADIUS configurado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/user/radius",
            }
        ],
    }


@pytest.fixture
def mock_radius_with_server():
    """Servidor RADIUS já configurado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {
                        "name": "SOC_RADIUS",
                        "server": "10.10.0.10",
                        "secret": "********",
                        "auth-type": "pap",
                        "nas-ip": "172.16.0.1",
                    }
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/user/radius",
            }
        ],
    }


# ─── Dados mockados para User Groups (Requisito 11) ─────────────────────────

@pytest.fixture
def mock_user_groups_no_radius():
    """Nenhum grupo RADIUS configurado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "Guest_Users", "member": [{"name": "guest"}]},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/user/group",
            }
        ],
    }


@pytest.fixture
def mock_user_groups_with_radius():
    """Grupo RADIUS já configurado"""
    return {
        "id": 1,
        "result": [
            {
                "data": [
                    {"name": "Guest_Users", "member": [{"name": "guest"}]},
                    {"name": "SOC_Admins", "member": [{"name": "SOC_RADIUS"}]},
                ],
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/user/group",
            }
        ],
    }


# ─── Dados mockados para admintimeout (Requisito 12) ────────────────────────

@pytest.fixture
def mock_system_global_default():
    """admintimeout no valor padrão (240)"""
    return {
        "id": 1,
        "result": [
            {
                "data": {
                    "admintimeout": 240,
                    "hostname": "fgt-atacarejo-01",
                },
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/global",
            }
        ],
    }


@pytest.fixture
def mock_system_global_standard():
    """admintimeout já no padrão Algar (480)"""
    return {
        "id": 1,
        "result": [
            {
                "data": {
                    "admintimeout": 480,
                    "hostname": "fgt-atacarejo-01",
                },
                "status": {"code": 0, "message": "OK"},
                "url": "/pm/config/device/FGT-ATACAREJO-01/global/system/global",
            }
        ],
    }


# ─── Dados mockados para Sync Status (Requisito 13) ─────────────────────────

@pytest.fixture
def mock_sync_status_ok():
    """Device sincronizado"""
    return {
        "id": 1,
        "result": [
            {
                "data": {
                    "db_status": "in_sync",
                    "mgmt_mode": "fmg",
                },
                "status": {"code": 0, "message": "OK"},
                "url": "/dvmdb/device/FGT-ATACAREJO-01",
            }
        ],
    }


@pytest.fixture
def mock_sync_status_out_of_sync():
    """Device fora de sincronia"""
    return {
        "id": 1,
        "result": [
            {
                "data": {
                    "db_status": "out_of_sync",
                    "mgmt_mode": "fmg",
                },
                "status": {"code": 0, "message": "OK"},
                "url": "/dvmdb/device/FGT-ATACAREJO-01",
            }
        ],
    }