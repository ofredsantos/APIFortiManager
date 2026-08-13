# Especificação de Design: Script de Inventário de Sincronia FortiManager (`src/sync_inventory.py`)

**Data:** 05/08/2026  
**Módulo Alvo:** `src/sync_inventory.py`  
**Objetivo:** Criar um módulo de inventário executável que se conecta à API JSON-RPC do FortiManager, coleta o estado de sincronia de configuração (Config/DB Sync: *In-Sync* vs *Out-of-Sync*) e o estado do pacote de políticas (*Policy Package Status*: Installed, Modified, Conflict, etc.) de todos os firewalls FortiGate gerenciados, gerando relatórios em Terminal, CSV e Markdown.

---

## 1. Arquitetura do Módulo

O script será integrado à arquitetura existente da aplicação Python em `src/`:

```
src/
├── config.py             # Carrega credenciais do .env (FMGR_HOST, FMGR_API_KEY)
├── client.py             # Cliente HTTP JSON-RPC FortiManagerClient
├── sync_inventory.py     # [NOVO MÓDULO] Script principal de inventário de sincronia
└── models/
    └── sync_status.py    # [NOVO DATACLASS] Modelo de dados SyncDeviceStatus
```

### Dataclass `SyncDeviceStatus`
- `name` (str): Nome do dispositivo.
- `adom` (str): ADOM pertencente.
- `serial` (str): Número de série.
- `ip` (str): IP de gerência.
- `platform` (str): Modelo do hardware/VM.
- `os_ver` (str): Versão do FortiOS.
- `conn_status` (str): `Up` / `Down`.
- `db_status` (str): `In-Sync` / `Out-of-Sync` / `Unknown`.
- `policy_package` (str): Nome do Policy Package atribuído.
- `policy_status` (str): `Installed` / `Modified` / `Conflict` / `Never Installed` / `Unknown`.

---

## 2. Coleta via API & Mapeamento de Status

### 2.1. Consulta Inicial em Lote
- **Endpoint:** `/dvmdb/device`
- **Método:** `get`
- **Params:** `option: ["extra info", "assignment info"]`
- **Campos Mapeados:**
  - `sn`, `ip`, `platform_str`, `os_ver`, `adom`.
  - `conn_status`: `1` -> `Up`, `0` -> `Down`.
  - `db_status`: `1` / `"in_sync"` -> `In-Sync`, `2` / `"out_of_sync"` -> `Out-of-Sync`.

### 2.2. Consulta de Status do Pacote de Políticas (*Policy Package Status*)
- **Endpoint:** `/pm/config/adom/{adom}/_package/status/{device_name}/root`
- **Método:** `get`
- **Mapeamento:**
  - Extrai o atributo `status` (ex: `Installed`, `Modified`, `Conflict`, `Never Installed`).
  - Extrai o atributo `package_name` / `name` (ex: `default`, `PKG-SPOKE`).

---

## 3. Relatórios e Formatos de Saída

1. **Saída Formatada no Terminal (stdout):**
   - Tabela organizada com colunas: Device, ADOM, IP, Modelo, Conexão, Config Sync, Pacote de Políticas, Status Pacote.
   - Resumo Estatístico: Total de Firewalls, Total In-Sync, Total Out-of-Sync, Desconectados e Distribuição dos Status de Pacotes.

2. **Arquivo CSV (`reports/sync_inventory.csv`):**
   - Colunas brutas prontas para importação no Excel / PowerBI.

3. **Relatório Markdown (`reports/sync_inventory.md`):**
   - Documento executivo estruturado com tabelas de governança e ações corretivas recomendadas para dispositivos desatualizados.
