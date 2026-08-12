from dataclasses import dataclass
from typing import Optional


@dataclass
class BackupResult:
    device_name: str
    hostname: str
    adom: str
    serial: str
    platform: str
    os_ver: str
    file_path: str
    file_size_bytes: int
    status: str            # "✅ Sucesso", "❌ Falha", "⚠️ Vazio/Incompleto"
    error_message: Optional[str] = None
