# Procedimento de Configuração do Gerenciamento do FortiGate pela Algar

<!-- 
===============================================================================
DIRECTIVAS GERAIS DE PADRONIZAÇÃO DO GERENCIAMENTO ALGAR (FORTIGATE)
===============================================================================

1. ESCOPO E OBJETIVO:
   Este documento especifica o procedimento padrão oficial para implantação e
   padronização da infraestrutura de gerenciamento remoto dos equipamentos 
   FortiGate sob responsabilidade da Algar Telecom.
   
   O procedimento contempla ambientes que possuem 1 (um) ou 2 (dois) uplinks WAN
   ativos e estabelece o isolamento do tráfego gerencial em tabela de roteamento 
   dedicada (VRF 1) e interface de terminação em Loopback.

2. DICIONÁRIO DE VARIÁVEIS DE ENTRADA (AGENT PARSING):
   Antes de aplicar as configurações, o agente de automação deve obrigatoriamente 
   receber e validar o valor das seguintes variáveis:
   
   - <int_uplink-1> : [Obrigatório] Nome exato da interface física/lógica WAN principal.
   - <int_uplink-2> : [Opcional/Condicional] Nome exato da segunda interface WAN.
                      Caso o equipamento possua apenas 1 link WAN, esta variável
                      deve ser nula/em branco, ativando a regra DUAL_UPLINK=False.
   - <ip_loopback>  : [Obrigatório] Endereço IPv4 único (máscara /32 implicitamente)
                      designado para a gerência da unidade.

3. REGRAS DE EXECUÇÃO E ALGORITMO PARA AGENTES DE IA:
   - Condicional DUAL_UPLINK:
     * SE <int_uplink-2> estiver presente e válido (DUAL_UPLINK=True):
       Criar túneis VPN.MGMT.01 e VPN.MGMT.02, Phase2 correspondentes, associar
       ambas as interfaces à VRF 1, criar rotas de prioridade 50 (link 1) e 60 
       (link 2) e adicionar ambas as interfaces na Zone ZN.MGMT.
     * SE <int_uplink-2> for nulo/indefinido (DUAL_UPLINK=False):
       Criar apenas o túnel VPN.MGMT.01 / VPN.MGMT.01.P2, omitindo qualquer
       referência ao túnel 02 (Phase 1, Phase 2, rotas com prioridade 60 e 
       membro 02 na Zone ZN.MGMT).
   
   - Isolamento em VRF 1:
     * As interfaces dos túneis VPN.MGMT.* e a interface de loopback mgmt.algar
       DEVEM obrigatoriamente ser vinculadas à VRF 1 (set vrf 1).
     * O tráfego de gerenciamento e RADIUS trafega exclusivamente na VRF 1.

   - Preservação de Segredos & Idempotência:
     * As chaves Pre-Shared Key (psksecret) e senhas criptografadas em formato 
       FortiOS (ENC ...) NUNCA devem ser alteradas ou decodificadas; devem ser 
       aplicadas exatamente como literais presentes neste documento.
     * Antes de criar qualquer objeto ou política, validar se os mesmos já 
       existem no equipamento para evitar duplicações destrutivas.

4. PADRÃO ESTREITO DE NOMENCLATURA:
   - Túneis IPsec Phase 1: "VPN.MGMT.01" (Principal), "VPN.MGMT.02" (Secundário)
   - Túneis IPsec Phase 2: "VPN.MGMT.01.P2" (Principal), "VPN.MGMT.02.P2" (Secundário)
   - Interface Zone: "ZN.MGMT"
   - Interface Loopback: "mgmt.algar"
   - Address Objects: "MGMT.DC" (198.19.0.0/26), "MGMT.DC-2" (198.19.255.0/24),
                      "MGMT.SPOKE" (<ip_loopback>/32)
   - Firewall Policy: "MGMT-INBOUND"
   - Servidor RADIUS: "authenticatorfn01.algar" (198.19.255.10)
   - Grupo de Usuários: "GRP.SOCAdmins" (match "Grp_SOC_Operacao")
   - Perfil de API: "api"
   - Usuários Admin: "api_soc", "api_nava", "algar_soc", "algar_atv", "operacao_soc"
