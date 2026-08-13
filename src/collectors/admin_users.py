"""
Coletor para Requisito 4: Contas Administrativas Padrão Algar
"""
from src.models.device_inventory import RequirementStatus

# Contas administrativas padrão esperadas conforme baseline Algar
EXPECTED_ADMINS = {"api_soc", "api_nava", "algar_soc", "algar_atv", "operacao_soc"}


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
                "Criar contas administrativas padrão: api_soc, api_nava, algar_soc, algar_atv, operacao_soc."
            ),
        )

    existing_admins = {a.get("name", "") for a in data}
    found = EXPECTED_ADMINS.intersection(existing_admins)

    if len(found) >= 3 or not (EXPECTED_ADMINS - existing_admins):
        admins_str = ", ".join(
            f"{a['name']} ({a.get('accprofile', 'N/A')})"
            for a in data if a.get("name") in existing_admins
        )
        status_flag = "✅ OK" if not (EXPECTED_ADMINS - existing_admins) else "⚠️ Parcial"
        return RequirementStatus(
            number=4,
            name="Contas Admin Padrão",
            status=status_flag,
            current_config=f"Contas encontradas: {admins_str}",
            suggestion="Nenhuma ação crítica necessária." if status_flag == "✅ OK" else f"Criar contas faltantes: {', '.join(EXPECTED_ADMINS - existing_admins)}",
        )
    else:
        missing_str = ", ".join(EXPECTED_ADMINS - existing_admins)
        existing_str = ", ".join(existing_admins)
        return RequirementStatus(
            number=4,
            name="Contas Admin Padrão",
            status="❌ Ausente",
            current_config=f"Contas existentes: {existing_str}. Faltando: {missing_str}",
            suggestion=f"Criar contas faltantes: {missing_str} conforme política de gerenciamento Algar.",
        )