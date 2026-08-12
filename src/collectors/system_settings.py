"""
Coletores para Requisitos 12 e 13: admintimeout e Sync Status
"""
from src.models.device_inventory import RequirementStatus

# Valor padrão do admintimeout conforme política Algar
STANDARD_ADMINTIMEOUT = 480


def collect_admintimeout(response: dict) -> RequirementStatus:
    """
    Verifica se o admintimeout está configurado conforme o padrão.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", {})
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=12,
            name="admintimeout",
            status="❌ Ausente",
            current_config="Não foi possível obter configurações globais.",
            suggestion="Verificar conectividade com o device.",
        )

    current_timeout = data.get("admintimeout", 0)

    if current_timeout == STANDARD_ADMINTIMEOUT:
        return RequirementStatus(
            number=12,
            name="admintimeout",
            status="✅ OK",
            current_config=f"admintimeout = {current_timeout} minutos (padrão)",
            suggestion="Nenhuma ação necessária.",
        )
    else:
        return RequirementStatus(
            number=12,
            name="admintimeout",
            status="❌ Ausente",
            current_config=f"admintimeout = {current_timeout} minutos "
                          f"(esperado: {STANDARD_ADMINTIMEOUT})",
            suggestion=(
                f"Ajustar admintimeout para {STANDARD_ADMINTIMEOUT} minutos:\n"
                "config system global\n"
                f"  set admintimeout {STANDARD_ADMINTIMEOUT}\n"
                "end"
            ),
        )


def collect_sync_status(response: dict) -> RequirementStatus:
    """
    Verifica se o device está sincronizado com o FMG.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", {})
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=13,
            name="Sync Status",
            status="❌ Ausente",
            current_config="Não foi possível obter status de sincronia.",
            suggestion="Verificar conectividade com o device.",
        )

    db_status = data.get("db_status", "unknown")
    mgmt_mode = data.get("mgmt_mode", "unknown")

    if db_status == "in_sync":
        return RequirementStatus(
            number=13,
            name="Sync Status",
            status="✅ OK",
            current_config=f"Device sincronizado (db_status={db_status}, mgmt_mode={mgmt_mode})",
            suggestion="Nenhuma ação necessária.",
        )
    else:
        return RequirementStatus(
            number=13,
            name="Sync Status",
            status="❌ Ausente",
            current_config=f"Device fora de sincronia (db_status={db_status}, mgmt_mode={mgmt_mode})",
            suggestion=(
                "Sincronizar device com o FMG:\n"
                "1. Revisar configurações pendentes no FMG\n"
                "2. Executar install para sincronizar"
            ),
        )