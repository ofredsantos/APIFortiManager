"""
Coletor para Requisito 2: Rotas Estáticas para o SOC
"""
from src.models.device_inventory import RequirementStatus


def collect_routes(device_name: str, response: dict) -> RequirementStatus:
    """
    Verifica se existem rotas estáticas apontando para os túneis SOC.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="❌ Ausente",
            current_config="Nenhuma rota estática encontrada.",
            suggestion=(
                "Criar rotas estáticas para as redes do SOC apontando para os túneis "
                "IPsec (to_soc_wan1, to_soc_wan2)."
            ),
        )

    # Filtra rotas que usam túneis de gerência (VPN.MGMT / SOC) ou apontam para sub-redes Algar (198.19.*)
    def _is_mgmt_route(route: dict) -> bool:
        device = route.get("device", "")
        dst = str(route.get("dst", ""))
        dev_str = ""
        if isinstance(device, list):
            dev_str = " ".join(str(d) for d in device).lower()
        else:
            dev_str = str(device).lower()

        is_mgmt_dev = any(k in dev_str for k in ("vpn.mgmt", "soc", "mgmt"))
        is_mgmt_dst = dst.startswith("198.19.") or "198.19." in dst
        return is_mgmt_dev or is_mgmt_dst

    soc_routes = [r for r in data if _is_mgmt_route(r)]

    if len(soc_routes) >= 1:
        routes_str = "\n".join(
            f"  - {r.get('dst', 'N/A')} → {r.get('device', 'N/A')} (GW: {r.get('gateway', 'N/A')})"
            for r in soc_routes
        )
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="✅ OK",
            current_config=f"{len(soc_routes)} rotas de gerenciamento encontradas:\n{routes_str}",
            suggestion="Nenhuma ação necessária. Rotas estáticas já configuradas.",
        )
    else:
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="❌ Ausente",
            current_config="Nenhuma rota para túneis de gerência (VPN.MGMT) encontrada.",
            suggestion=(
                "Criar rotas estáticas para as redes de gerência (198.19.0.0/26 e 198.19.255.0/24) "
                "apontando para os túneis VPN.MGMT.01 (priority 50) e VPN.MGMT.02 (priority 60)."
            ),
        )