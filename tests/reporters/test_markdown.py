"""
Testes para o gerador de relatórios Markdown
"""
from src.models.device_inventory import DeviceInfo, DeviceInventory, RequirementStatus
from src.reporters.markdown import generate_device_report


def test_generate_device_report():
    """Gera um relatório Markdown e verifica o conteúdo"""
    device = DeviceInfo(
        name="FGT-TESTE-01",
        serial="FG1K5C3XY1234567",
        adom="DOM_TESTE",
        hostname="fgt-teste-01",
        version="FOS 7.4.0",
        platform="FortiGate-100F",
    )
    inventory = DeviceInventory(device=device)
    inventory.add_requirement(
        RequirementStatus(
            number=1,
            name="VPN IPsec",
            status="✅ OK",
            current_config="2 túneis encontrados",
            suggestion="Nenhuma ação necessária.",
        )
    )
    inventory.add_requirement(
        RequirementStatus(
            number=2,
            name="Rotas Estáticas",
            status="❌ Ausente",
            current_config="Nenhuma rota",
            suggestion="Criar rotas.",
        )
    )

    report = generate_device_report(inventory)

    assert "# Inventário de Padronização - fgt-teste-01" in report
    assert "FG1K5C3XY1234567" in report
    assert "DOM_TESTE" in report
    assert "✅ OK" in report
    assert "❌ Ausente" in report
    assert "2 túneis encontrados" in report
    assert "Nenhuma ação necessária." in report