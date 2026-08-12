"""
Testes para o gerador de CSV
"""
from src.models.device_inventory import DeviceInfo, DeviceInventory, RequirementStatus
from src.reporters.csv_writer import generate_csv


def test_generate_csv():
    """Gera um CSV e verifica o conteúdo"""
    device1 = DeviceInfo(
        name="FGT-TESTE-01",
        serial="FG1K5C3XY1234567",
        adom="DOM_TESTE",
        hostname="fgt-teste-01",
    )
    inv1 = DeviceInventory(device=device1)
    inv1.add_requirement(
        RequirementStatus(number=1, name="VPN", status="✅ OK", current_config="", suggestion="")
    )
    inv1.add_requirement(
        RequirementStatus(number=2, name="Rotas", status="❌ Ausente", current_config="", suggestion="")
    )

    device2 = DeviceInfo(
        name="FGT-TESTE-02",
        serial="FG1K5C3XY7654321",
        adom="DOM_TESTE",
        hostname="fgt-teste-02",
    )
    inv2 = DeviceInventory(device=device2)
    inv2.add_requirement(
        RequirementStatus(number=1, name="VPN", status="❌ Ausente", current_config="", suggestion="")
    )
    inv2.add_requirement(
        RequirementStatus(number=2, name="Rotas", status="✅ OK", current_config="", suggestion="")
    )

    csv_content = generate_csv([inv1, inv2])

    assert "ADOM" in csv_content
    assert "Device" in csv_content
    assert "R01" in csv_content
    assert "R02" in csv_content
    assert "FGT-TESTE-01" in csv_content
    assert "FGT-TESTE-02" in csv_content
    assert "OK" in csv_content
    assert "AUSENTE" in csv_content