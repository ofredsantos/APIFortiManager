# Especificação de Design: Script de Backup Completo de Dispositivos (`src/backup_devices.py`)

**Data:** 06/08/2026  
**Módulo Alvo:** `src/backup_devices.py`  
**Objetivo:** Desenvolver um script executável multithreaded que realiza o backup completo das configurações CLI em texto puro de todos os equipamentos FortiGate gerenciados pelo FortiManager, salvando os arquivos em diretórios organizados por Timestamp e ADOM, e gerando relatórios de auditoria em Terminal, CSV e Markdown.

---

## 1. Arquitetura do Módulo

O script será integrado à arquitetura existente da aplicação Python em `src/`:

```
src/
├── config.py             # Carrega credenciais do .env (FMGR_HOST, FMGR_API_KEY)
├── client.py             # Cliente HTTP JSON-RPC FortiManagerClient
├── backup_devices.py     # [NOVO MÓDULO] Script principal de backup
└── models/
    └── backup_status.py  # [NOVO DATACLASS] Modelo de dados BackupResult
```

### Dataclass `BackupResult`
- `device_name` (str): Nome do dispositivo no DVMDB.
- `hostname` (str): Hostname configurado no FortiGate.
- `adom` (str): Nome da ADOM a qual o equipamento pertence.
- `serial` (str): Número de série (`sn`).
- `platform` (str): Modelo do hardware/VM.
- `os_ver` (str): Versão do FortiOS.
- `file_path` (str): Caminho absoluto do arquivo `.conf` salvo.
- `file_size_bytes` (int): Tamanho do arquivo salvo em bytes.
- `status` (str): `✅ Sucesso`, `❌ Falha`, `⚠️ Vazio/Incompleto`.
- `error_message` (str): Mensagem detalhada de eventual erro.

---

## 2. Coleta Concorrente & Estrutura de Diretórios

### 2.1. Estrutura de Pastas e Nomenclatura
- **Formato de Timestamp de Execução:** `YYYY-MM-DD_HH-MM-SS` (ex: `2026-08-06_16-45-00`).
- **Diretório Raiz:** `backups/<timestamp_execucao>/`
- **Subpastas por ADOM:** `backups/<timestamp_execucao>/<ADOM>/`
- **Arquivo `.conf`:** `<hostname>_<timestamp_execucao>.conf`

### 2.2. Fluxo de Download e Fallback de API
- **Endpoint Principal:** `/deployment/export/config` (`method: exec`, `data: {"device": device_name}`).
- **Endpoint Fallback:** `/deployment/checkout/revision` (`method: exec`, `data: {"device": device_name, "revision": -1}`).
- **Execução Concorrente:** `concurrent.futures.ThreadPoolExecutor(max_workers=10)` para download paralelo de alta velocidade.

### 2.3. Validação de Integridade
- Checa se o arquivo retornado possui tamanho > 1000 bytes e contém o cabeçalho nativo FortiOS (`#config-version=`).

---

## 3. Relatórios e Formatos de Saída

Todos os relatórios da execução serão gravados dentro do diretório `backups/<timestamp_execucao>/`:

1. **Dashboard no Terminal (Console Output):** Tabela resumo em tempo real e consolidação de total de dispositivos, volume baixado em MB e tempo total.
2. **Relatório CSV (`backups/<timestamp_execucao>/backup_summary.csv`):** Tabela estruturada para importação e auditoria.
3. **Relatório Executivo Markdown (`backups/<timestamp_execucao>/backup_summary.md`):** Documento formal com indicadores de sucesso por ADOM e destaques de falha.
