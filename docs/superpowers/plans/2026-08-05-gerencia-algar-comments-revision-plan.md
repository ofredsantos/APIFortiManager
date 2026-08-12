# Plano de Implementação: Revisão de Comentários do Baseline de Gerência Algar (FortiGate)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reestruturar os comentários do arquivo `baseline/Gerencia Algar com 2 uplinks.md` para fornecer diretrizes estritas a um Agente de IA de automação FortiManager/FortiGate e documentação técnica para engenheiros humanos.

**Architecture:** Atualização direta do documento Markdown através de inserção de comentários HTML (`<!-- ... -->`) contendo instruções de algoritmo, parsing de variáveis, isolamento em VRF 1, tratamento de 1 vs 2 uplinks e os 4 tópicos padrão por tarefa.

**Tech Stack:** Markdown, HTML comments, FortiOS CLI Syntax.

## Global Constraints

- Manter o código CLI FortiOS exatamente como definido originalmente.
- Formatar todos os comentários utilizando blocos de comentário HTML (`<!-- ... -->`).
- Cada comentário de etapa deve conter obrigatoriamente os 4 tópicos: Objetivo, Instruções para o Agente de IA, Contexto de Uso & Regras, e Validação & Pré-requisitos.
- Fornecer regras explícitas para execução condicional quando o equipamento possuir apenas 1 link WAN (`DUAL_UPLINK=False`).

---

### Task 1: Atualização do Bloco de Instruções Gerais no Topo do Arquivo

**Files:**
- Modify: `baseline/Gerencia Algar com 2 uplinks.md:3-51`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-08-05-gerencia-algar-comments-revision-design.md`
- Produces: Prompt de Sistema e Guia Operacional do Agente de IA no topo do arquivo `baseline/Gerencia Algar com 2 uplinks.md`.

- [ ] **Step 1: Escrever o novo bloco de comentário HTML inicial**

Substituir o comentário inicial (linhas 3 a 51) pelo prompt de sistema estruturado contendo:
- Contexto e objetivo do padrão Algar.
- Dicionário de Variáveis (`<int_uplink-1>`, `<int_uplink-2>`, `<ip_loopback>`).
- Lógica de algoritmo (Tratamento de 1 vs 2 uplinks, isolamento em VRF 1, idempotência e tratamento de secrets `ENC ...`).
- Tabela estrita de nomenclatura de objetos e interfaces.

- [ ] **Step 2: Verificar a formatação do bloco inicial**

Executar a leitura do trecho modificado para assegurar que as tags HTML `<!--` e `-->` fecham corretamente antes da seção `## Etapas de Configuração`.

- [ ] **Step 3: Commit**

```bash
git add "baseline/Gerencia Algar com 2 uplinks.md"
git commit -m "docs: update general AI agent instructions header in baseline"
```

---

### Task 2: Inserção de Comentários Detalhados nas Etapas 1 a 6

**Files:**
- Modify: `baseline/Gerencia Algar com 2 uplinks.md`

**Interfaces:**
- Consumes: Estrutura dos 4 tópicos padrão definidos no Design Spec.
- Produces: Comentários de IA/Humanos para as Etapas 1 (Variáveis), 2 (IPsec Phase 1/2), 3 (VRF 1 Binding), 4 (Rotas Estáticas), 5 (Zone ZN.MGMT) e 6 (Loopback mgmt.algar).

- [ ] **Step 1: Adicionar comentário da Etapa 1 (Variáveis)**
Inserir bloco `<!-- ... -->` detalhando o parsing de `<int_uplink-1>`, `<int_uplink-2>` e `<ip_loopback>`, e definindo a variável booleana `DUAL_UPLINK`.

- [ ] **Step 2: Adicionar comentário da Etapa 2 (Túneis IPsec Phase 1 e 2)**
Inserir bloco `<!-- ... -->` orientando a criação de `VPN.MGMT.01` e condicionalmente `VPN.MGMT.02` se `DUAL_UPLINK=True`.

- [ ] **Step 3: Adicionar comentário da Etapa 3 (VRF 1 Binding)**
Inserir bloco `<!-- ... -->` instruindo a atribuição das interfaces de túnel à VRF 1.

