"""
Coletor para Requisito 8: Address Objects do SOC
"""
from src.models.device_inventory import RequirementStatus


def collect_addresses(response: dict) -> RequirementStatus:
    """
    Verifica se existem address objects para a infraestrutura do SOC.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=8,
            name="Address Objects SOC",
            status="❌ Ausente",
            current_config="Nenhum address object encontrado.",
            suggestion=(
                "Criar address objects para a infraestrutura do SOC:\n"
                "- SOC_NETWORK (rede do SOC)\n"
                "- SOC_MGMT_IP (IP de gerenciamento)\n"
                "- etc."
            ),
        )

    soc_addresses = [
        a for a in data 
        if any(k in a.get("name", "").lower() for k in ("mgmt.dc", "mgmt.spoke", "soc"))
    ]

    if len(soc_addresses) >= 1:
        addrs_str = "\n".join(
            f"  - {a['name']}: {a.get('subnet', 'N/A')}"
            for a in soc_addresses
        )
        return RequirementStatus(
            number=8,
            name="Address Objects Gerenciamento",
            status="✅ OK",
            current_config=f"Address objects de gerenciamento encontrados:\n{addrs_str}",
            suggestion="Nenhuma ação necessária. Address objects já existem.",
        )
    else:
        existing = ", ".join(a.get("name", "?") for a in data[:5])
        return RequirementStatus(
            number=8,
            name="Address Objects Gerenciamento",
            status="❌ Ausente",
            current_config=f"Addresses existentes: {existing}",
            suggestion="Criar os objetos de endereço: MGMT.DC (198.19.0.0/26), MGMT.DC-2 (198.19.255.0/24) e MGMT.SPOKE.",
        )