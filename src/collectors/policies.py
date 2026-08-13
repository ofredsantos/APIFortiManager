"""
Coletor para Requisito 9: Firewall Policies para Gerenciamento SOC
"""
from src.models.device_inventory import RequirementStatus


def collect_policies(response: dict) -> RequirementStatus:
    """
    Verifica se existem firewall policies permitindo tráfego de gerenciamento SOC.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=9,
            name="Firewall Policies SOC",
            status="❌ Ausente",
            current_config="Nenhuma firewall policy encontrada.",
            suggestion=(
                "Criar firewall policies para permitir tráfego de gerenciamento "
                "entre a zone SOC e a interface loopback_mgmt."
            ),
        )

    soc_policies = [
        p for p in data 
        if any(k in p.get("name", "").lower() for k in ("mgmt-inbound", "mgmt", "soc"))
    ]

    if soc_policies:
        policies_str = "\n".join(
            f"  - ID {p.get('policyid', 'N/A')}: {p.get('name', 'N/A')} (action: {p.get('action', 'N/A')})"
            for p in soc_policies
        )
        return RequirementStatus(
            number=9,
            name="Firewall Policy MGMT-INBOUND",
            status="✅ OK",
            current_config=f"Policies de gerenciamento encontradas:\n{policies_str}",
            suggestion="Nenhuma ação necessária. Policies já existem.",
        )
    else:
        existing = ", ".join(
            f"ID {p.get('policyid', 'N/A')}: {p.get('name', 'N/A')}"
            for p in data[:5]
        )
        return RequirementStatus(
            number=9,
            name="Firewall Policy MGMT-INBOUND",
            status="❌ Ausente",
            current_config=f"Policies existentes: {existing}",
            suggestion=(
                "Criar policy MGMT-INBOUND permitindo tráfego da zone ZN.MGMT para a loopback mgmt.algar."
            ),
        )