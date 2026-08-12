# Plano de Implementação: Script de Backup Completo de Dispositivos (`src/backup_devices.py`)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Desenvolver o script executável multithreaded `src/backup_devices.py` para realizar o backup completo das configurações CLI de todos os firewalls gerenciados pelo FortiManager, salvando em subpastas organizadas por Timestamp/ADOM e gerando relatórios de auditoria.

**Architecture:** Módulo Python integrado em `src/`, reutilizando `load_config` e `FortiManagerClient`. Coleta dispositivos via `/dvmdb/device`, baixa arquivos de configuração CLI via `/deployment/export/config` (fallback `/deployment/checkout/revision`) usando `ThreadPoolExecutor(max_workers=10)`, gravando os arquivos `.conf`, `backup_summary.csv` e `backup_summary.md` no diretório `backups/<timestamp_execucao>/`.

**Tech Stack:** Python 3, `dataclasses`, `concurrent.futures`, `requests`, `csv`, `json`, `os`, `time`.

## Global Constraints

- Reutilizar `load_config` de `src/config.py` e `FortiManagerClient` de `src/client.py`.
- Formatar timestamps como `YYYY-MM-DD_HH-MM-SS`.
- Salvar todos os backups e relatórios de cada execução dentro do diretório `backups/<timestamp_execucao>/`.

---

### Task 1: Criar o Dataclass Modelo `BackupResult`

**Files:**
- Create: `src/models/backup_status.py`

**Interfaces:**
- Consumes: Dataclass nativo Python.
- Produces: Objeto `BackupResult` para armazenar o resultado de cada backup.

- [ ] **Step 1: Escrever a definição do dataclass `BackupResult`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add "src/models/backup_status.py"
git commit -m "feat: add BackupResult dataclass model"
```

---

### Task 2: Implementar o Módulo Principal `src/backup_devices.py`

**Files:**
- Create: `src/backup_devices.py`

**Interfaces:**
- Consumes: `src.config.load_config`, `src.client.FortiManagerClient`, `src.models.backup_status.BackupResult`.
- Produces: Execução via `python -m src.backup_devices`, download paralelo em `backups/<timestamp>/<adom>/<hostname>_<timestamp>.conf` e relatórios.

- [ ] **Step 1: Escrever a lógica de download de configuração individual de um dispositivo**

Criar a função `backup_single_device(client, dev_data, timestamp_str, base_backup_dir)`:
- Identifica `device_name`, `hostname` (fallback para `device_name`), `adom` (via `vdom[0]['extra info']['adom']`), `serial`, `platform`, `os_ver`.
- Cria a pasta do ADOM: `os.path.join(base_backup_dir, adom)`.
- Dispara requisição `/deployment/export/config` (`data={"device": device_name}`).
- Se retornar erro ou payload vazio, tenta o fallback em `/deployment/checkout/revision` (`data={"device": device_name, "revision": -1}`).
- Valida o conteúdo recebido (se inicia com `#config-version=` ou possui > 1000 bytes).
- Salva o arquivo `.conf` em `backups/<timestamp_str>/<adom>/<hostname>_<timestamp_str>.conf`.
- Retorna uma instância de `BackupResult`.

- [ ] **Step 2: Escrever a lógica de execução concorrente (`ThreadPoolExecutor`) e geradores de relatórios**

- `backup_all_devices(client, max_workers=10)`:
  - Cria pasta base `backups/YYYY-MM-DD_HH-MM-SS`.
  - Dispara `ThreadPoolExecutor` para baixar os arquivos em paralelo.
  - Exibe resumo no terminal.
  - Salva `backup_summary.csv` e `backup_summary.md` no diretório da execução.

- [ ] **Step 3: Commit**

```bash
git add "src/backup_devices.py"
git commit -m "feat: implement backup_devices module for FortiManager"
```

---

### Task 3: Validação da Execução do Script de Backup

**Files:**
- Test: Execução real de `python -m src.backup_devices` e verificação dos arquivos `.conf` salvos no diretório `backups/`.

- [ ] **Step 1: Testar o script baixando backups em tempo real**

Rodar no terminal:
`python3 -m src.backup_devices`

- [ ] **Step 2: Verificar a integridade dos arquivos gerados**

Confirmar se a pasta `backups/<timestamp>` foi criada, se os arquivos `.conf` por ADOM existem e se possuem o cabeçalho `#config-version=`.

- [ ] **Step 3: Commit final**

```bash
git add .
git commit -m "feat: complete device backup execution and verification"
```
