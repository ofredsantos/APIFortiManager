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

    # Filtra rotas que usam túneis SOC
    def _device_contains_soc(route: dict) -> bool:
        device = route.get("device", "")
        if isinstance(device, list):
            return any("soc" in d.lower() for d in device if isinstance(d, str))
        return "soc" in str(device).lower()

    soc_routes = [r for r in data if _device_contains_soc(r)]

    if len(soc_routes) >= 2:
        routes_str = "\n".join(
            f"  - {r['dst']} → {r['device']} (GW: {r.get('gateway', 'N/A')})"
            for r in soc_routes
        )
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="✅ OK",
            current_config=f"{len(soc_routes)} rotas SOC encontradas:\n{routes_str}",
            suggestion="Nenhuma ação necessária. Rotas estáticas já configuradas.",
        )
    elif len(soc_routes) == 1:
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="⚠️ Parcial",
            current_config=f"Apenas 1 rota SOC encontrada: {soc_routes[0]['dst']}",
            suggestion="Criar a segunda rota estática para o segundo túnel SOC.",
        )
    else:
        return RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="❌ Ausente",
            current_config="Nenhuma rota para túneis SOC encontrada.",
            suggestion=(
                "Criar rotas estáticas para as redes do SOC (ex: 10.10.0.0/16) "
                "apontando para os túneis IPsec to_soc_wan1 e to_soc_wan2."
            ),
        )