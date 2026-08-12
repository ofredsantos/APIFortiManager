"""
Coletor para Requisito 3: Perfil de Administrador 'API'
"""
from src.models.device_inventory import RequirementStatus


def collect_accprofile(response: dict) -> RequirementStatus:
    """
    Verifica se existe um accprofile chamado 'API'.
    """
    result = response.get("result", [{}])[0]
    data = result.get("data", [])
    status_code = result.get("status", {}).get("code", -1)

    if status_code != 0 or not data:
        return RequirementStatus(
            number=3,
            name="Accprofile 'API'",
            status="❌ Ausente",
            current_config="Nenhum perfil de administrador encontrado.",
            suggestion=(
                "Criar accprofile 'API' com permissões de leitura/escrita via RPC: "
                "config system accprofile\n"
                "  edit API\n"
                "    set adomprlv custom\n"
                "    set fmgprlv custom\n"
                "    set rpc-permit read-write\n"
                "  next\nend"
            ),
        )

    api_profile = [p for p in data if p.get("name", "").lower() == "api"]

    if api_profile:
        return RequirementStatus(
            number=3,
            name="Accprofile 'API'",
            status="✅ OK",
            current_config=f"Perfil 'API' encontrado: {api_profile[0]}",
            suggestion="Nenhuma ação necessária. Accprofile 'API' já existe.",
        )
    else:
        existing = ", ".join(p.get("name", "?") for p in data)
        return RequirementStatus(
            number=3,
            name="Accprofile 'API'",
            status="❌ Ausente",
            current_config=f"Perfis existentes: {existing}",
            suggestion="Criar accprofile 'API' conforme padrão operacional.",
        )