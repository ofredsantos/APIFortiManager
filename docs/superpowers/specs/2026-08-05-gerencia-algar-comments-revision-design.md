# Especificação de Design: Revisão de Comentários do Baseline de Gerência Algar (FortiGate)

**Data:** 05/08/2026  
**Arquivo Alvo:** `baseline/Gerencia Algar com 2 uplinks.md`  
**Objetivo:** Reestruturar os comentários do documento para servir como uma instrução estrita e executável para um Agente de IA de automação (FortiManager / FortiGate API / CLI), mantendo a clareza e legibilidade técnica para analistas humanos.

---

## 1. Visão Geral das Instruções Gerais (Bloco do Topo)

O comentário HTML inicial (`<!-- ... -->`) será transformado em um **Prompt de Sistema e Diretrizes Operacionais** para o agente de IA:

1. **Escopo e Propósito:** Definir o padrão oficial de gerência remota Algar para FortiGate (1 ou 2 uplinks WAN).
2. **Dicionário de Variáveis:**
   - `<int_uplink-1>`: Interface WAN principal (obrigatória).
   - `<int_uplink-2>`: Interface WAN secundária (opcional / condicional).
   - `<ip_loopback>`: IP exclusivo de gerenciamento da unidade (IPv4 sem máscara).
3. **Regras de Algoritmo e Execução do Agente de IA:**
   - **Condicional 1 vs 2 Uplinks:** Se `<int_uplink-2>` for nulo/ausente, desativar dinamicamente as etapas de `VPN.MGMT.02`, `VPN.MGMT.02.P2`, rotas de backup (prioridade 60) e a inclusão da interface 2 na zona `ZN.MGMT`.
   - **Isolamento de VRF:** Garantir que todas as interfaces de gerenciamento e a loopback operem estritamente na `vrf 1`.
   - **Idempotência & Verificação:** Checar a existência de objetos/interfaces antes de aplicar comandos destrutivos.
   - **Preservação de Segredos:** Tratar os blocos `ENC ...` (passwords e secrets) como valores literais sensíveis.
4. **Tabela de Nomenclatura Estrita:**
   - Túneis: `VPN.MGMT.01`, `VPN.MGMT.02`, `VPN.MGMT.01.P2`, `VPN.MGMT.02.P2`.
   - Interfaces & Zonas: `mgmt.algar` (loopback), `ZN.MGMT` (zone).
   - Address Objects: `MGMT.DC`, `MGMT.DC-2`, `MGMT.SPOKE`.
   - Policies & Profiles: `MGMT-INBOUND`, `api`, `api_soc`, `api_nava`, `algar_soc`, `algar_atv`, `operacao_soc`, `GRP.SOCAdmins`, `authenticatorfn01.algar`.

---

## 2. Estrutura dos Comentários das Tarefas (Etapas 1 a 13)

Cada uma das 13 etapas de configuração possuirá seu próprio bloco HTML (`<!-- ... -->`) posicionado antes do comando CLI correspondente. Todos os comentários seguirão a estrutura rigorosa de 4 tópicos:

```html
<!--
===============================================================================
ETAPA [X]: [NOME DA ETAPA]
===============================================================================
1. OBJETIVO:
   [Descrição do que esta etapa realiza no equipamento]

2. INSTRUÇÕES PARA O AGENTE DE IA:
   [Ações exatas de parsing, substituição de variáveis e condicionais (1 vs 2 uplinks)]

3. CONTEXTO DE USO & REGRAS:
   [Justificativa técnica dos parâmetros - VRF, prioridades, criptografia, etc.]

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   [O que deve ter sido executado antes e como validar o sucesso da etapa]
===============================================================================
-->
```

### Mapeamento Específico das 13 Etapas:

- **Etapa 1:** Substituição e validação de variáveis (`<int_uplink-1>`, `<int_uplink-2>`, `<ip_loopback>`).
- **Etapa 2:** Configuração dos túneis IPsec Phase 1 e Phase 2 (`VPN.MGMT.01`, `VPN.MGMT.02`, `src-subnet`).
- **Etapa 3:** Associação das interfaces IPsec à VRF 1.
- **Etapa 4:** Roteamento estático para a rede de gerenciamento (prioridades 50 e 60).
- **Etapa 5:** Criação e vinculação da Interface Zone `ZN.MGMT`.
- **Etapa 6:** Configuração da Interface Loopback `mgmt.algar` na VRF 1.
- **Etapa 7:** Integração com o servidor RADIUS `authenticatorfn01.algar`.
- **Etapa 8:** Criação do grupo de autenticação RADIUS `GRP.SOCAdmins`.
- **Etapa 9:** Ajuste do Admin Timeout global (`31` minutos).
- **Etapa 10:** Criação dos objetos de endereço `MGMT.DC`, `MGMT.DC-2` e `MGMT.SPOKE`.
- **Etapa 11:** Criação da política de firewall `MGMT-INBOUND`.
- **Etapa 12:** Configuração do perfil de acesso à API (`api`) com permissões `read`.
- **Etapa 13:** Provisionamento de usuários administrativos e vinculação aos `trusthost` e `accprofile`.

---

## 3. Plano de Verificação

1. **Inspeção de Sintaxe Markdown / HTML:** Garantir que todos os comentários estejam devidamente fechados e que o código CLI FortiOS permaneça intacto nos blocos de código.
2. **Revisão de Conteúdo:** Verificar se nenhuma regra do padrão Algar foi omitida ou distorcida.
3. **Leitura Pelo Agente:** Confirmar que o novo arquivo serve como instrução completa para automações futuras.
