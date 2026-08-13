from dataclasses import dataclass
from typing import Optional


@dataclass
class SyncDeviceStatus:
    name: str
    adom: str
    serial: str
    ip: str
    platform: str
    os_ver: str
    conn_status: str       # "🟢 Up" ou "🔴 Down"
    db_status: str         # "✅ In-Sync", "❌ Out-of-Sync", "❓ Unknown"
    policy_package: str    # Nome do Policy Package (ex: "default", "PKG-ALGAR")
    policy_status: str     # "Installed", "Modified", "Conflict", "Never Installed", "Unknown"

    @property
    def is_synced(self) -> bool:
        return "In-Sync" in self.db_status and self.policy_status in ("Installed", "Imported")