===============================================================================
-->

## Etapas de Configuração

<!--
===============================================================================
ETAPA 1: MAPEAMENTO E SUBSTITUIÇÃO DE VARIÁVEIS DO SCRIPT
===============================================================================
1. OBJETIVO:
   Definir e instanciar as variáveis obrigatórias e condicionais de rede que
   personalizam as configurações do FortiGate para a unidade consumidora.

2. INSTRUÇÕES GERAIS:
   - Extrair e validar o valor das 3 variáveis de ambiente:
     * <int_uplink-1>: Nome exato da interface física/WAN principal (ex: port1, wan1).
     * <int_uplink-2>: Nome exato da interface física/WAN secundária (ex: port2, wan2).
     * <ip_loopback>: Endereço IPv4 válido (ex: 10.200.1.50), fornecido sem a máscara.
   - SE <int_uplink-2> estiver em branco ou indefinido, setar a flag DUAL_UPLINK = False.
     Caso contrário, setar DUAL_UPLINK = True.
   - Realizar a substituição textual exata das tags em todo o script antes da aplicação.

3. CONTEXTO DE USO & REGRAS:
   - A interface de loopback servirá como origem e término de todo o tráfego gerencial,
     enquanto os uplinks servirão como transporte dos túneis IPsec.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: As interfaces <int_uplink-1> (e <int_uplink-2>, se houver) devem
     existir no inventário físico/lógico do FortiGate.
   - Validação: Confirmar que o endereço IP informado para a loopback é exclusivo.
===============================================================================
-->
1. Substituir as variáveis utilizadas nos scripts de configuração.

<int_uplink-1> = Primeira interface Wan
<int_uplink-2> = Segunda interface Wan
<ip_loopback> = Ip de loopback designado para a unidade sem a mascara.

<!--
===============================================================================
ETAPA 2: CONFIGURAÇÃO DOS TÚNEIS IPSEC DE GERENCIAMENTO (PHASE 1 E PHASE 2)
===============================================================================
1. OBJETIVO:
   Estabelecer os túneis de criptografia IPsec responsáveis por transportar com
   segurança o tráfego de gerenciamento entre o FortiGate e os Datacenters Algar.

2. INSTRUÇÕES GERAIS:
   - Aplicar a configuração da Phase 1 (VPN.MGMT.01) e Phase 2 (VPN.MGMT.01.P2)
     utilizando a interface <int_uplink-1>.
   - SE DUAL_UPLINK = True:
     Aplicar também as configurações de Phase 1 (VPN.MGMT.02) e Phase 2 
     (VPN.MGMT.02.P2) utilizando a interface <int_uplink-2>.
   - SE DUAL_UPLINK = False:
     Pular/omitir os blocos edit "VPN.MGMT.02" e edit "VPN.MGMT.02.P2".
   - Substituir <ip_loopback> em src-subnet no formato "<ip_loopback> 255.255.255.255".
   - Manter as chaves psksecret literais (formato ENC ...).

3. CONTEXTO DE USO & REGRAS:
   - Usa modo agressivo com peerid/localid "mgmt01" e "mgmt02".
   - Proposta de criptografia: AES128-SHA1, Diffie-Hellman Group 5.
   - DPD ativado em idle (dpd on-idle).

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Verificar via CLI se a interface IPsec virtual "VPN.MGMT.01" 
     (e "VPN.MGMT.02") foi criada.
===============================================================================
-->
2. Configurar os túneis IPsec de gerenciamento, conforme a quantidade de uplinks disponíveis.

