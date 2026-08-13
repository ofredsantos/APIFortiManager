"""
Coletor para Requisito 7: Zone para Túneis SOC
"""
from src.models.device_inventory import RequirementStatus


def collect_zones(response: dict) -> RequirementStatus:
    """
    Verifica se existe uma zone 'SOC' contendo os túneis IPsec.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=7,
            name="Zone SOC",
            status="❌ Ausente",
            current_config="Nenhuma zone encontrada.",
            suggestion=(
                "Criar zone 'SOC' e associar os túneis IPsec:\n"
                "config system zone\n"
                "  edit SOC\n"
                "    set interface to_soc_wan1 to_soc_wan2\n"
                "  next\nend"
            ),
        )

    soc_zone = [
        z for z in data 
        if z.get("name", "").lower() in ("zn.mgmt", "soc", "mgmt")
    ]

    if soc_zone:
        interfaces = soc_zone[0].get("interface", [])
        if isinstance(interfaces, list) and len(interfaces) >= 1:
            return RequirementStatus(
                number=7,
                name="Zone ZN.MGMT / SOC",
                status="✅ OK",
                current_config=(
                    f"Zone '{soc_zone[0].get('name')}' encontrada com interfaces: {', '.join(interfaces)}"
                ),
                suggestion="Nenhuma ação necessária. Zone já configurada.",
            )
        else:
            return RequirementStatus(
                number=7,
                name="Zone ZN.MGMT / SOC",
                status="⚠️ Parcial",
                current_config=f"Zone '{soc_zone[0].get('name')}' existe mas sem interfaces associadas.",
                suggestion="Associar as interfaces de túnel IPsec (VPN.MGMT.01/02) à zone.",
            )
    else:
        existing = ", ".join(z.get("name", "?") for z in data)
        return RequirementStatus(
            number=7,
            name="Zone ZN.MGMT / SOC",
            status="❌ Ausente",
            current_config=f"Zones existentes: {existing}",
            suggestion="Criar zone 'ZN.MGMT' com as interfaces de túnel associadas.",
        )