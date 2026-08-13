# Automação de Atendimento Direto e Padronização de Firewalls (`Atividade/`)

> **Projeto**: Suíte de Automação de Atendimento e Governança de Gerência FortiGate  
> **Escopo**: ADOM `DOM_ATACAREJO` (FortiManager `187.72.197.227`)  
> **Cliente / Padrão Operacional**: Algar Telecom — Baseline de Gerência ([Gerencia Algar com 2 uplinks.md](file:///e:/Projetos/Dev/APIFortiManager/baseline/Gerencia%20Algar%20com%202%20uplinks.md))  

---

## 🎯 Visão Geral da Solução

Esta pasta reúne a solução completa de automação para atendimento direto, auditoria, exportação de backups brutos sanitizados e geração de **bilhetes de intervenção auditáveis** para os 28 firewalls FortiGate do ADOM `DOM_ATACAREJO`.

A solução foi projetada para garantir **risco zero de parada indevida**, aplicando o princípio da **não duplicação de configurações**, retenção inegociável de ponto de restauração (Etapa Zero) e fallback automático entre protocolos de comunicação.

---

## 📁 Arquitetura e Estrutura de Arquivos

```text
Atividade/
├── .env                       # Credenciais diretas dos firewalls (user e pass)
├── fortigate_client.py        # Cliente híbrido (REST API HTTPS com Fallback SSH CLI)
├── ticket_generator.py        # Gerador de bilhetes auditáveis e scripts deltas não duplicados
├── run_atividade.py           # Orquestrador de atendimento direto com trava de acesso ao vivo
├── sync_inventory.py          # Inventário de sincronia FortiManager e extração de IPs
├── main.py                    # Auditoria das 13 atividades de gerência Algar
├── DESIGN.md                  # Documento oficial de arquitetura e decisões do projeto
├── backups/                   # Repositório de backups brutos sanitizados (.conf)
└── bilhetes/                  # Repositório de bilhetes e playbooks por equipamento
```

---

## 🔐 1. Pré-Requisitos e Autenticação

### Dependências de Software
- **Python**: v3.9 ou superior.
- **Bibliotecas Python**:
  ```bash
  pip install requests urllib3 paramiko python-dotenv
  ```

### Arquivo de Credenciais (`Atividade/.env`)
As credenciais diretas de acesso aos equipamentos devem estar cadastradas no arquivo `Atividade/.env`:
```env
user: e_atalayac
pass: F3.HMtNA
```

---

## 🚀 2. Guia de Uso Rápido para Analistas

### A. Inventariar Sincronia e Mapear IPs dos Firewalls
Executa a varredura no FortiManager para extrair o status FGFM, a sincronia de banco de dados e os endereços IP de todos os firewalls do ADOM `DOM_ATACAREJO`:
```bash
python Atividade/sync_inventory.py
```
> **Saídas**:
> - Console: Matriz tabular executiva no terminal.
> - Relatórios em: `Atividade/reports/sync_inventory.csv` e `Atividade/reports/sync_inventory.md`.

---

### B. Auditar as 13 Atividades da Baseline nos Equipamentos
Verifica o estado atual dos 28 equipamentos do ADOM em relação às 13 atividades da baseline Algar:
```bash
python Atividade/main.py
```
> **Saídas**:
> - Console: Resumo de conformidade (`OK`, `PARCIAL`, `AUSENTE`).
> - Relatórios em: `Atividade/inventario/resumo_equipamentos.csv` e `Atividade/inventario/DOM_ATACAREJO/*.md`.

---

### C. Executar Atendimento Direto em um Firewall Alvo (`run_atividade.py`)
Realiza a validação ao vivo com um equipamento específico (iniciando por padrão no IP de testes `187.72.59.197`), exporta o backup bruto sanitizado e gera **exclusivamente o bilhete desse equipamento**:

```bash
# Execução direta para o IP alvo (Modo Rápido)
python Atividade/run_atividade.py --ip 187.72.59.197
```

```bash
# Execução para Qualquer Outro Firewall do ADOM
python Atividade/run_atividade.py --ip 189.112.141.25
```

```bash
# Execução com Simulação de Janela de Analista (30 minutos de pacing)
python Atividade/run_atividade.py --ip 187.72.59.197 --mode simulate
```

```bash
# Geração da Suíte Completa de Bilhetes para Todos os Equipamentos
python Atividade/run_atividade.py --ip 187.72.59.197 --all
```

---

## 🛡️ 3. Mecanismos de Proteção e Resiliência

### 🟢 Conectividade Híbrida com Fallback Automático
1. **Canal Principal (REST API - HTTPS:443)**: O script tenta login nativo via REST API (`/api/v2/login`) obtendo cookie `CCSID` e token CSRF.
2. **Fallback Automático (SSH CLI - SSH:22)**: Se o HTTPS estiver desativado na WAN ou der timeout, o cliente aciona **imediatamente o fallback SSH CLI via Paramiko**, autenticando e executando comandos nativos de CLI sem interromper o atendimento.

### ⛔ Trava de Conexão Ao Vivo (Live Connection Gate)
O orquestrador exige validação de conectividade real antes de gerar qualquer arquivo. Se um equipamento estiver offline ou inacessível (REST API e SSH falharem), a execução é **abortada imediatamente**, impedindo a criação de bilhetes não validados.

### 🧹 Sanitização Inegociável de Backup (`sanitize_fortigate_config`)
Os backups `.conf` gerados via SSH CLI são higienizados automaticamente em tempo de execução:
- **Linha 1 Limpa**: Garante que o arquivo inicie estritamente com o cabeçalho oficial `#config-version=...` (removendo o prompt do hostname).
- **Purga de `--More--`**: Remove todas as marcações de paginação de terminal `--More--`, garantindo que o arquivo seja 100% válido para restauração via `execute restore config`.

---

## 🔄 4. Procedimentos de Rollback e Contingência

Cada bilhete gerado em `Atividade/bilhetes/bilhete_<hostname>.md` contém duas estratégias de rollback:

### 1. Soft Rollback (Reversão Suave sem Reboot)
Comandos CLI para remoção pontual apenas dos objetos que foram adicionados pela atividade:
```fortinet
config firewall policy
  delete [ID_POLICY_MGMT_INBOUND]
end
config user group
  delete "GRP.SOCAdmins"
end
config user radius
  delete "authenticatorfn01.algar"
end
config system zone
  delete "ZN.MGMT"
end
config system interface
  delete "mgmt.algar"
end
config vpn ipsec phase1-interface
  delete "VPN.MGMT.01"
  delete "VPN.MGMT.02"
end
```

### 2. Hard Rollback (Restauração do Backup Bruto Full)
Em caso de contingência severa ou perda de conectividade:
1. Localizar o arquivo `.conf` gerado na pasta `Atividade/backups/` durante a Etapa Zero.
2. Executar via CLI ou TFTP/REST API:
   ```fortinet
   execute restore config tftp <nome_do_arquivo>.conf <ip_tftp>
   ```

---

## 📋 5. Checklist das 13 Provas de Conceito (Pós-Intervenção)

Após aplicar o bilhete no equipamento, execute os comandos de verificação para validar a conformidade com a baseline Algar:

| # | Requisito Baseline | Comando de Validação CLI | Resultado Esperado |
| :---: | :--- | :--- | :--- |
| **1** | Mapeamento de Variáveis | `get system interface` | WAN1 e WAN2 ativas e UP |
| **2** | Túneis IPsec | `get vpn ipsec tunnel summary` | `VPN.MGMT.01` (e `VPN.MGMT.02`) em estado UP |
| **3** | VRF 1 nos Túneis | `get system interface VPN.MGMT.01` | Parâmetro `vrf: 1` |
| **4** | Roteamento Estático | `get router info routing-table vrf 1` | Rotas `198.19.0.0/26` e `198.19.255.0/24` |
| **5** | Zone `ZN.MGMT` | `get system zone ZN.MGMT` | Interfaces `VPN.MGMT.01/02` associadas |
| **6** | Interface Loopback | `get system interface mgmt.algar` | Interface UP em VRF 1 com IP designado |
| **7** | Servidor RADIUS | `diagnose test authserver radius authenticatorfn01.algar pap <user> <pass>` | Retorno `successful` do RADIUS |
| **8** | Grupo `GRP.SOCAdmins` | `get user group GRP.SOCAdmins` | Membro `authenticatorfn01.algar` e match `Grp_SOC_Operacao` |
| **9** | Admin Timeout Global | `get system global` | `admintimeout: 31` |
| **10**| Address Objects | `get firewall address MGMT.DC` | Sub-redes `198.19.0.0/26` e `<ip_loopback>` |
| **11**| Policy `MGMT-INBOUND` | `get firewall policy` | Regra `MGMT-INBOUND` habilitada de `ZN.MGMT` para `mgmt.algar` |
| **12**| Perfil REST API | `get system accprofile api` | Perfil `api` com permissões de leitura ativadas |
| **13**| Usuários Admin | `get system admin` | Contas `api_soc`, `algar_soc`, `algar_atv`, `operacao_soc` criadas |

---

## 👨‍💻 Suporte e Contato

Para dúvidas ou relatórios de divergência em janelas operacionais, consulte o arquivo [DESIGN.md](file:///e:/Projetos/Dev/APIFortiManager/Atividade/DESIGN.md) ou acione a equipe de Engenharia de Automação / SOC Algar.
