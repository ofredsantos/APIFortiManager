"""
Coletores para Requisitos 5 e 6: Interface Loopback e Nomenclatura de Túneis
"""
from src.models.device_inventory import RequirementStatus


def collect_loopback(response: dict) -> RequirementStatus:
    """
    Verifica se existe uma interface loopback dedicada para gerenciamento.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=5,
            name="Interface Loopback",
            status="❌ Ausente",
            current_config="Nenhuma interface encontrada.",
            suggestion=(
                "Criar interface loopback dedicada para gerenciamento:\n"
                "config system interface\n"
                "  edit loopback_mgmt\n"
                "    set type loopback\n"
                "    set ip 172.16.0.1/32\n"
                "    set allowaccess ping\n"
                "  next\nend"
            ),
        )

    loopbacks = [i for i in data if i.get("type") == "loopback"]

    if loopbacks:
        lb_str = "\n".join(
            f"  - {lb['name']}: {lb.get('ip', 'N/A')}"
            for lb in loopbacks
        )
        return RequirementStatus(
            number=5,
            name="Interface Loopback",
            status="✅ OK",
            current_config=f"Loopback(s) encontrado(s):\n{lb_str}",
            suggestion="Nenhuma ação necessária. Loopback já configurada.",
        )
    else:
        return RequirementStatus(
            number=5,
            name="Interface Loopback",
            status="❌ Ausente",
            current_config="Nenhuma interface loopback encontrada.",
            suggestion="Criar interface loopback_mgmt para serviços de gerenciamento.",
        )


def collect_tunnel_naming(response: dict) -> RequirementStatus:
    """
    Verifica se os túneis IPsec seguem o padrão de nomenclatura 'to_soc_*'.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=6,
            name="Nomenclatura de Túneis",
            status="❌ Ausente",
            current_config="Nenhuma interface túnel encontrada.",
            suggestion=(
                "Padronizar nomenclatura dos túneis IPsec: to_soc_wan1, to_soc_wan2."
            ),
        )

    tunnels = [i for i in data if i.get("type") == "tunnel"]
    soc_tunnels = [t for t in tunnels if t["name"].startswith("to_soc_")]

    if not tunnels:
        return RequirementStatus(
            number=6,
            name="Nomenclatura de Túneis",
            status="❌ Ausente",
            current_config="Nenhuma interface túnel encontrada.",
            suggestion="Criar túneis com nomenclatura padrão: to_soc_wan1, to_soc_wan2.",
        )

    if len(soc_tunnels) == len(tunnels) and len(soc_tunnels) >= 2:
        names = ", ".join(t["name"] for t in soc_tunnels)
        return RequirementStatus(
            number=6,
            name="Nomenclatura de Túneis",
            status="✅ OK",
            current_config=f"Túneis no padrão: {names}",
            suggestion="Nenhuma ação necessária. Nomenclatura já padronizada.",
        )
    else:
        current = ", ".join(t["name"] for t in tunnels)
        return RequirementStatus(
            number=6,
            name="Nomenclatura de Túneis",
            status="❌ Ausente",
            current_config=f"Túneis atuais: {current}",
            suggestion=(
                "Renomear túneis para o padrão: to_soc_wan1, to_soc_wan2."
            ),
        )