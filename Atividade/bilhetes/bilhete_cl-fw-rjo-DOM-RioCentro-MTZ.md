# Bilhete de Intervenção e Padronização de Gerência - cl-fw-rjo-DOM-RioCentro-MTZ

## 1. Identificação do Equipamento e Variáveis de Entrada

| Parâmetro | Valor Configurado / Detectado |
| :--- | :--- |
| **Hostname / Device** | `cl-fw-rjo-DOM-RioCentro-MTZ` (`cl-fw-rjo-DOM-RioCentro-MTZ`) |
| **Número de Série** | `FG100FTK23024786` |
| **ADOM FortiManager** | `DOM_ATACAREJO` |
| **`<int_uplink-1>` (WAN Principal)** | `port1` |
| **`<int_uplink-2>` (WAN Backup)** | `port2` |
| **`<ip_loopback>` (IP Gerência)** | `<ip_loopback_A_PREENCHER>` |

---

## 2. Matriz de Auditoria das 13 Atividades (Baseline Algar)

| Requisito | Atividade Baseline | Status Atual | Ação Requerida |
| :---: | :--- | :---: | :--- |
| **R01** | Túneis IPsec (`VPN.MGMT.01/02`) | `AUSENTE` | Criar túneis VPN.MGMT.01 e VPN.MGMT.02 |
| **R02** | Rotas Estáticas em VRF 1 | `OK` | Nenhuma (Existente) |
| **R03** | Perfil REST API (`api`) | `AUSENTE` | Criar accprofile api com acesso de leitura |
| **R04** | Contas Admin Padrão Algar | `AUSENTE` | Criar usuários api_soc, api_nava, algar_soc, algar_atv, operacao_soc |
| **R05** | Interface Loopback (`mgmt.algar`) | `OK` | Nenhuma (Existente) |
| **R06** | Nomenclatura de Túneis | `OK` | Nenhuma (Existente) |
| **R07** | Zone de Gerência (`ZN.MGMT`) | `AUSENTE` | Criar zone ZN.MGMT e associar interfaces de túnel |
| **R08** | Address Objects (`MGMT.DC`, `SPOKE`) | `OK` | Nenhuma (Existente) |
| **R09** | Policy `MGMT-INBOUND` | `AUSENTE` | Criar regra MGMT-INBOUND permitindo ZN.MGMT para mgmt.algar |
| **R10** | Servidor RADIUS (`authenticatorfn01.algar`)| `AUSENTE` | Configurar servidor RADIUS 198.19.255.10 |
| **R11** | User Group RADIUS (`GRP.SOCAdmins`) | `AUSENTE` | Criar grupo GRP.SOCAdmins com membro authenticatorfn01.algar |
| **R12** | Admin Timeout Global (`31 min`) | `OK` | Nenhuma (Existente) |
| **R13** | Sincronia de Configuração (Sync Status) | `AUSENTE` | Revisar pendências de sincronização |

---

## 3. Script CLI de Aplicação Incremental (Não Duplicado)

> [!IMPORTANT]
> O script abaixo contempla **exclusivamente os itens ausentes/incompletos**, preservando configurações válidas já existentes.

```fortinet
config vpn ipsec phase1-interface
edit "VPN.MGMT.01"
set interface "port1"
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
set interface "port2"
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
set src-subnet <ip_loopback_A_PREENCHER> 255.255.255.255
next
edit "VPN.MGMT.02.P2"
set phase1name "VPN.MGMT.02"
set proposal aes128-sha1
set dhgrp 5
set auto-negotiate enable
set src-subnet <ip_loopback_A_PREENCHER> 255.255.255.255
next
end

config system interface
edit VPN.MGMT.01
set vrf 1
next
edit VPN.MGMT.02
set vrf 1
next
end

config system zone
edit "ZN.MGMT"
set interface "VPN.MGMT.01" "VPN.MGMT.02"
next
end

config user radius
edit "authenticatorfn01.algar"
set server "198.19.255.10"
set secret ZFT4paKPt8Qh!CkTGcmR
set auth-type pap
set source-ip <ip_loopback_A_PREENCHER>
next
end

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

---

## 4. Procedimento de Rollback e Contingência

### 4.1 Script de Reversão Suave (Soft Rollback - Sem Reboot)
```fortinet
config firewall policy
delete [ID_POLICY_MGMT_INBOUND]
end
config firewall address
delete "MGMT.SPOKE"
delete "MGMT.DC-2"
delete "MGMT.DC"
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

### 4.2 Restauração de Backup Bruto Full (Rollback Total com Reboot)
Em caso de contingência severa ou perda de conectividade:
1. Localizar o arquivo de backup `.conf` gerado na etapa 0: `Atividade/backups/`
2. Executar restauração via CLI ou REST API:
```fortinet
execute restore config tftp <nome_arquivo_backup>.conf <ip_tftp>
# O equipamento irá reiniciar automaticamente restaurando o estado inicial.
```

---

## 5. Checklist de Verificação e Provas de Conceito (Pós-Intervenção)

| # | Etapa / Item | Comando de Validação | Resultado Esperado |
| :---: | :--- | :--- | :--- |
| 1 | Interfaces WAN | `get system interface` | WAN1 e WAN2 ativas eUP |
| 2 | Túneis IPsec | `get vpn ipsec tunnel summary` | VPN.MGMT.01 (e 02) UP |
| 3 | VRF 1 nos Túneis | `get system interface VPN.MGMT.01` | Parâmetro `vrf: 1` |
| 4 | Roteamento Gerência | `get router info routing-table vrf 1` | Rotas 198.19.0.0/26 e 198.19.255.0/24 |
| 5 | Zone ZN.MGMT | `get system zone ZN.MGMT` | Interfaces VPN.MGMT.01/02 vinculadas |
| 6 | Loopback mgmt.algar | `get system interface mgmt.algar` | Interface UP em VRF 1 com IP designado |
| 7 | Servidor RADIUS | `diagnose test authserver radius authenticatorfn01.algar pap test_user pass` | Resposta `successful` do RADIUS |
| 8 | Grupo GRP.SOCAdmins | `get user group GRP.SOCAdmins` | Membro `authenticatorfn01.algar` e match `Grp_SOC_Operacao` |
| 9 | Admin Timeout | `get system global` | `admintimeout: 31` |
| 10| Objetos MGMT.DC | `get firewall address MGMT.DC` | Objetos MGMT.DC (198.19.0.0/26) e MGMT.SPOKE criados |
| 11| Policy MGMT-INBOUND | `get firewall policy` | Regra MGMT-INBOUND ativa de ZN.MGMT para mgmt.algar |
| 12| Perfil REST API | `get system accprofile api` | Perfil `api` com permissões read ativadas |
| 13| Usuários Admin | `get system admin` | Usuários `api_soc`, `algar_soc`, `algar_atv`, `operacao_soc` criados |