```
config vpn ipsec phase1-interface
edit "VPN.MGMT.01"
set interface "<int_uplink-1>"
set mode aggressive
set peertype one
set peerid "mgmt01"
set proposal aes128-sha1
set localid "mgmt01"
set dpd on-idle
set dhgrp 5
set remote-gw 189.112.0.244
set psksecret ENC lcoIKHaj1+QbySR417wUBGOl0xmZ9x7rarBCNANLpNl6pwh3hKAGQsHRV1IC/9HhdCDf6bfsm7Ve9IO9hnir2rWIA3X03T4V3VhG0TqXw9FZTTuvgzrUEOVYdlBBEOFvt1wt+XgwSzJkNPZOsiHOKlKGUWoKTgKiVwA9QPgYIPhBXxIXaEgcjOsW31HGLl8Tcf2hXg==
next
edit "VPN.MGMT.02"
set interface "<int_uplink-2>"
set mode aggressive
set peertype one
set peerid "mgmt02"
set proposal aes128-sha1
set localid "mgmt02"
set dhgrp 5
set remote-gw 189.112.0.244
set psksecret ENC lcoIKHaj1+QbySR417wUBGOl0xmZ9x7rarBCNANLpNl6pwh3hKAGQsHRV1IC/9HhdCDf6bfsm7Ve9IO9hnir2rWIA3X03T4V3VhG0TqXw9FZTTuvgzrUEOVYdlBBEOFvt1wt+XgwSzJkNPZOsiHOKlKGUWoKTgKiVwA9QPgYIPhBXxIXaEgcjOsW31HGLl8Tcf2hXg==
next
end

config vpn ipsec phase2-interface
edit "VPN.MGMT.01.P2"
set phase1name "VPN.MGMT.01"
set proposal aes128-sha1
set dhgrp 5
set auto-negotiate enable
set src-subnet <ip_loopback> 255.255.255.255
next
edit "VPN.MGMT.02.P2"
set phase1name "VPN.MGMT.02"
set proposal aes128-sha1
set dhgrp 5
set auto-negotiate enable
set src-subnet <ip_loopback> 255.255.255.255
next
end
```

<!--
===============================================================================
ETAPA 3: ATRIBUIÇÃO DAS INTERFACES DOS TÚNEIS À VRF 1
===============================================================================
1. OBJETIVO:
   Isolar as interfaces virtuais dos túneis IPsec na VRF 1 (Virtual Routing and
   Forwarding), separando a tabela de roteamento de gerência da tabela default (VRF 0).

2. INSTRUÇÕES GERAIS:
   - Executar 'config system interface' e aplicar 'set vrf 1' em VPN.MGMT.01.
   - SE DUAL_UPLINK = True:
     Aplicar também 'set vrf 1' na interface VPN.MGMT.02.
   - SE DUAL_UPLINK = False:
     Omitir o bloco edit VPN.MGMT.02.

3. CONTEXTO DE USO & REGRAS:
   - O isolamento em VRF 1 é mandatória no padrão Algar para impedir que falhas de
     roteamento na tabela default afetem o acesso gerencial do SOC/NOC.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: Etapa 2 concluída (túneis criados).
   - Validação: Executar 'get system interface VPN.MGMT.01' e checar 'vrf: 1'.
===============================================================================
-->
3. Ajustar as interfaces dos túneis IPsec, associando-as à VRF 1.

```
config system interface
edit VPN.MGMT.01
set vrf 1
next
edit VPN.MGMT.02
set vrf 1
next
end
```
<!--
===============================================================================
ETAPA 4: ROTEAMENTO ESTÁTICO DE GERENCIAMENTO (VRF 1 E PRIORIZAÇÃO DE LINKS)
===============================================================================
1. OBJETIVO:
   Configurar as rotas estáticas apontando para as sub-redes dos Datacenters Algar
   (198.19.0.0/26 e 198.19.255.0/24) através dos túneis IPsec na VRF 1.

2. INSTRUÇÕES GERAIS:
   - Criar rotas para os dois destinos vinculadas ao dispositivo "VPN.MGMT.01"
     com 'distance 10' e 'priority 50'.
   - SE DUAL_UPLINK = True:
     Criar rotas para os dois mesmos destinos vinculadas ao dispositivo "VPN.MGMT.02"
     com 'distance 10' e 'priority 60' (link de backup).
   - SE DUAL_UPLINK = False:
     Omitir as duas rotas referentes a "VPN.MGMT.02".

