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

    radius_groups = []
    for g in data:
        name_lower = g.get("name", "").lower()
        if "grp.socadmins" in name_lower or "soc" in name_lower:
            radius_groups.append(g)
            continue
        members = g.get("member", [])
        if isinstance(members, list):
            for m in members:
                m_str = str(m.get("name") if isinstance(m, dict) else m).lower()
                if any(k in m_str for k in ("authenticatorfn01", "radius", "algar")):
                    radius_groups.append(g)
                    break

    if radius_groups:
        groups_str = "\n".join(
            f"  - {g['name']}: members={g.get('member', [])}"
            for g in radius_groups
        )
        return RequirementStatus(
            number=11,
            name="User Groups GRP.SOCAdmins",
            status="✅ OK",
            current_config=f"Grupos de autenticação encontrados:\n{groups_str}",
            suggestion="Nenhuma ação necessária. User groups já configurados.",
        )
    else:
        existing = ", ".join(g.get("name", "?") for g in data)
        return RequirementStatus(
            number=11,
            name="User Groups GRP.SOCAdmins",
            status="❌ Ausente",
            current_config=f"Grupos existentes: {existing}",
            suggestion="Criar user group 'GRP.SOCAdmins' com membro 'authenticatorfn01.algar'.",
        )