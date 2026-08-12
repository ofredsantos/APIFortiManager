from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DeviceInfo:
    """Informações básicas do device obtidas do DVMDB"""
    name: str
    serial: str
    adom: str
    hostname: Optional[str] = None
    version: Optional[str] = None
    platform: Optional[str] = None


@dataclass
class RequirementStatus:
    """Status de um requisito de padronização"""
    number: int
    name: str
    status: str  # "✅ OK", "⚠️ Parcial", "❌ Ausente", "🔍 Não verificado"
    current_config: str = ""
    suggestion: str = ""


@dataclass
class DeviceInventory:
    """Inventário completo de um device"""
    device: DeviceInfo
    requirements: list[RequirementStatus] = field(default_factory=list)

    def add_requirement(self, req: RequirementStatus):
        self.requirements.append(req)

    def to_csv_row(self) -> dict:
        """Gera uma linha para o CSV resumo"""
        row = {
            "ADOM": self.device.adom,
            "Device": self.device.name,
            "Hostname": self.device.hostname or "",
            "Serial": self.device.serial,
            "Version": self.device.version or "",
        }
        for req in self.requirements:
            # Abrevia o status para o CSV
            if req.status == "✅ OK":
                row[f"R{req.number:02d}"] = "OK"
            elif req.status == "⚠️ Parcial":
                row[f"R{req.number:02d}"] = "PARCIAL"
            elif req.status == "❌ Ausente":
                row[f"R{req.number:02d}"] = "AUSENTE"
            else:
                row[f"R{req.number:02d}"] = "?"
        return row