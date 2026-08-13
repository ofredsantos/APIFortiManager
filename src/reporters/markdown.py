"""
Gerador de relatórios Markdown por device
"""
import os
from src.models.device_inventory import DeviceInventory


def generate_device_report(inventory: DeviceInventory) -> str:
    """Gera um relatório Markdown completo para um device"""
    d = inventory.device
    lines = [
        f"# Inventário de Padronização - {d.hostname or d.name}",
        "",
        f"**Device:** {d.name}",
        f"**Serial:** {d.serial}",
        f"**ADOM:** {d.adom}",
        f"**Plataforma:** {d.platform or 'N/A'}",
        f"**Versão:** {d.version or 'N/A'}",
        "",
        "---",
        "## Resumo dos Requisitos",
        "",
        "| # | Requisito | Status |",
        "|---|-----------|--------|",
    ]

    for req in inventory.requirements:
        lines.append(f"| {req.number} | {req.name} | {req.status} |")

    lines.extend(["", "---", "## Detalhamento por Requisito", ""])

    for req in inventory.requirements:
        lines.extend([
            f"### {req.number}. {req.name}",
            "",
            f"**Status:** {req.status}",
            "",
            "**Configuração Atual:**",
            "",
            f"```",
            req.current_config,
            f"```",
            "",
            "**Sugestão:**",
            "",
            req.suggestion,
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def save_device_report(inventory: DeviceInventory, output_dir: str):
    """Salva o relatório Markdown em arquivo"""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{inventory.device.name}.md"
    filepath = os.path.join(output_dir, filename)
    content = generate_device_report(inventory)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath