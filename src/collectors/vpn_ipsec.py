"""
Coletor para Requisito 1: Túneis VPN IPsec dedicados para o SOC
"""
from src.models.device_inventory import RequirementStatus


def collect_vpn_ipsec(device_name: str, response: dict) -> RequirementStatus:
    """
    Verifica se existem túneis VPN IPsec configurados para o SOC.

    Espera ao menos 2 túneis (um por link WAN) com nomenclatura padrão 'to_soc_*'.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=1,
            name="VPN IPsec (Túneis Dedicados)",
            status="❌ Ausente",
            current_config="Nenhum túnel IPsec encontrado ou erro na consulta.",
            suggestion=(
                "Criar 2 túneis VPN IPsec (um por link WAN) entre o FortiGate e o SOC. "
                "Utilizar nomenclatura padrão: to_soc_wan1, to_soc_wan2."
            ),
        )

    # Filtra túneis que parecem ser para o SOC (nome contendo "soc")
    soc_tunnels = [t for t in data if "soc" in t.get("name", "").lower()]

    if len(soc_tunnels) >= 2:
        names = ", ".join(t["name"] for t in soc_tunnels)
        return RequirementStatus(
            number=1,
            name="VPN IPsec (Túneis Dedicados)",
            status="✅ OK",
            current_config=(
                f"{len(soc_tunnels)} túneis SOC encontrados: {names}\n"
                + "\n".join(
                    f"  - {t['name']}: GW={t.get('remote-gw', 'N/A')}, "
                    f"Interface={t.get('interface', 'N/A')}"
                    for t in soc_tunnels
                )
            ),
            suggestion="Nenhuma ação necessária. Túneis IPsec já configurados.",
        )
    elif len(soc_tunnels) == 1:
        return RequirementStatus(
            number=1,
            name="VPN IPsec (Túneis Dedicados)",
            status="⚠️ Parcial",
            current_config=f"Apenas 1 túnel SOC encontrado: {soc_tunnels[0]['name']}",
            suggestion="Criar o segundo túnel VPN IPsec para o segundo link WAN.",
        )
    else:
        # Existem túneis, mas nenhum com nome SOC
        existing = ", ".join(t.get("name", "?") for t in data)
        return RequirementStatus(
            number=1,
            name="VPN IPsec (Túneis Dedicados)",
            status="❌ Ausente",
            current_config=f"Túneis existentes (sem padrão SOC): {existing}",
            suggestion=(
                "Criar 2 túneis VPN IPsec dedicados para o SOC com nomenclatura "
                "padrão: to_soc_wan1, to_soc_wan2."
            ),
        )