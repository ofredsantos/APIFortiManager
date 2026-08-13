# FortiManager JSON RPC API — Guia de Referência para Engenheiros

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura da API](#2-arquitetura-da-api)
3. [Autenticação](#3-autenticação)
4. [Métodos JSON RPC](#4-métodos-json-rpc)
5. [Opções de Requisição](#5-opções-de-requisição)
6. [URLs da API por Categoria](#6-urls-da-api-por-categoria)
7. [Multiplexing (Batching)](#7-multiplexing-batching)
8. [Gerenciamento de Tarefas Assíncronas](#8-gerenciamento-de-tarefas-assíncronas)
9. [Proxy para APIs do FortiGate](#9-proxy-para-apis-do-fortigate)
10. [Fluxos Completos de Exemplo](#10-fluxos-completos-de-exemplo)
11. [Boas Práticas](#11-boas-práticas)
12. [Referência Rápida de Variáveis](#12-referência-rápida-de-variáveis)
13. [Diferenças entre Versões de ADOM](#13-diferenças-entre-versões-de-adom)

---

## 1. Visão Geral

A **FortiManager JSON RPC API** é uma API baseada no padrão **JSON RPC 2.0** que permite automação completa de um ou mais FortiManagers. Todas as operações — desde autenticação até provisionamento, monitoramento e instalação — utilizam o mesmo endpoint e estrutura de payload.

### 1.1. Características Fundamentais

| Característica | Descrição |
|---|---|
| **Protocolo** | JSON RPC 2.0 sobre HTTPS |
| **Endpoint único** | `POST https://<fmg_ip>/jsonrpc` |
| **Porta padrão** | 443 (HTTPS) |
| **Formato do body** | JSON |
| **Autenticação** | Session-based (login/logout) ou Token-based (API key) |
| **Idempotência** | Métodos `get` são seguros; `set`/`add`/`delete` não são |
| **Operações assíncronas** | Operações longas retornam task ID para polling |
| **Multiplexing** | Múltiplas operações em um único request |

### 1.2. Estrutura do Payload

```json
{
  "id": <number>,
  "method": "<get|set|add|update|delete|exec|move>",
  "params": [
    {
      "url": "<path_da_api>",
      "data": { ... },
      "option": ["loadsub", "count", ...],
      "filter": [...],
      "fields": ["name", ...]
    }
  ],
  "session": "<session_id>",
  "verbose": 1
}
```

### 1.3. Estrutura da Resposta

```json
{
  "id": 1,
  "result": [
    {
      "data": { ... },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "<path_da_api>"
    }
  ],
  "session": "<session_id>"
}
```

O campo `status.code` é crítico: `0` significa sucesso, qualquer outro valor indica erro.

---

## 2. Arquitetura da API

### 2.1. Conceitos Fundamentais

A API do FortiManager organiza-se em torno de três grandes domínios:

#### 2.1.1. Device Manager (Configuração de Dispositivos)

Gerencia configurações de rede e sistema dos devices gerenciados. Utiliza URLs no formato:

- **Global scope** (para devices sem VDOM ou config global):
  ```
  /pm/config/device/<device>/global/<cli_path>
  ```

- **VDOM scope** (para configurações por VDOM):
  ```
  /pm/config/device/<device>/vdom/<vdom>/<cli_path>
  ```

Onde `<cli_path>` é o caminho CLI do FortiGate sem a palavra `config` e com espaços substituídos por `/`.

**Exemplo:** Para configurar DNS (`config system dns`) no device `FGT1`:
```
/pm/config/device/FGT1/global/system/dns
```

> **⚠️ Importante:** Interfaces (`config system interface`) usam **sempre** o formato global scope, mesmo em devices com VDOM.

#### 2.1.2. Policy & Objects (Objetos de Segurança)

Gerencia objetos de segurança e policy packages no banco de dados do ADOM:

- **Objetos** (addresses, services, etc.):
  ```
  /pm/config/adom/<adom>/obj/<cli_path>
  ```

- **Policy packages**:
  ```
  /pm/config/adom/<adom>/pkg/<pkg>/firewall/policy
  ```

#### 2.1.3. System & Device Management Database (dvmdb)

Gerencia a infraestrutura do FortiManager: ADOMs, devices, grupos, scripts:

```
/dvmdb/adom
/dvmdb/device
/dvmdb/group
/dvmdb/script
```

### 2.2. Hierarquia de URLs

```
/fmg
├── /sys                    # Sistema do FMG (status, login, logout, hitcount)
├── /dvmdb                  # Device Management Database
│   ├── /adom               # ADOMs
│   ├── /device             # Devices gerenciados
│   ├── /group              # Grupos de devices
│   ├── /script             # CLI scripts
│   └── /_meta_fields       # Meta fields (custom variables)
├── /pm                     # Policy & Object Manager
│   ├── /config
│   │   ├── /adom/<adom>
│   │   │   ├── /obj/...    # Objetos de segurança
│   │   │   └── /pkg/...    # Policy packages
│   │   └── /device/<dev>
│   │       ├── /global/... # Config global do device
│   │       └── /vdom/...   # Config VDOM do device
│   ├── /pkg/adom/<adom>    # Lista de policy packages
│   └── /wanprof/adom/<adom> # Perfis SD-WAN
├── /securityconsole        # Instalação de configurações
│   ├── /install/device     # Instalar config de device
│   └── /install/package    # Instalar policy package
├── /task/task/<id>         # Monitoramento de tasks
├── /um                     # Upgrade Management
│   ├── /image/upgrade      # Upgrade de firmware
│   └── /misc/dump_contract # Contratos de suporte
└── /sys/proxy/json         # Proxy para APIs nativas do FortiGate
```

---

## 3. Autenticação

### 3.1. Session-based Authentication

Fluxo tradicional: login → obter session ID → operações → logout.

#### 3.1.1. Login

**Request:**
```json
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "user": "admin",
        "passwd": "fortinet"
      },
      "url": "/sys/login/user"
    }
  ],
  "session": null,
  "verbose": 1
}
```

**Response:**
```json
{
  "id": 1,
  "result": [
    {
      "status": { "code": 0, "message": "OK" },
      "url": "/sys/login/user"
    }
  ],
  "session": "y5I9dOaJyotAoco6nY3VfUcgTwp7Alk7jib3tX5ECEv4WabzSllv9umEzfAFVJxI4azqZE9xEh3lEWLi1AOYbw=="
}
```

O campo `session` retornado deve ser incluído em **todas** as requisições subsequentes.

> **Nota:** O atributo `session` pode ser omitido no login ou definido como `null`.

#### 3.1.2. Logout

```json
{
  "id": 1,
  "method": "exec",
  "params": [
    { "url": "/sys/logout" }
  ],
  "session": "<session_id>",
  "verbose": 1
}
```

### 3.2. Token-based Authentication (API Key)

Disponível desde FMG 7.2.2. Elimina a necessidade de login/logout explícitos.

#### 3.2.1. Configuração do API User no FMG

```cli
config system admin user
    edit api_001
        set user_type api
        set rpc-permit read-write
    next
end
```

#### 3.2.2. Geração da API Key

```cli
execute api-user generate-key api_001
```

Retorna: `New API key: 33fzwipq4amujunzgzn46mg1to9p8wbi`

A API key é **permanente** (nunca expira), mas pode ser renovada.

#### 3.2.3. Uso da API Key

Via HTTP Header:
```
POST https://<fmg_ip>/jsonrpc
Authorization: Bearer 33fzwipq4amujunzgzn46mg1to9p8wbi
```

> **⚠️ A partir de FMG 7.4.7/7.6.2:** Não é mais possível usar `access_token` como query string.

> **⚠️ A partir de FMG 7.6.7/8.0.0:** É possível especificar o API user name via header `access_user`:
> ```
> access_user: api_001
> ```

### 3.3. FortiManager Cloud Authentication

Para instâncias FortiManager Cloud, o fluxo é multi-etapas:

1. **Obter FortiCloud Token:**
   ```json
   POST https://customerapiauth.fortinet.com/api/v1/oauth/token/
   {
     "username": "<IAM_API_user_apiId>",
     "password": "<IAM_API_user_password>",
     "client_id": "FortiManager",
     "grant_type": "password"
   }
   ```

2. **Obter Session ID do FMG Cloud:**
   ```json
   POST https://<account_id>.<region>.fortimanager.forticloud.com/p/forticloud_jsonrpc_login/
   {
     "access_token": "<forticloud_token>"
   }
   ```

3. **Operações normais** usando o session ID obtido no endpoint:
   ```
   https://<account_id>.<region>.fortimanager.forticloud.com/jsonrpc
   ```

> **Nota:** FMG Cloud **não** suporta token-based authentication.

---

## 4. Métodos JSON RPC

| Método | Descrição | Equivalente CLI/HTTP |
|---|---|---|
| `get` | Ler configurações ou objetos | `show`, `get` |
| `set` | Criar ou substituir objeto | `edit <name>` + `set` |
| `add` | Adicionar a uma lista/tabela | `edit <new>` |
| `update` | Atualizar parcialmente | `set <attr>` (patch) |
| `delete` | Remover objeto | `delete` |
| `exec` | Executar ação | Comandos de ação |
| `move` | Reordenar (ex.: políticas) | `move` |

### 4.1. Exemplos por Método

**get** — Listar devices:
```json
{
  "method": "get",
  "params": [{ "url": "/dvmdb/device" }],
  "session": "<session>",
  "id": 1
}
```

**set** — Criar firewall address:
```json
{
  "method": "set",
  "params": [{
    "data": [{ "name": "server1", "type": "ipmask", "subnet": "10.0.0.1/32" }],
    "url": "/pm/config/adom/root/obj/firewall/address"
  }],
  "session": "<session>",
  "id": 1
}
```

**add** — Adicionar device a grupo:
```json
{
  "method": "add",
  "params": [{
    "data": [{ "name": "FGT1", "vdom": "root" }],
    "url": "/dvmdb/group/MyGroup/object member"
  }],
  "session": "<session>",
  "id": 1
}
```

**update** — Alterar password do usuário:
```json
{
  "method": "update",
  "params": [{
    "data": { "password": "nova_senha" },
    "url": "/cli/global/system/admin/user/admin"
  }],
  "session": "<session>",
  "id": 1
}
```

**delete** — Remover firewall address:
```json
{
  "method": "delete",
  "params": [{ "url": "/pm/config/adom/root/obj/firewall/address/server1" }],
  "session": "<session>",
  "id": 1
}
```

**exec** — Executar script:
```json
{
  "method": "exec",
  "params": [{
    "data": {
      "adom": "root",
      "script": "my_script",
      "scope": [{ "name": "FGT1", "vdom": "root" }]
    },
    "url": "/dvmdb/script/execute"
  }],
  "session": "<session>",
  "id": 1
}
```

---

## 5. Opções de Requisição

### 5.1. `loadsub`

Instrui o FMG a retornar informações de sub-tabelas.

```json
"option": ["loadsub"]
// ou
"loadsub": 1
```

### 5.2. `count`

Retorna apenas o número de entradas em uma tabela.

```json
"option": ["count"]
```

**Response:** `"data": 400000` (número de firewall addresses)

### 5.3. `syntax`

Retorna o schema completo de um objeto ou tabela, incluindo tipos, valores padrão, limites e referências a outras tabelas.

```json
"option": ["syntax"]
```

**Uso típico:** Descobrir a estrutura de um objeto antes de criá-lo programaticamente.

**Exemplo de retorno:**
```json
{
  "data": {
    "firewall address": {
      "alimit": 400000,
      "attr": {
        "allow-routing": {
          "default": "disable",
          "type": "uint32",
          "opts": { "disable": 0, "enable": 1 }
        },
        "subnet": {
          "type": "string"
        }
      }
    }
  }
}
```

O atributo `alimit` (disponível desde FMG 6.2.4/6.4.0) indica o limite máximo de objetos daquele tipo.

### 5.4. `devinfo`

Retorna um checksum do ADOM, útil para detectar mudanças.

```json
"option": ["devinfo"],
"url": "/pm/config/adom/TEST/obj"
```

### 5.5. `datasrc`

Lista objetos disponíveis de tipos específicos que podem ser usados como referência em outros objetos.

```json
"attr": "member",
"option": "datasrc",
"url": "/pm/config/adom/DEMO/obj/firewall/internet-service-group"
```

### 5.6. `chksum`

Retorna a versão/checksum de uma tabela específica.

```json
"option": "chksum",
"url": "pm/config/adom/root/pkg/default/firewall/policy"
```

**Response:** `"data": 6` (versão 6 do policy package)

### 5.7. `object member`

Retorna os membros de um grupo ou escopo.

```json
"option": "object member",
"url": "/dvmdb/adom"
```

### 5.8. `filter`

Filtra resultados usando operadores lógicos.

**Formato:** `[<field>, <operator>, <value>]`

**Operadores suportados:**
| Operador | Descrição |
|---|---|
| `==` | Igual |
| `!=` | Diferente |
| `>`, `<`, `>=`, `<=` | Comparação numérica |
| `like` | LIKE SQL (case insensitive) |
| `glob` | Pattern matching com `*` e `?` |
| `in` | Múltiplos valores (OR interno) |

**AND filter:**
```json
"filter": [
  ["tcp-portrange", "in", "80", "443"],
  "&&",
  ["udp-portrange", "==", "53"]
]
```

**OR filter** (múltiplos filtros no mesmo nível):
```json
"filter": [
  ["tcp-portrange", "in", "80", "443"],
  ["udp-portrange", "==", "53"]
]
```

### 5.9. `fields`

Seleciona campos específicos para retornar, melhorando performance.

```json
"fields": ["name", "policyid", "status", "srcintf", "dstintf"]
```

### 5.10. `sort`

Ordena resultados.

```json
"sort": [["name", 1]]  // 1 = ascending, -1 = descending
```

---

## 6. URLs da API por Categoria

### 6.1. System

| Operação | URL | Método |
|---|---|---|
| Status do FMG | `/sys/status` | `get` |
| Interfaces do FMG | `/cli/global/system/interface` | `get` |
| Config global do FMG | `/cli/global/system/global` | `get` |
| Hitcounts (solicitar) | `/sys/hitcount` | `exec` |
| Resultado de task | `/sys/task/result` | `get` |

### 6.2. Autenticação

| Operação | URL | Método |
|---|---|---|
| Login | `/sys/login/user` | `exec` |
| Logout | `/sys/logout` | `exec` |
| Change password | `/cli/global/system/admin/user/<user>` | `update` |

### 6.3. ADOMs

| Operação | URL | Método |
|---|---|---|
| Listar ADOMs | `/dvmdb/adom` | `get` |
| Detalhe de ADOM | `/dvmdb/adom/<adom>` | `get` |
| Criar ADOM | `/dvmdb/adom` | `add` |
| Deletar ADOM | `/dvmdb/adom/<adom>` | `delete` |
| Mover device para ADOM | `/dvmdb/adom/<adom>/object member` | `add` |

### 6.4. Devices

| Operação | URL | Método |
|---|---|---|
| Listar devices | `/dvmdb/device` | `get` |
| Listar não autorizados | `/dvmdb/device` (filter: `mgmt_mode == unreg`) | `get` |
| Detalhe do device | `/dvmdb/device/<device>` | `get` |
| Registrar device | `/dvm/cmd/add/device` | `exec` |
| Autorizar device | `/dvm/cmd/add/device` (com `promote_unreg`) | `exec` |
| Deletar device | `/dvm/cmd/del/device` | `exec` |
| Listar grupos | `/dvmdb/group` | `get` |
| Add device a grupo | `/dvmdb/group/<group>/object member` | `add` |
| Remover device de grupo | `/dvmdb/group/<group>/object member` | `delete` |
| Contratos | `/um/misc/dump_contract` | `exec` |

### 6.5. Device Configuration

| Escopo | URL Pattern | Exemplo |
|---|---|---|
| Global | `/pm/config/device/<dev>/global/<cli>` | `/pm/config/device/FGT1/global/system/dns` |
| VDOM | `/pm/config/device/<dev>/vdom/<vdom>/<cli>` | `/pm/config/device/FGT1/vdom/root/router/static` |

### 6.6. Firewall Objects

| Operação | URL | Método |
|---|---|---|
| Listar addresses | `/pm/config/adom/<adom>/obj/firewall/address` | `get` |
| Criar address | `/pm/config/adom/<adom>/obj/firewall/address` | `set` |
| Deletar address | `/pm/config/adom/<adom>/obj/firewall/address/<name>` | `delete` |
| Listar services | `/pm/config/adom/<adom>/obj/firewall/service/custom` | `get` |
| Listar service groups | `/pm/config/adom/<adom>/obj/firewall/service/group` | `get` |
| Criar service group | `/pm/config/adom/<adom>/obj/firewall/service/group` | `set` |
| Deletar service group | `/pm/config/adom/<adom>/obj/firewall/service/group/<name>` | `delete` |

### 6.7. Policy Packages

| Operação | URL | Método |
|---|---|---|
| Listar packages | `/pm/pkg/adom/<adom>` | `get` |
| Listar firewall policies | `/pm/config/adom/<adom>/pkg/<pkg>/firewall/policy` | `get` |
| Instalar package | `/securityconsole/install/package` | `exec` |
| Reinstalar package | `/securityconsole/reinstall/package` | `exec` |
| Instalar device config | `/securityconsole/install/device` | `exec` |

### 6.8. SD-WAN

| Operação | URL | Método |
|---|---|---|
| Listar profiles | `/pm/wanprof/adom/<adom>` | `get` |
| Profile detail | `/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan` | `get` |
| Members em zone | `/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan/members` | `get` |
| Add member | `/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan/members` | `add` |
| Delete member | `/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan/members/<id>` | `delete` |
| Change assignment | `/pm/wanprof/adom/<adom>/<profile>` | `update` |

### 6.9. Normalized Interfaces

| Operação | URL | Método |
|---|---|---|
| Interface mapping | `/pm/config/adom/<adom>/obj/dynamic/interface` | `get` |
| Per-device mapping | `/pm/config/adom/<adom>/obj/dynamic/interface/<name>/dynamic_mapping` | `get` |
| Per-platform mapping | `/pm/config/adom/<adom>/obj/dynamic/interface/<name>/platform_mapping/<platform>` | `get` |

### 6.10. Meta Fields

| Operação | URL | Método |
|---|---|---|
| Listar meta fields | `/dvmdb/_meta_fields/vdom` | `get` |
| Criar meta field | `/dvmdb/_meta_fields/vdom` | `add` |
| Get meta values | `/dvmdb/adom/<adom>/device/<dev>/vdom/<vdom>` | `get` |
| Set meta value | `/dvmdb/adom/<adom>/device/<dev>/vdom/<vdom>` | `set` |

### 6.11. VPN (IPSec)

| Operação | URL | Método |
|---|---|---|
| Listar phase1 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase1-interface` | `get` |
| Criar phase1 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase1-interface` | `set` |
| Deletar phase1 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase1-interface/<name>` | `delete` |
| Listar phase2 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase2-interface` | `get` |
| Criar phase2 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase2-interface` | `set` |
| Deletar phase2 | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase2-interface/<name>` | `delete` |

### 6.12. Scripts

| Operação | URL | Método |
|---|---|---|
| Listar scripts | `/dvmdb/script` | `get` |
| Criar script | `/dvmdb/script` | `set` |
| Executar script | `/dvmdb/script/execute` | `exec` |
| Deletar script | `/dvmdb/script/<name>` | `delete` |
| Logs de scripts | `/dvmdb/global/script/log/summary` | `get` |

### 6.13. Firmware

| Operação | URL | Método |
|---|---|---|
| Upgrade device | `/um/image/upgrade` | `exec` |

### 6.14. Tasks

| Operação | URL | Método |
|---|---|---|
| Status da task | `/task/task/<id>` | `get` |

---

## 7. Multiplexing (Batching)

O FMG permite agrupar múltiplas operações em um único request HTTP, utilizando múltiplos elementos no array `params`.

### 7.1. Mesma URL, Diferentes Contextos

```json
{
  "id": 1,
  "method": "get",
  "params": [
    { "url": "pm/config/adom/adom_001/obj/webfilter/profile", "fields": ["name"], "loadsub": 0 },
    { "url": "pm/config/adom/adom_002/obj/webfilter/profile", "fields": ["name"], "loadsub": 0 },
    { "url": "pm/config/adom/adom_003/obj/webfilter/profile", "fields": ["name"], "loadsub": 0 }
  ],
  "session": "<session_id>"
}
```

### 7.2. URLs Diferentes

```json
{
  "id": 3,
  "method": "get",
  "params": [
    { "fields": ["name"], "loadsub": 0, "url": "/dvmdb/device" },
    { "fields": ["name"], "filter": ["restricted_prds", "==", "fos"], "loadsub": 0, "url": "/dvmdb/adom" }
  ],
  "session": "<session_id>"
}
```

### 7.3. Monitoramento Multi-ADOM via Proxy

```json
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "action": "get",
        "resource": "/api/v2/monitor/firewall/policy",
        "target": ["/adom/dc_emea/group/All_FortiGate"]
      },
      "url": "/sys/proxy/json"
    },
    {
      "data": {
        "action": "get",
        "resource": "/api/v2/monitor/system/available-interfaces?format=name|ipv4_addresses",
        "target": ["/adom/dc_amer/group/All_FortiGate"]
      },
      "url": "/sys/proxy/json"
    }
  ],
  "session": "<session>"
}
```

---

## 8. Gerenciamento de Tarefas Assíncronas

Operações como instalação de configuração, upgrade de firmware e execução de scripts são **assíncronas**. O FMG retorna imediatamente com um **task ID**, que deve ser monitorado via polling.

### 8.1. Resposta Inicial

```json
{
  "id": 1,
  "result": [{
    "data": { "task": 2066 },
    "status": { "code": 0, "message": "OK" },
    "url": "/securityconsole/install/device"
  }]
}
```

### 8.2. Polling da Task

```json
{
  "method": "get",
  "params": [{ "url": "/task/task/2066" }],
  "session": "<session>",
  "id": 1
}
```

### 8.3. Atributos Chave da Resposta

| Atributo | Descrição |
|---|---|
| `percent` | Progresso global (0-100) |
| `num_lines` | Número de sub-tasks |
| `num_err` | Número de sub-tasks com erro |
| `num_warn` | Número de sub-tasks com warning |
| `state` | Estado: `running`, `done` |
| `tot_percent` | Soma dos percentuais de todas as sub-tasks |
| `line[].history` | Histórico detalhado de cada sub-task |
| `line[].state` | Estado de cada sub-task |
| `line[].percent` | Progresso de cada sub-task |

### 8.4. Algoritmo de Polling Recomendado

```python
import time

def wait_for_task(session, task_id, interval=5, timeout=300):
    elapsed = 0
    while elapsed < timeout:
        response = fmg_request("get", f"/task/task/{task_id}", session)
        data = response["result"][0]["data"]
        
        if data["percent"] == 100:
            if data["num_err"] == 0:
                return {"success": True, "data": data}
            else:
                return {"success": False, "errors": data["num_err"], "data": data}
        
        time.sleep(interval)
        elapsed += interval
    
    return {"success": False, "error": "timeout"}
```

---

## 9. Proxy para APIs do FortiGate

O FMG pode atuar como proxy para acessar APIs nativas REST dos FortiGates gerenciados, utilizando a URL `/sys/proxy/json`.

### 9.1. Estrutura

```json
{
  "method": "exec",
  "params": [{
    "data": {
      "action": "get|post|put|delete",
      "resource": "/api/v2/<path>",
      "target": ["/adom/<adom>/device/<device>"],
      "payload": { ... }  // apenas para POST/PUT
    },
    "url": "/sys/proxy/json"
  }],
  "session": "<session>"
}
```

### 9.2. Exemplos de Uso

**Backup de configuração:**
```json
{
  "data": {
    "action": "get",
    "resource": "/api/v2/monitor/system/config/backup/?scope=global",
    "target": ["/adom/root/device/FGT1"]
  },
  "url": "/sys/proxy/json"
}
```

**Status de licenças:**
```json
{
  "data": {
    "action": "get",
    "resource": "/api/v2/monitor/license/status",
    "target": ["/adom/root/device/FGT1"]
  },
  "url": "/sys/proxy/json"
}
```

**Alterar senha de admin:**
```json
{
  "data": {
    "action": "post",
    "resource": "/api/v2/monitor/system/change-password/select",
    "target": ["/adom/root/device/FGT1"],
    "payload": {
      "mkey": "admin",
      "old_password": "old",
      "new_password": "new"
    }
  },
  "url": "/sys/proxy/json"
}
```

---

## 10. Fluxos Completos de Exemplo

### 10.1. Fluxo Básico: Login → Listar → Logout

```python
import requests
import json

BASE_URL = "https://<fmg_ip>/jsonrpc"

def fmg_call(method, url, session=None, data=None, **kwargs):
    payload = {
        "id": 1,
        "method": method,
        "params": [{"url": url}],
        "verbose": 1
    }
    if data:
        payload["params"][0]["data"] = data
    if session:
        payload["session"] = session
    if kwargs:
        payload["params"][0].update(kwargs)
    
    response = requests.post(BASE_URL, json=payload, verify=False)
    return response.json()

# Login
login_resp = fmg_call("exec", "/sys/login/user", data={"user": "admin", "passwd": "fortinet"})
session = login_resp["session"]

# Listar devices
devices = fmg_call("get", "/dvmdb/device", session=session)

# Listar ADOMs
adoms = fmg_call("get", "/dvmdb/adom", session=session)

# Logout
fmg_call("exec", "/sys/logout", session=session)
```

### 10.2. Criar Objeto e Instalar

```python
# 1. Criar firewall address
fmg_call("set", "/pm/config/adom/root/obj/firewall/address",
         session=session,
         data=[{"name": "server1", "type": "ipmask", "subnet": "10.0.0.1/32"}])

# 2. Instalar device config
install_resp = fmg_call("exec", "/securityconsole/install/device",
                        session=session,
                        data={
                            "adom": "root",
                            "scope": [{"name": "FGT1", "vdom": "root"}]
                        })
task_id = install_resp["result"][0]["data"]["task"]

# 3. Aguardar conclusão
result = wait_for_task(session, task_id)
```

### 10.3. Executar CLI Script

```python
# 1. Criar script
fmg_call("set", "/dvmdb/script",
         session=session,
         data={
             "name": "set_timeout",
             "type": "cli",
             "target": "device_database",
             "content": "config system global\nset admintimeout 400\nend\n"
         })

# 2. Executar script
exec_resp = fmg_call("exec", "/dvmdb/script/execute",
                     session=session,
                     data={
                         "adom": "root",
                         "script": "set_timeout",
                         "scope": [{"name": "FGT1", "vdom": "root"}]
                     })
task_id = exec_resp["result"][0]["data"]["task"]

# 3. Aguardar conclusão
result = wait_for_task(session, task_id)
```

---

## 11. Boas Práticas

### 11.1. Gerenciamento de Sessão

- **Sempre fazer logout** após concluir as operações para liberar recursos do FMG.
- Com API key (token-based), não há necessidade de login/logout.
- A sessão tem timeout configurável no FMG (`admintimeout`).

### 11.2. Tratamento de Erros

Sempre verificar `status.code` na resposta:
- `0` = Sucesso
- `-1` = Erro genérico
- `-3` = Sessão inválida/expirada (requer re-login)
- `-11` = Recurso não encontrado
- `-13` = Permissão negada
- `-23` = Objeto já existe
- `-61` = Validação falhou

### 11.3. Performance

- Use **`fields`** para selecionar apenas os atributos necessários.
- Use **`loadsub: 0`** quando não precisar de sub-tabelas.
- Use **multiplexing** para agrupar operações relacionadas.
- Use **`filter`** para reduzir o volume de dados retornados.
- Evite polling muito frequente de tasks (intervalo recomendado: 5s).

### 11.4. Paginação

Para tabelas grandes, use `sort` combinado com `filter` para paginar:

```json
{
  "url": "/pm/config/adom/root/obj/firewall/address",
  "sort": [["name", 1]],
  "filter": [["name", ">", "last_name"]]
}
```

### 11.5. Descoberta de Schema

Use `option: ["syntax"]` para descobrir programaticamente a estrutura de qualquer objeto, incluindo:
- Tipos de dados (`string`, `uint32`, `datasrc`, etc.)
- Valores padrão
- Limites (`alimit`)
- Referências a outras tabelas (`ref`)
- Opções disponíveis (`opts`)

### 11.6. Versionamento

- Diferentes versões de ADOM (6.2, 6.4, 7.0+) podem ter URLs diferentes.
- Exemplo: SD-WAN em ADOM 6.2 usa `virtual-wan-link`, enquanto 7.0+ usa `sdwan`.
- Sempre verificar a versão do ADOM antes de operar.

---

## 12. Referência Rápida de Variáveis

### 12.1. Variáveis de Ambiente (Postman)

| Variável | Descrição | Exemplo |
|---|---|---|
| `host` | IP/FQDN do FortiManager | `192.168.1.100` |
| `user` | Usuário admin | `admin` |
| `password` | Senha do usuário | `fortinet` |
| `fmg-session` | Session ID (auto-preenchido) | — |
| `adom` | Nome do ADOM | `root` |
| `device` | Nome do device gerenciado | `FGT1` |
| `vdom` | Nome do VDOM | `root` |
| `policy-package` | Nome do policy package | `default` |
| `device-admin` | Admin do device | `admin` |
| `device-password` | Senha do device | — |
| `device-ip` | IP do device | `10.0.0.1` |
| `group` | Nome do grupo de devices | `All_FortiGate` |
| `script` | Nome do script | `my_script` |
| `lastTask` | Último task ID (auto-preenchido) | — |
| `sdwan-profile` | Nome do perfil SD-WAN | `default` |
| `sdwan-zone` | Nome da zone SD-WAN | `zone1` |
| `normalized-iface` | Interface normalizada | `port2` |
| `ipsec-name` | Nome do túnel IPSec | `to_branch` |
| `address-name` | Nome do firewall address | `server1` |
| `address-ip` | IP do address | `10.0.0.1` |
| `meta-vdom-field-name` | Nome do meta field | `wan1_ip` |
| `meta-vdom-field-value` | Valor do meta field | `10.0.0.1` |

---

## 13. Diferenças entre Versões de ADOM

### 13.1. ADOM 6.2 vs 6.4 vs 7.0+

| Funcionalidade | ADOM 6.2 | ADOM 6.4 | ADOM 7.0+ |
|---|---|---|---|
| **SD-WAN** | `virtual-wan-link` | `sdwan` | `sdwan` (sem normalized interfaces) |
| **Zones SD-WAN** | Não existem | Sim | Sim |
| **Normalized interfaces** | Usadas no SD-WAN | Usadas no SD-WAN | Apenas via meta fields |
| **Meta fields** | Não disponíveis | Sim | Essenciais para SD-WAN |

### 13.2. SD-WAN: Mudanças Críticas na v7

Na versão 7 do ADOM:
- **Não** é mais possível usar "normalized interfaces" como membros do SD-WAN.
- Apenas **interfaces físicas** podem ser configuradas diretamente.
- Para simular o comportamento anterior, use **meta fields** (Device VDOM) com valores por device/vdom.
- Durante upgrade de v6 para v7, o FMG tenta converter a configuração automaticamente, mas pode ser necessário ajuste manual.

### 13.3. Compatibilidade de URLs

**ADOM 6.2 — Virtual WAN Link:**
```
/pm/config/adom/<adom>/wanprof/<profile>/system/virtual-wan-link
/pm/config/adom/<adom>/obj/dynamic/virtual-wan-link/members
```

**ADOM 6.4+ — SD-WAN:**
```
/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan
/pm/config/adom/<adom>/wanprof/<profile>/system/sdwan/members
```

---

## Apêndice A: Códigos de Status

| Código | Significado |
|---|---|
| 0 | Sucesso |
| -1 | Erro interno |
| -2 | Operação não suportada |
| -3 | Sessão inválida/expirada |
| -4 | Parâmetros inválidos |
| -5 | Recurso bloqueado |
| -11 | Recurso não encontrado |
| -13 | Permissão negada |
| -23 | Objeto já existe |
| -61 | Falha de validação |
| -101 | Timeout |
| -901 | Task não encontrada |

## Apêndice B: Referência CLI para API

| CLI FortiGate | URL da API |
|---|---|
| `config system dns` | `/pm/config/device/<dev>/global/system/dns` |
| `config system interface` | `/pm/config/device/<dev>/global/system/interface` |
| `config router static` | `/pm/config/device/<dev>/vdom/<vdom>/router/static` |
| `config firewall address` | `/pm/config/adom/<adom>/obj/firewall/address` |
| `config firewall service custom` | `/pm/config/adom/<adom>/obj/firewall/service/custom` |
| `config firewall policy` | `/pm/config/adom/<adom>/pkg/<pkg>/firewall/policy` |
| `config vpn ipsec phase1-interface` | `pm/config/device/<dev>/vdom/<vdom>/vpn/ipsec/phase1-interface` |
| `config system admin user` | `/cli/global/system/admin/user` |

---

*Documentação baseada na coleção Postman "FortiManager" e nos 24 capítulos de documentação técnica da API FortiManager JSON RPC.*