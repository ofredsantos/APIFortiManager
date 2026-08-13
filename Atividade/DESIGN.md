# Documento de Arquitetura e Design: Automação de Atendimento Direto aos Firewalls (`Atividade/`)

## 1. Resumo do Entendimento (Understanding Summary)

- **Objetivo**: Implementar uma automação robusta, segura e auditável na pasta `Atividade/` para realizar inspeção, backup completo em formato `export`, auditoria das 13 atividades da baseline Algar (Gerencia Algar com 2 uplinks.md) e geração de **bilhetes/playbooks de intervenção por equipamento** para os 28 firewalls do ADOM `DOM_ATACAREJO`.
- **Equipamento de Validação Inicial**: `187.72.59.197` (`cl-fw-ama-DOM-111-Araruama`).
- **Público-Alvo**: Equipes de engenharia de redes, SOC e implantação Algar.

---

## 2. Premissas e Restrições (Assumptions & Constraints)

1. **Protocolo de Comunicação**: Atuação direta no FortiGate via **REST API nativa do FortiOS** (`/api/v2/login` com sessão HTTP/cookie). SSH/CLI mantido estritamente como fallback extremo.
2. **Isolamento do FortiManager**: Atuação 100% direta nos equipamentos (sem chamadas ou re-sync no FortiManager durante esta janela).
3. **Não Duplicação & Idempotência**: Se uma configuração ou objeto equivalente já existir (interfaces, fases IPsec, zonas, objetos de endereço, políticas), o bilhete/script não criará duplicatas; irá validar e complementar apenas o que estiver ausente.
4. **Backup & Rollback Inegociável**: Backup completo da configuração (`/api/v2/monitor/system/config/backup?scope=global`) exportado antes de qualquer leitura/alteração. Geração de script de reversão limpa (sem reboot) + restauração de backup full em caso de contingência.
5. **Variáveis por Equipamento**: Interfaces WAN1 (`<int_uplink-1>`) e WAN2 (`<int_uplink-2>`) descobertas automaticamente via REST API. Para a Loopback (`<ip_loopback>`), o IP é reaproveitado se a interface existir; se for ausente, o bilhete deixará a tag `<ip_loopback>` sinalizada para preenchimento manual pelo operador.

---

## 3. Registro de Decisões (Decision Log)

| Decisão | Opções Consideradas | Razão da Escolha |
| :--- | :--- | :--- |
| **Método de Conexão** | 1. REST API (/api/v2/login) [Escolhida]<br>2. SSH CLI (Netmiko) | A REST API oferece comunicação HTTPS estruturada, nativa e segura para backup bruto e inspeção. |
| **Arquitetura da Solução** | 1. Gerador de Bilhetes Auditáveis + Módulos Python [Escolhida]<br>2. Execução Inline Direta | A geração de bilhetes prévia permite revisão humana auditável de cada comando antes de executar na rede. |
| **Sincronia FortiManager** | 1. Operação Isolada no FortiGate [Escolhida]<br>2. Re-sync via API do FMG | Foco 100% no FortiGate direto sem introduzir dependências com o FMG durante a janela. |
| **Descoberta de Variáveis** | 1. Descoberta Automática via REST API com Fallback para Tabela [Escolhida]<br>2. De-Para Estático Manual | Reduz o trabalho manual a zero para WANs e reaproveita o IP de loopback existente quando presente. |
| **Simulação de Analista** | 1. Fluxo Cadenciado de 30 min por Equipamento com Pacing [Escolhida]<br>2. Execução Instantânea em Lote | Simula com precisão o tempo de preparação, execução e pós-validação de uma janela operacional de analista. |

---

## 4. Estrutura dos Módulos da Solução (`Atividade/`)

```text
Atividade/
├── .env                       # Credenciais user/pass dos firewalls
├── fortigate_client.py        # Cliente REST API (login, backup, discovery de WAN/Loopback)
├── ticket_generator.py        # Gerador de bilhetes auditáveis MD/CLI com análise de deltas
├── run_atividade.py           # Orquestrador com simulação de janela (30 min) e 13 checagens
├── backups/                   # Repositório dos arquivos de backup .conf brutos
└── bilhetes/                  # Bilhetes de intervenção e scripts de rollback por equipamento
```

---

## 5. Tabela das 13 Atividades e Comandos de Verificação

| Etapa | Atividade Baseline | Comando de Verificação / Prova de Conceito |
| :---: | :--- | :--- |
| **1** | Mapeamento de Variáveis | `get system interface` (Verificação de WAN1/WAN2 ativas) |
| **2** | Túneis IPsec (`VPN.MGMT.01/02`) | `get vpn ipsec tunnel summary` / `diagnose vpn tunnel list` |
| **3** | Interfaces vinculadas à VRF 1 | `get system interface VPN.MGMT.01` (Confirmar `vrf: 1`) |
| **4** | Roteamento Estático (VRF 1) | `get router info routing-table vrf 1` |
| **5** | Zone `ZN.MGMT` | `get system zone ZN.MGMT` |
| **6** | Interface Loopback (`mgmt.algar`) | `get system interface mgmt.algar` (Confirmar IP e VRF 1) |
| **7** | Servidor RADIUS (`authenticatorfn01.algar`) | `diagnose test authserver radius authenticatorfn01.algar pap test_user test_pass` |
| **8** | Grupo de Usuários (`GRP.SOCAdmins`) | `get user group GRP.SOCAdmins` |
| **9** | Admin Timeout Global (`31 min`) | `get system global` (Confirmar `admintimeout: 31`) |
| **10**| Address Objects (`MGMT.DC`, `SPOKE`) | `get firewall address MGMT.DC` e `MGMT.SPOKE` |
| **11**| Policy `MGMT-INBOUND` | `get firewall policy` (Filtrar regra `MGMT-INBOUND`) |
| **12**| Perfil REST API (`api`) | `get system accprofile api` |
| **13**| Usuários Administradores Locais/API | `get system admin` (Confirmar `api_soc`, `algar_soc`, etc.) |
