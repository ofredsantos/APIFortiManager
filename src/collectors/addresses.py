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

    soc_addresses = [a for a in data if "soc" in a.get("name", "").lower()]

    if len(soc_addresses) >= 2:
        addrs_str = "\n".join(
            f"  - {a['name']}: {a.get('subnet', 'N/A')}"
            for a in soc_addresses
        )
        return RequirementStatus(
            number=8,
            name="Address Objects SOC",
            status="✅ OK",
            current_config=f"Address objects SOC encontrados:\n{addrs_str}",
            suggestion="Nenhuma ação necessária. Address objects já existem.",
        )
    elif len(soc_addresses) == 1:
        return RequirementStatus(
            number=8,
            name="Address Objects SOC",
            status="⚠️ Parcial",
            current_config=f"Apenas 1 address SOC: {soc_addresses[0]['name']}",
            suggestion="Criar address objects adicionais para a infraestrutura do SOC.",
        )
    else:
        existing = ", ".join(a.get("name", "?") for a in data[:5])
        return RequirementStatus(
            number=8,
            name="Address Objects SOC",
            status="❌ Ausente",
            current_config=f"Addresses existentes (sem SOC): {existing}",
            suggestion="Criar address objects para comunicação com o SOC.",
        )