3. CONTEXTO DE USO & REGRAS:
   - Menor valor de priority (50 vs 60) garante que o tráfego gerencial flua
     preferencialmente pelo túnel 1 (WAN 1). Em caso de queda, o túnel 2 assume automaticamente.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Executar 'get router info routing-table all' ou 'get router info routing-table vrf 1'.
===============================================================================
-->
4. Criar as rotas estáticas necessárias para o tráfego de gerenciamento, considerando cada túnel IPsec configurado.

```
config router static
edit 0
set dst 198.19.0.0 255.255.255.192
set priority 50
set distance 10
set device "VPN.MGMT.01"
next
edit 0
set dst 198.19.255.0 255.255.255.0
set priority 50
set distance 10
set device "VPN.MGMT.01"
next
edit 0
set dst 198.19.0.0 255.255.255.192
set priority 60
set distance 10
set device "VPN.MGMT.02"
next
edit 0
set dst 198.19.255.0 255.255.255.0
set priority 60
set distance 10
set device "VPN.MGMT.02"
next
end
```

<!--
===============================================================================
ETAPA 5: CRIAÇÃO DA INTERFACE ZONE (ZN.MGMT)
===============================================================================
1. OBJETIVO:
   Agrupar as interfaces de túnel IPsec em uma Zone de firewall ("ZN.MGMT") para
   simplificar a aplicação de regras de segurança padronizadas.

2. INSTRUÇÕES GERAIS:
   - Executar 'config system zone' e criar/editar "ZN.MGMT".
   - SE DUAL_UPLINK = True:
     Setar 'set interface "VPN.MGMT.01" "VPN.MGMT.02"'.
   - SE DUAL_UPLINK = False:
     Setar 'set interface "VPN.MGMT.01"'.

3. CONTEXTO DE USO & REGRAS:
   - Permite que a política de firewall referencie uma única zona de origem (ZN.MGMT)
     independentemente de qual túnel o tráfego esteja trafegando.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Checar se a Zone ZN.MGMT contém as interfaces de túnel ativas.
===============================================================================
-->
5. Criar uma Interface Zone e adicionar as interfaces dos túneis IPsec para padronização das políticas de segurança.

```
config system zone
edit "ZN.MGMT"
set interface "VPN.MGMT.01" "VPN.MGMT.02"
next
end
```

<!--
===============================================================================
ETAPA 6: CRIAÇÃO DA INTERFACE LOOPBACK DE GERENCIAMENTO (mgmt.algar)
===============================================================================
1. OBJETIVO:
   Criar a interface lógica de Loopback ("mgmt.algar") com IP exclusivo, associada 
   à VRF 1, servindo como destino e origem de todos os serviços de gerência.

2. INSTRUÇÕES GERAIS:
   - Criar a interface "mgmt.algar" com os seguintes parâmetros fixos:
     * vdom "root"
     * vrf 1
     * type loopback
     * role dmz
     * allowaccess ping https ssh http fgfm
   - Substituir <ip_loopback> no parâmetro: 'set ip <ip_loopback> 255.255.255.255'.

3. CONTEXTO DE USO & REGRAS:
   - O protocolo FGFM (FortiManager) e acessos de gerência (SSH/HTTPS) respondem
     neste IP de loopback exclusivo e protegido.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Testar conectividade (ping) e verificar se a interface está UP em VRF 1.
===============================================================================
-->
6. Criar a interface Loopback destinada ao gerenciamento.

```
config system interface
edit "mgmt.algar"
set vdom "root"
set vrf 1
set ip <ip_loopback> 255.255.255.255
set allowaccess ping https ssh http fgfm
set type loopback
set role dmz
next
end
```
<!--
===============================================================================
ETAPA 7: CONFIGURAÇÃO DO SERVIDOR RADIUS (authenticatorfn01.algar)
===============================================================================
1. OBJETIVO:
   Integrar o FortiGate ao servidor de autenticação centralizada RADIUS da Algar.

2. INSTRUÇÕES GERAIS:
   - Criar/editar a entrada "authenticatorfn01.algar" em 'config user radius'.
   - Definir os parâmetros fixos:
     * server: "198.19.255.10"
     * secret: "ZFT4paKPt8Qh!CkTGcmR" (aplicar como literal)
     * auth-type: pap
   - Substituir <ip_loopback> no campo 'set source-ip <ip_loopback>'.