- [ ] **Step 4: Adicionar comentário da Etapa 4 (Rotas Estáticas de Gerência)**
Inserir bloco `<!-- ... -->` detalhando as rotas para `198.19.0.0/26` e `198.19.255.0/24` com prioridades 50 (principal) e 60 (backup).

- [ ] **Step 5: Adicionar comentário da Etapa 5 (Zone ZN.MGMT)**
Inserir bloco `<!-- ... -->` explicando a criação da zona de segurança agregadora de túneis.

- [ ] **Step 6: Adicionar comentário da Etapa 6 (Loopback mgmt.algar)**
Inserir bloco `<!-- ... -->` orientando a criação da interface de terminação gerencial com IP exclusivo em VRF 1.

- [ ] **Step 7: Commit**

```bash
git add "baseline/Gerencia Algar com 2 uplinks.md"
git commit -m "docs: add structured comments for steps 1 to 6"
```

---

### Task 3: Inserção de Comentários Detalhados nas Etapas 7 a 13

**Files:**
- Modify: `baseline/Gerencia Algar com 2 uplinks.md`

**Interfaces:**
- Consumes: Estrutura dos 4 tópicos padrão definidos no Design Spec.
- Produces: Comentários de IA/Humanos para as Etapas 7 (RADIUS), 8 (User Group), 9 (Admin Timeout), 10 (Address Objects), 11 (Firewall Policy), 12 (API Profile) e 13 (Usuários Administrativos).

- [ ] **Step 1: Adicionar comentário da Etapa 7 (RADIUS Server)**
Inserir bloco `<!-- ... -->` detalhando a configuração do servidor `authenticatorfn01.algar` com `source-ip` vinculada à `<ip_loopback>`.

- [ ] **Step 2: Adicionar comentário da Etapa 8 (User Group GRP.SOCAdmins)**
Inserir bloco `<!-- ... -->` orientando o mapeamento do grupo RADIUS `Grp_SOC_Operacao`.

- [ ] **Step 3: Adicionar comentário da Etapa 9 (Global Admin Timeout)**
Inserir bloco `<!-- ... -->` com justificativa operacional do timeout de 31 minutos.

- [ ] **Step 4: Adicionar comentário da Etapa 10 (Address Objects)**
Inserir bloco `<!-- ... -->` para a criação de `MGMT.DC`, `MGMT.DC-2` e `MGMT.SPOKE`.

- [ ] **Step 5: Adicionar comentário da Etapa 11 (Firewall Policy MGMT-INBOUND)**
Inserir bloco `<!-- ... -->` descrevendo a liberação de tráfego de `ZN.MGMT` para `mgmt.algar`.

- [ ] **Step 6: Adicionar comentário da Etapa 12 (API Access Profile)**
Inserir bloco `<!-- ... -->` detalhando o perfil de leitura `api`.

- [ ] **Step 7: Adicionar comentário da Etapa 13 (Usuários Administrativos)**
Inserir bloco `<!-- ... -->` detalhando o provisionamento de `api_soc`, `api_nava`, `algar_soc`, `algar_atv` e `operacao_soc` com seus respectivos `trusthost` e perfis.

- [ ] **Step 8: Commit**

```bash
git add "baseline/Gerencia Algar com 2 uplinks.md"
git commit -m "docs: add structured comments for steps 7 to 13"
```

---

### Task 4: Validação Final e Inspeção de Integridade

**Files:**
- View: `baseline/Gerencia Algar com 2 uplinks.md`

**Interfaces:**
- Consumes: Arquivo final editado.
- Produces: Confirmação de integridade sintática e semântica.

- [ ] **Step 1: Realizar leitura completa do arquivo atualizado**
Conferir se todas as tags `<!--` e `-->` estão pareadas e se os blocos de código FortiOS estão íntegros e funcionais.

- [ ] **Step 2: Commit final de conclusão**

```bash
git add "baseline/Gerencia Algar com 2 uplinks.md"
git commit -m "docs: complete revision of comments in gerencia algar baseline"
```
