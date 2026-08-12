"""
Coletor para Requisito 4: Contas Administrativas Padrão Algar
"""
from src.models.device_inventory import RequirementStatus

# Contas administrativas padrão esperadas
STANDARD_ADMINS = {"algar_ops", "algar_soc"}


def collect_admin_users(response: dict) -> RequirementStatus:
    """
    Verifica se as contas administrativas padrão Algar existem.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=4,
            name="Contas Admin Padrão",
            status="❌ Ausente",
            current_config="Nenhum administrador encontrado.",
            suggestion=(
                "Criar contas administrativas padrão: algar_ops (super_admin) "
                "e algar_soc (read_only)."
            ),
        )

    existing_admins = {a.get("name", "") for a in data}
    missing = STANDARD_ADMINS - existing_admins

    if not missing:
        admins_str = ", ".join(
            f"{a['name']} ({a.get('accprofile', 'N/A')})"
            for a in data if a.get("name") in STANDARD_ADMINS
        )
        return RequirementStatus(
            number=4,
            name="Contas Admin Padrão",
            status="✅ OK",
            current_config=f"Contas padrão encontradas: {admins_str}",
            suggestion="Nenhuma ação necessária. Contas administrativas já existem.",
        )
    else:
        missing_str = ", ".join(missing)
        existing_str = ", ".join(existing_admins)
        return RequirementStatus(
            number=4,
            name="Contas Admin Padrão",
            status="❌ Ausente",
            current_config=f"Contas existentes: {existing_str}. Faltando: {missing_str}",
            suggestion=f"Criar contas faltantes: {missing_str} conforme política de gerenciamento.",
        )