3. CONTEXTO DE USO & REGRAS:
   - O parâmetro 'source-ip' com o IP de loopback garante que os pacotes RADIUS
     sejam roteados através da VRF 1 via túnel IPsec, correspondendo à IP liberada no servidor.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: Etapa 6 (loopback criada).
   - Validação: Testar autenticação via CLI ('diagnose test authserver radius authenticatorfn01.algar pap <user> <pass>').
===============================================================================
-->
7. Configurar a integração com o servidor RADIUS da Algar.

```
config user radius 
edit "authenticatorfn01.algar" 
set server "198.19.255.10" 
set secret ZFT4paKPt8Qh!CkTGcmR 
set auth-type pap 
set source-ip <ip_loopback>
next 
end 
```

<!--
===============================================================================
ETAPA 8: CRIAÇÃO DO GRUPO DE USUÁRIOS RADIUS (GRP.SOCAdmins)
===============================================================================
1. OBJETIVO:
   Mapear o grupo de autenticação do servidor RADIUS para permissões administrativas no FortiGate.

2. INSTRUÇÕES GERAIS:
   - Criar o grupo "GRP.SOCAdmins" em 'config user group'.
   - Adicionar o membro "authenticatorfn01.algar".
   - Configurar o bloco 'config match' relacionando a regra 1:
     * server-name: "authenticatorfn01.algar"
     * group-name: "Grp_SOC_Operacao"

3. CONTEXTO DE USO & REGRAS:
   - Permite que os analistas do SOC autentiquem no FortiGate usando suas credenciais corporativas RADIUS.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: Etapa 7 (servidor RADIUS configurado).
   - Validação: Verificar se o grupo contém o membro e o match corretos.
===============================================================================
-->
8. Criar o User Group vinculado ao servidor RADIUS para autenticação dos administradores.

```
config user group 
edit "GRP.SOCAdmins" 
set member "authenticatorfn01.algar" 
config match 
edit 1 
set server-name "authenticatorfn01.algar" 
set group-name "Grp_SOC_Operacao" 
next 
end 
next 
end 
```

<!--
===============================================================================
ETAPA 9: AJUSTE DO ADMIN TIMEOUT GLOBAL
===============================================================================
1. OBJETIVO:
   Definir o tempo máximo de inatividade permitido para sessões administrativas no FortiGate.

2. INSTRUÇÕES GERAIS:
   - Executar 'config system global' e aplicar 'set admintimeout 31'.

3. CONTEXTO DE USO & REGRAS:
   - Em conformidade com a política de segurança da informação Algar (sessões encerram após 31 minutos).

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Executar 'get system global' e checar se admintimeout = 31.
===============================================================================
-->
9. Ajustar o parâmetro Admin Timeout do FortiGate conforme o padrão operacional da Algar.

```
config system global 
set admintimeout 31 
end
```
<!--
===============================================================================
ETAPA 10: CRIAÇÃO DOS OBJETOS DE ENDEREÇO (MGMT.DC, MGMT.DC-2, MGMT.SPOKE)
===============================================================================
1. OBJETIVO:
   Criar os objetos de rede que representam os Datacenters Algar e o IP de gerenciamento local.

2. INSTRUÇÕES GERAIS:
   - Em 'config firewall address', criar os 3 objetos:
     * "MGMT.DC": 'set subnet 198.19.0.0 255.255.255.192'
     * "MGMT.DC-2": 'set subnet 198.19.255.0 255.255.255.0'
     * "MGMT.SPOKE": 'set subnet <ip_loopback> 255.255.255.255'
   - Substituir <ip_loopback> em MGMT.SPOKE.

3. CONTEXTO DE USO & REGRAS:
   - Objetos reutilizáveis essenciais para a montagem das políticas de firewall.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Executar 'get firewall address MGMT.SPOKE' e confirmar a subnet /32.
===============================================================================
-->
10. Criar os objetos de endereço Address Objects necessários para o gerenciamento.

