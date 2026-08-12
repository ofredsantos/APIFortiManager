"""
Coletor para Requisito 11: User Groups para Autenticação RADIUS
"""
from src.models.device_inventory import RequirementStatus


def collect_user_groups(response: dict) -> RequirementStatus:
    """
    Verifica se existe um user group utilizando o servidor RADIUS do SOC.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=11,
            name="User Groups RADIUS",
            status="❌ Ausente",
            current_config="Nenhum user group encontrado.",
            suggestion=(
                "Criar user group para autenticação RADIUS:\n"
                "config user group\n"
                "  edit SOC_Admins\n"
                "    set member SOC_RADIUS\n"
                "  next\nend"
            ),
        )

    # Procura grupos que usam RADIUS
    radius_groups = []
    for g in data:
        members = g.get("member", [])
        if isinstance(members, list):
            for m in members:
                if isinstance(m, dict) and "radius" in m.get("name", "").lower():
                    radius_groups.append(g)
                    break
                elif isinstance(m, str) and "radius" in m.lower():
                    radius_groups.append(g)
                    break

    if radius_groups:
        groups_str = "\n".join(
            f"  - {g['name']}: members={g.get('member', [])}"
            for g in radius_groups
        )
        return RequirementStatus(
            number=11,
            name="User Groups RADIUS",
            status="✅ OK",
            current_config=f"Grupos RADIUS encontrados:\n{groups_str}",
            suggestion="Nenhuma ação necessária. User groups já configurados.",
        )
    else:
        existing = ", ".join(g.get("name", "?") for g in data)
        return RequirementStatus(
            number=11,
            name="User Groups RADIUS",
            status="❌ Ausente",
            current_config=f"Grupos existentes (sem RADIUS): {existing}",
            suggestion="Criar user group 'SOC_Admins' com membro 'SOC_RADIUS'.",
        )