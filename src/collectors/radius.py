"""
Coletor para Requisito 10: Servidor RADIUS
"""
from src.models.device_inventory import RequirementStatus


def collect_radius(response: dict) -> RequirementStatus:
    """
    Verifica se existe um servidor RADIUS configurado para autenticação.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=10,
            name="Servidor RADIUS",
            status="❌ Ausente",
            current_config="Nenhum servidor RADIUS configurado.",
            suggestion=(
                "Configurar servidor RADIUS para autenticação administrativa:\n"
                "config user radius\n"
                "  edit SOC_RADIUS\n"
                "    set server <ip_radius>\n"
                "    set secret <secret>\n"
                "    set auth-type pap\n"
                "  next\nend"
            ),
        )

    # Procura por servidor RADIUS com nome relacionado ao SOC
    soc_radius = [r for r in data if "soc" in r.get("name", "").lower()]

    if soc_radius:
        radius_str = "\n".join(
            f"  - {r['name']}: server={r.get('server', 'N/A')}, "
            f"auth={r.get('auth-type', 'N/A')}"
            for r in soc_radius
        )
        return RequirementStatus(
            number=10,
            name="Servidor RADIUS",
            status="✅ OK",
            current_config=f"Servidor(es) RADIUS encontrado(s):\n{radius_str}",
            suggestion="Nenhuma ação necessária. RADIUS já configurado.",
        )
    else:
        existing = ", ".join(r.get("name", "?") for r in data) if data else "nenhum"
        return RequirementStatus(
            number=10,
            name="Servidor RADIUS",
            status="❌ Ausente",
            current_config=f"Servidores RADIUS existentes: {existing}",
            suggestion="Configurar servidor RADIUS do SOC para autenticação administrativa.",
        )