```
config firewall address
edit "MGMT.DC"
set subnet 198.19.0.0 255.255.255.192
next
edit "MGMT.DC-2"
set subnet 198.19.255.0 255.255.255.0
next
edit "MGMT.SPOKE"
set subnet <ip_loopback> 255.255.255.255
next
end
```

<!--
===============================================================================
ETAPA 11: POLÍTICA DE FIREWALL DE GERENCIAMENTO (MGMT-INBOUND)
===============================================================================
1. OBJETIVO:
   Criar a regra de firewall permitindo o tráfego gerencial vindo dos Datacenters Algar para a Loopback local.

2. INSTRUÇÕES GERAIS:
   - Criar uma nova política em 'config firewall policy' (edit 0):
     * set name "MGMT-INBOUND"
     * set srcintf "ZN.MGMT"
     * set dstintf "mgmt.algar"
     * set srcaddr "MGMT.DC" "MGMT.DC-2"
     * set dstaddr "MGMT.SPOKE"
     * set action accept
     * set status enable
     * set schedule "always"
     * set service "ALL"
     * set logtraffic all

3. CONTEXTO DE USO & REGRAS:
   - Habilita acessos administrativos remotos via VPN e registra logs completos (logtraffic all).

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: Etapas 5 (Zone), 6 (Loopback) e 10 (Address Objects) concluídas.
   - Validação: Checar a regra na tabela de políticas de firewall.
===============================================================================
-->
11. Criar as políticas de firewall Firewall Policies permitindo o tráfego de gerenciamento.

```
config firewall policy
edit 0
set name "MGMT-INBOUND"
set srcintf "ZN.MGMT"
set dstintf "mgmt.algar"
set srcaddr "MGMT.DC" "MGMT.DC-2"
set dstaddr "MGMT.SPOKE"
set action accept
set status enable
set schedule "always"
set service "ALL"
set logtraffic all
next
end
```

<!--
===============================================================================
ETAPA 12: PERFIL DE ACESSO À API REST (api)
===============================================================================
1. OBJETIVO:
   Criar um perfil de acesso restrito de leitura (read-only) para integração via REST API.

2. INSTRUÇÕES GERAIS:
   - Criar 'config system accprofile' com edit "api".
   - Definir permissão 'read' para os grupos: secfabgrp, ftviewgrp, authgrp, sysgrp, netgrp, loggrp, fwgrp, vpngrp, utmgrp, wifi.

3. CONTEXTO DE USO & REGRAS:
   - Garante o princípio do menor privilégio para ferramentas de monitoramento e auditoria automatizadas.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Validação: Executar 'get system accprofile api'.
===============================================================================
-->
12. Criar o perfil de acesso à API (REST API Administrator Profile) com as permissões necessárias.

```
config system accprofile 
edit api 
set secfabgrp read 
set ftviewgrp read 
set authgrp read 
set sysgrp read 
set netgrp read 
set loggrp read 
set fwgrp read 
set vpngrp read 
set utmgrp read 
set wifi read 
next 
end 
```

<!--
===============================================================================
ETAPA 13: PROVISIONAMENTO DE USUÁRIOS ADMINISTRATIVOS LOCAIS E API
===============================================================================
1. OBJETIVO:
   Cadastrar as contas de administradores locais para automação, atração e times de suporte.

2. INSTRUÇÕES GERAIS:
   - Em 'config system admin', criar/editar as 5 contas:
     * "api_soc": accprofile super_admin, trusthost1..4, email soc@algar.com.br
     * "api_nava": accprofile api, trusthost1 (198.19.0.0/26)
     * "algar_soc": accprofile super_admin, trusthost1..8, email soc@algar.com.br
     * "algar_atv": accprofile super_admin, trusthost1..9, email socimplantacao@algartelecom.com.br
     * "operacao_soc": accprofile prof_admin, trusthost1..8, email soc@algar.com.br
   - Aplicar exatamente as senhas literais criptografadas (formatos ENC ...).
   - Aplicar exatamente as sub-redes de trusthost especificadas para restringir a origem do acesso.

