# Plano de Implementação: Script de Inventário de Sincronia FortiManager (`src/sync_inventory.py`)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Desenvolver o script executável `src/sync_inventory.py` para inventariar o status de sincronia (Config/DB Sync: *In-Sync* vs *Out-of-Sync*) e a situação dos pacotes de política (*Policy Package Status*: Installed, Modified, Conflict, etc.) em todos os firewalls gerenciados pelo FortiManager.

**Architecture:** Módulo Python integrado em `src/`, reutilizando `load_config` e `FortiManagerClient`. Coleta dados em lote via `/dvmdb/device` e `/pm/config/adom/{adom}/_package/status/{device}/root`, salvando relatórios em `reports/sync_inventory.csv` e `reports/sync_inventory.md` e exibindo resumo formatado no terminal.

**Tech Stack:** Python 3, `dataclasses`, `requests`, `csv`, `json`.

## Global Constraints

- Reutilizar `load_config` de `src/config.py` e `FortiManagerClient` de `src/client.py`.
- Tratar graciosamente falhas de conexão de dispositivos mantendo a resiliência da coleta.
- Gerar os relatórios CSV e Markdown no diretório `reports/`.

---

### Task 1: Criar o Dataclass Modelo `SyncDeviceStatus`

**Files:**
- Create: `src/models/sync_status.py`

**Interfaces:**
- Consumes: Dataclass nativo Python.
- Produces: Objeto `SyncDeviceStatus` para armazenar o estado de cada dispositivo.

- [ ] **Step 1: Escrever a definição do dataclass `SyncDeviceStatus`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add "src/models/sync_status.py"
git commit -m "feat: add SyncDeviceStatus dataclass model"
```

---

### Task 2: Implementar o Módulo Principal `src/sync_inventory.py`

**Files:**
- Create: `src/sync_inventory.py`

**Interfaces:**
- Consumes: `src.config.load_config`, `src.client.FortiManagerClient`, `src.models.sync_status.SyncDeviceStatus`.
- Produces: Execução via `python -m src.sync_inventory`, geração de `reports/sync_inventory.csv` e `reports/sync_inventory.md`.

- [ ] **Step 1: Escrever a lógica de coleta de status de dispositivos e pacotes de política**

Criar funções em `src/sync_inventory.py`:
- `parse_conn_status(val)`: Converte inteiros/strings em indicador legível (`🟢 Up` / `🔴 Down`).
- `parse_db_status(val)`: Converte inteiros/strings em indicador legível (`✅ In-Sync` / `❌ Out-of-Sync` / `❓ Unknown`).
- `fetch_policy_package_status(client, adom, device_name, vdom="root")`: Consulta `/pm/config/adom/{adom}/_package/status/{device_name}/{vdom}` e retorna uma tupla `(package_name, status)`.
- `collect_all_sync_statuses(client)`: Executa `/dvmdb/device` com `option: ["extra info", "assignment info"]`, itera os dispositivos e constrói a lista `List[SyncDeviceStatus]`.

- [ ] **Step 2: Escrever os geradores de relatório (Terminal, CSV e Markdown)**

- `print_terminal_summary(devices: List[SyncDeviceStatus])`: Exibe tabela formatada e contadores agregados (Total, Conectados, In-Sync, Out-of-Sync, Policy Package Status).
- `export_csv(devices: List[SyncDeviceStatus], filepath: str)`: Salva em `reports/sync_inventory.csv`.
- `export_markdown(devices: List[SyncDeviceStatus], filepath: str, host: str)`: Salva em `reports/sync_inventory.md`.
- Bloco `main()` chamando `load_config()`, instanciando `FortiManagerClient`, executando a coleta e salvando os relatórios.

- [ ] **Step 3: Commit**

```bash
git add "src/sync_inventory.py"
git commit -m "feat: implement sync_inventory module for FortiManager"
```

---

### Task 3: Validação da Execução do Script

**Files:**
- Test: Execução de `python -m src.sync_inventory` em ambiente sintético/local ou validação sintática do módulo.

- [ ] **Step 1: Testar a importação e execução sintática do módulo**

Rodar no terminal:
`python3 -c "import src.sync_inventory; print('Módulo carregado com sucesso!')"`

- [ ] **Step 2: Commit final**

```bash
git add .
git commit -m "docs: finalize sync inventory script plan and validation"
```
