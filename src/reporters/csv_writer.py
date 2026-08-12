"""
Gerador de CSV resumo de todos os equipamentos
"""
import os
import csv
import io
from src.models.device_inventory import DeviceInventory


def generate_csv(inventories: list[DeviceInventory]) -> str:
    """Gera o conteúdo CSV com resumo de todos os devices"""
    if not inventories:
        return ""

    # Define os cabeçalhos fixos + dinâmicos baseados nos requisitos
    fieldnames = ["ADOM", "Device", "Hostname", "Serial", "Version"]
    if inventories:
        for req in inventories[0].requirements:
            fieldnames.append(f"R{req.number:02d}")

    rows = [inv.to_csv_row() for inv in inventories]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()


def save_csv(inventories: list[DeviceInventory], output_dir: str) -> str:
    """Salva o CSV resumo em arquivo"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "resumo_equipamentos.csv")
    content = generate_csv(inventories)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    return filepath