3. CONTEXTO DE USO & REGRAS:
   - O uso rigoroso de trusthosts previne acessos não autorizados mesmo se houver vazamento de credenciais.

4. VALIDAÇÃO & PRÉ-REQUISITOS:
   - Pré-requisito: Etapa 12 (Perfil API) concluída.
   - Validação: Executar 'get system admin' e confirmar a existência dos 5 usuários com seus trusthosts.
===============================================================================
-->
13. Criar os usuários administrativos do FortiGate e associá-los aos respectivos perfis de acesso e grupos de autenticação.

```
config system admin 
edit "api_soc" 
set trusthost1 200.225.197.0 255.255.255.0 
set trusthost2 187.32.0.80 255.255.255.240 
set trusthost3 186.237.192.32 255.255.255.224 
set trusthost4 198.19.0.0 255.255.0.0 
set accprofile "super_admin" 
set comments "Credencial de acesso de automacao" 
set vdom "root" 
set email-to "soc@algar.com.br" 
set password ENC SH2em1vo9A9XTUSRWrSFnDYk0nvbfymwi5JOi0bWNPQIc/nGXKr5ljLDwfKJkI=
next 
edit "api_nava" 
set accprofile api 
set vdom "root" 
set trusthost1 198.19.0.0 255.255.255.192 
set password ENC SH2w/ihVL8wifdaYnvwX3Og9jdFr3PjVnUGlegtcmm+PU18U2YTOKlxrYzn4Uw= 
next 
edit "algar_soc" 
set trusthost1 200.225.197.0 255.255.255.0 
set trusthost2 187.32.0.80 255.255.255.240 
set trusthost3 186.237.192.32 255.255.255.224 
set trusthost4 10.0.0.0 255.0.0.0 
set trusthost5 172.16.0.0 255.240.0.0 
set trusthost6 192.168.0.0 255.255.0.0 
set trusthost7 169.254.0.0 255.255.0.0 
set trusthost8 198.19.0.0 255.255.0.0 
set accprofile "super_admin" 
set comments "Credencial de acesso do time de Sustentacao-Gestao" 
set vdom "root" 
set email-to "soc@algar.com.br" 
set password ENC SH24+v6TeulgGtLjMWB6QlaMSpmQl3ZvbH/vOCfdlSgCQ1qbXBnUy/kHOe+4YY= 
next
edit "algar_atv" 
set trusthost1 200.225.197.0 255.255.255.0 
set trusthost2 187.32.0.80 255.255.255.240 
set trusthost3 186.237.192.32 255.255.255.224 
set trusthost4 10.0.0.0 255.0.0.0 
set trusthost5 172.16.0.0 255.240.0.0 
set trusthost6 192.168.0.0 255.255.0.0 
set trusthost7 169.254.0.0 255.255.0.0 
set trusthost8 198.19.0.0 255.255.0.0 
set trusthost9 189.112.147.64 255.255.255.224 
set accprofile "super_admin" 
set comments "Credencial de acesso do time de Ativacao" 
set vdom "root" 
set email-to "socimplantacao@algartelecom.com.br" 
set password ENC SH2PRWUioJD32H7cYVjoDuD33kICsHW+vuPbun/95LrMiMSnl/QulnsyLcgsfw= 
next
edit "operacao_soc" 
set trusthost1 200.225.197.0 255.255.255.0 
set trusthost2 187.32.0.80 255.255.255.240 
set trusthost3 186.237.192.32 255.255.255.224 
set trusthost4 10.0.0.0 255.0.0.0 
set trusthost5 172.16.0.0 255.240.0.0 
set trusthost6 192.168.0.0 255.255.0.0 
set trusthost7 169.254.0.0 255.255.0.0 
set trusthost8 198.19.0.0 255.255.0.0 
set accprofile "prof_admin" 
set comments "Credencial de acesso do time de Sustentacao N1 e N2" 
set vdom "root" 
set email-to "soc@algar.com.br" 
set password ENC SH2uR4WPWxm4axsUZX8CBvqgQ6DetV7W0CArD5x7ugFZXOEhqnSuxiUVAD8x7Y= 
next
end
```