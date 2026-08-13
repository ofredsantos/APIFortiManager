"""
Gerador de Bilhetes Auditáveis e Playbooks de Intervenção FortiGate (Atividade/).

Lê o inventário resumo_equipamentos.csv, cruza com o padrão de gerência
Gerencia Algar com 2 uplinks.md e gera bilhetes individuais em Markdown/CLI
com scripts de aplicação incremental (não duplicada), comandos de rollback
e o checklist com as 13 verificações de prova de conceito.

Uso:
    python -m Atividade.ticket_generator
"""

import csv
import os
import sys
from typing import Dict, List, Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_resumo_csv(csv_path: str) -> List[dict]:
    """Carrega o resumo_equipamentos.csv em uma lista de dicionários."""
    equipments = []
    if not os.path.exists(csv_path):
        return equipments
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            equipments.append(row)
    return equipments


def generate_device_ticket(
    eq: dict,
    int_uplink_1: str = "port1",
    int_uplink_2: Optional[str] = None,
    ip_loopback: Optional[str] = None,
    output_dir: str = ""
) -> str:
    """
    Gera o arquivo de bilhete de intervenção para um equipamento específico.
    """
    device_name = eq.get("Device", "desconhecido")
    hostname = eq.get("Hostname", device_name)
    serial = eq.get("Serial", "N/A")
    adom = eq.get("ADOM", "DOM_ATACAREJO")
    has_dual_uplink = int_uplink_2 is not None and bool(int_uplink_2.strip())

    loopback_value = ip_loopback if ip_loopback else "<ip_loopback_A_PREENCHER>"

    # Mapeamento dos 13 requisitos do CSV
    req_status = {f"R{i:02d}": eq.get(f"R{i:02d}", "AUSENTE") for i in range(1, 14)}

    ticket_lines = [
        f"# Bilhete de Intervenção e Padronização de Gerência - {hostname}",
        "",
        "## 1. Identificação do Equipamento e Variáveis de Entrada",
        "",
        "| Parâmetro | Valor Configurado / Detectado |",
        "| :--- | :--- |",
        f"| **Hostname / Device** | `{hostname}` (`{device_name}`) |",
        f"| **Número de Série** | `{serial}` |",
        f"| **ADOM FortiManager** | `{adom}` |",
        f"| **`<int_uplink-1>` (WAN Principal)** | `{int_uplink_1}` |",
        f"| **`<int_uplink-2>` (WAN Backup)** | `{int_uplink_2 if has_dual_uplink else 'N/A (Single Uplink)'}` |",
        f"| **`<ip_loopback>` (IP Gerência)** | `{loopback_value}` |",
        "",
        "---",
        "",
        "## 2. Matriz de Auditoria das 13 Atividades (Baseline Algar)",
        "",
        "| Requisito | Atividade Baseline | Status Atual | Ação Requerida |",
        "| :---: | :--- | :---: | :--- |",
        f"| **R01** | Túneis IPsec (`VPN.MGMT.01/02`) | `{req_status['R01']}` | {'Nenhuma (Existente)' if req_status['R01'] == 'OK' else 'Criar túneis VPN.MGMT.01 ' + ('e VPN.MGMT.02' if has_dual_uplink else '')} |",
        f"| **R02** | Rotas Estáticas em VRF 1 | `{req_status['R02']}` | {'Nenhuma (Existente)' if req_status['R02'] == 'OK' else 'Criar rotas para 198.19.0.0/26 e 198.19.255.0/24 em VRF 1'} |",
        f"| **R03** | Perfil REST API (`api`) | `{req_status['R03']}` | {'Nenhuma (Existente)' if req_status['R03'] == 'OK' else 'Criar accprofile api com acesso de leitura'} |",
        f"| **R04** | Contas Admin Padrão Algar | `{req_status['R04']}` | {'Nenhuma (Existente)' if req_status['R04'] == 'OK' else 'Criar usuários api_soc, api_nava, algar_soc, algar_atv, operacao_soc'} |",
        f"| **R05** | Interface Loopback (`mgmt.algar`) | `{req_status['R05']}` | {'Nenhuma (Existente)' if req_status['R05'] == 'OK' else 'Criar interface loopback mgmt.algar em VRF 1'} |",
        f"| **R06** | Nomenclatura de Túneis | `{req_status['R06']}` | {'Nenhuma (Existente)' if req_status['R06'] == 'OK' else 'Padronizar nomes VPN.MGMT.01/02'} |",
        f"| **R07** | Zone de Gerência (`ZN.MGMT`) | `{req_status['R07']}` | {'Nenhuma (Existente)' if req_status['R07'] == 'OK' else 'Criar zone ZN.MGMT e associar interfaces de túnel'} |",
        f"| **R08** | Address Objects (`MGMT.DC`, `SPOKE`) | `{req_status['R08']}` | {'Nenhuma (Existente)' if req_status['R08'] == 'OK' else 'Criar objetos MGMT.DC (198.19.0.0/26), MGMT.DC-2 e MGMT.SPOKE'} |",
        f"| **R09** | Policy `MGMT-INBOUND` | `{req_status['R09']}` | {'Nenhuma (Existente)' if req_status['R09'] == 'OK' else 'Criar regra MGMT-INBOUND permitindo ZN.MGMT para mgmt.algar'} |",
        f"| **R10** | Servidor RADIUS (`authenticatorfn01.algar`)| `{req_status['R10']}` | {'Nenhuma (Existente)' if req_status['R10'] == 'OK' else 'Configurar servidor RADIUS 198.19.255.10'} |",
        f"| **R11** | User Group RADIUS (`GRP.SOCAdmins`) | `{req_status['R11']}` | {'Nenhuma (Existente)' if req_status['R11'] == 'OK' else 'Criar grupo GRP.SOCAdmins com membro authenticatorfn01.algar'} |",
        f"| **R12** | Admin Timeout Global (`31 min`) | `{req_status['R12']}` | {'Nenhuma (Existente)' if req_status['R12'] == 'OK' else 'Ajustar admintimeout para 31 minutos'} |",
        f"| **R13** | Sincronia de Configuração (Sync Status) | `{req_status['R13']}` | {'Nenhuma (Existente)' if req_status['R13'] == 'OK' else 'Revisar pendências de sincronização'} |",
        "",
        "---",
        "",
        "## 3. Script CLI de Aplicação Incremental (Não Duplicado)",
        "",
        "> [!IMPORTANT]",
        "> O script abaixo contempla **exclusivamente os itens ausentes/incompletos**, preservando configurações válidas já existentes.",
        "",
        "```fortinet",
    ]

    # Constroi os blocos CLI apenas para o que for ausente
    # R01 & R06: Túneis IPsec
    if req_status["R01"] != "OK" or req_status["R06"] != "OK":
        ticket_lines.extend([
            "config vpn ipsec phase1-interface",
            'edit "VPN.MGMT.01"',
            f'set interface "{int_uplink_1}"',
            'set mode aggressive',
            'set peertype one',
            'set peerid "mgmt01"',
            'set proposal aes128-sha1',
            'set localid "mgmt01"',
            'set dpd on-idle',
            'set dhgrp 5',
            'set remote-gw 189.112.0.244',
            'set psksecret ENC lcoIKHaj1+QbySR417wUBGOl0xmZ9x7rarBCNANLpNl6pwh3hKAGQsHRV1IC/9HhdCDf6bfsm7Ve9IO9hnir2rWIA3X03T4V3VhG0TqXw9FZTTuvgzrUEOVYdlBBEOFvt1wt+XgwSzJkNPZOsiHOKlKGUWoKTgKiVwA9QPgYIPhBXxIXaEgcjOsW31HGLl8Tcf2hXg==',
            'next',
        ])
        if has_dual_uplink:
            ticket_lines.extend([
                'edit "VPN.MGMT.02"',
                f'set interface "{int_uplink_2}"',
                'set mode aggressive',
                'set peertype one',
                'set peerid "mgmt02"',
                'set proposal aes128-sha1',
                'set localid "mgmt02"',
                'set dhgrp 5',
                'set remote-gw 189.112.0.244',
                'set psksecret ENC lcoIKHaj1+QbySR417wUBGOl0xmZ9x7rarBCNANLpNl6pwh3hKAGQsHRV1IC/9HhdCDf6bfsm7Ve9IO9hnir2rWIA3X03T4V3VhG0TqXw9FZTTuvgzrUEOVYdlBBEOFvt1wt+XgwSzJkNPZOsiHOKlKGUWoKTgKiVwA9QPgYIPhBXxIXaEgcjOsW31HGLl8Tcf2hXg==',
                'next',
            ])
        ticket_lines.extend([
            "end",
            "",
            "config vpn ipsec phase2-interface",
            'edit "VPN.MGMT.01.P2"',
            'set phase1name "VPN.MGMT.01"',
            'set proposal aes128-sha1',
            'set dhgrp 5',
            'set auto-negotiate enable',
            f'set src-subnet {loopback_value} 255.255.255.255',
            'next',
        ])
        if has_dual_uplink:
            ticket_lines.extend([
                'edit "VPN.MGMT.02.P2"',
                'set phase1name "VPN.MGMT.02"',
                'set proposal aes128-sha1',
                'set dhgrp 5',
                'set auto-negotiate enable',
                f'set src-subnet {loopback_value} 255.255.255.255',
                'next',
            ])
        ticket_lines.extend(["end", ""])

    # R03: VRF 1 nas Interfaces dos Túneis
    if req_status["R01"] != "OK" or req_status["R06"] != "OK":
        ticket_lines.extend([
            "config system interface",
            "edit VPN.MGMT.01",
            "set vrf 1",
            "next",
        ])
        if has_dual_uplink:
            ticket_lines.extend([
                "edit VPN.MGMT.02",
                "set vrf 1",
                "next",
            ])
        ticket_lines.extend(["end", ""])

    # R02: Rotas Estáticas
    if req_status["R02"] != "OK":
        ticket_lines.extend([
            "config router static",
            "edit 0",
            "set dst 198.19.0.0 255.255.255.192",
            "set priority 50",
            "set distance 10",
            'set device "VPN.MGMT.01"',
            "next",
            "edit 0",
            "set dst 198.19.255.0 255.255.255.0",
            "set priority 50",
            "set distance 10",
            'set device "VPN.MGMT.01"',
            "next",
        ])
        if has_dual_uplink:
            ticket_lines.extend([
                "edit 0",
                "set dst 198.19.0.0 255.255.255.192",
                "set priority 60",
                "set distance 10",
                'set device "VPN.MGMT.02"',
                "next",
                "edit 0",
                "set dst 198.19.255.0 255.255.255.0",
                "set priority 60",
                "set distance 10",
                'set device "VPN.MGMT.02"',
                "next",
            ])
        ticket_lines.extend(["end", ""])

    # R07: Zone ZN.MGMT
    if req_status["R07"] != "OK":
        ifaces_zone = '"VPN.MGMT.01" "VPN.MGMT.02"' if has_dual_uplink else '"VPN.MGMT.01"'
        ticket_lines.extend([
            "config system zone",
            'edit "ZN.MGMT"',
            f'set interface {ifaces_zone}',
            "next",
            "end",
            "",
        ])

    # R05: Loopback mgmt.algar
    if req_status["R05"] != "OK":
        ticket_lines.extend([
            "config system interface",
            'edit "mgmt.algar"',
            'set vdom "root"',
            "set vrf 1",
            f"set ip {loopback_value} 255.255.255.255",
            "set allowaccess ping https ssh http fgfm",
            "set type loopback",
            "set role dmz",
            "next",
            "end",
            "",
        ])

    # R10: Servidor RADIUS
    if req_status["R10"] != "OK":
        ticket_lines.extend([
            "config user radius",
            'edit "authenticatorfn01.algar"',
            'set server "198.19.255.10"',
            "set secret ZFT4paKPt8Qh!CkTGcmR",
            "set auth-type pap",
            f"set source-ip {loopback_value}",
            "next",
            "end",
            "",
        ])

    # R11: Grupo RADIUS
    if req_status["R11"] != "OK":
        ticket_lines.extend([
            "config user group",
            'edit "GRP.SOCAdmins"',
            'set member "authenticatorfn01.algar"',
            "config match",
            "edit 1",
            'set server-name "authenticatorfn01.algar"',
            'set group-name "Grp_SOC_Operacao"',
            "next",
            "end",
            "next",
            "end",
            "",
        ])

    # R12: admintimeout
    if req_status["R12"] != "OK":
        ticket_lines.extend([
            "config system global",
            "set admintimeout 31",
            "end",
            "",
        ])

    # R08: Address Objects
    if req_status["R08"] != "OK":
        ticket_lines.extend([
            "config firewall address",
            'edit "MGMT.DC"',
            "set subnet 198.19.0.0 255.255.255.192",
            "next",
            'edit "MGMT.DC-2"',
            "set subnet 198.19.255.0 255.255.255.0",
            "next",
            'edit "MGMT.SPOKE"',
            f"set subnet {loopback_value} 255.255.255.255",
            "next",
            "end",
            "",
        ])

    # R09: Firewall Policy
    if req_status["R09"] != "OK":
        ticket_lines.extend([
            "config firewall policy",
            "edit 0",
            'set name "MGMT-INBOUND"',
            'set srcintf "ZN.MGMT"',
            'set dstintf "mgmt.algar"',
            'set srcaddr "MGMT.DC" "MGMT.DC-2"',
            'set dstaddr "MGMT.SPOKE"',
            "set action accept",
            "set status enable",
            'set schedule "always"',
            'set service "ALL"',
            "set logtraffic all",
            "next",
            "end",
            "",
        ])

    # R03: Accprofile API
    if req_status["R03"] != "OK":
        ticket_lines.extend([
            "config system accprofile",
            "edit api",
            "set secfabgrp read",
            "set ftviewgrp read",
            "set authgrp read",
            "set sysgrp read",
            "set netgrp read",
            "set loggrp read",
            "set fwgrp read",
            "set vpngrp read",
            "set utmgrp read",
            "set wifi read",
            "next",
            "end",
            "",
        ])

    # R04: Administradores Locais
    if req_status["R04"] != "OK":
        ticket_lines.extend([
            "config system admin",
            'edit "api_soc"',
            "set trusthost1 200.225.197.0 255.255.255.0",
            "set trusthost2 187.32.0.80 255.255.255.240",
            "set trusthost3 186.237.192.32 255.255.255.224",
            "set trusthost4 198.19.0.0 255.255.0.0",
            'set accprofile "super_admin"',
            'set comments "Credencial de acesso de automacao"',
            'set vdom "root"',
            'set email-to "soc@algar.com.br"',
            "set password ENC SH2em1vo9A9XTUSRWrSFnDYk0nvbfymwi5JOi0bWNPQIc/nGXKr5ljLDwfKJkI=",
            "next",
            'edit "api_nava"',
            "set accprofile api",
            'set vdom "root"',
            "set trusthost1 198.19.0.0 255.255.255.192",
            "set password ENC SH2w/ihVL8wifdaYnvwX3Og9jdFr3PjVnUGlegtcmm+PU18U2YTOKlxrYzn4Uw=",
            "next",
            'edit "algar_soc"',
            "set trusthost1 200.225.197.0 255.255.255.0",
            "set trusthost2 187.32.0.80 255.255.255.240",
            "set trusthost3 186.237.192.32 255.255.255.224",
            "set trusthost4 10.0.0.0 255.0.0.0",
            "set trusthost5 172.16.0.0 255.240.0.0",
            "set trusthost6 192.168.0.0 255.255.0.0",
            "set trusthost7 169.254.0.0 255.255.0.0",
            "set trusthost8 198.19.0.0 255.255.0.0",
            'set accprofile "super_admin"',
            'set comments "Credencial de acesso do time de Sustentacao-Gestao"',
            'set vdom "root"',
            'set email-to "soc@algar.com.br"',
            "set password ENC SH24+v6TeulgGtLjMWB6QlaMSpmQl3ZvbH/vOCfdlSgCQ1qbXBnUy/kHOe+4YY=",
            "next",
            'edit "algar_atv"',
            "set trusthost1 200.225.197.0 255.255.255.0",
            "set trusthost2 187.32.0.80 255.255.255.240",
            "set trusthost3 186.237.192.32 255.255.255.224",
            "set trusthost4 10.0.0.0 255.0.0.0",
            "set trusthost5 172.16.0.0 255.240.0.0",
            "set trusthost6 192.168.0.0 255.255.0.0",
            "set trusthost7 169.254.0.0 255.255.0.0",
            "set trusthost8 198.19.0.0 255.255.0.0",
            "set trusthost9 189.112.147.64 255.255.255.224",
            'set accprofile "super_admin"',
            'set comments "Credencial de acesso do time de Ativacao"',
            'set vdom "root"',
            'set email-to "socimplantacao@algartelecom.com.br"',
            "set password ENC SH2PRWUioJD32H7cYVjoDuD33kICsHW+vuPbun/95LrMiMSnl/QulnsyLcgsfw=",
            "next",
            'edit "operacao_soc"',
            "set trusthost1 200.225.197.0 255.255.255.0",
            "set trusthost2 187.32.0.80 255.255.255.240",
            "set trusthost3 186.237.192.32 255.255.255.224",
            "set trusthost4 10.0.0.0 255.0.0.0",
            "set trusthost5 172.16.0.0 255.240.0.0",
            "set trusthost6 192.168.0.0 255.255.0.0",
            "set trusthost7 169.254.0.0 255.255.0.0",
            "set trusthost8 198.19.0.0 255.255.0.0",
            'set accprofile "prof_admin"',
            'set comments "Credencial de acesso do time de Sustentacao N1 e N2"',
            'set vdom "root"',
            'set email-to "soc@algar.com.br"',
            "set password ENC SH2uR4WPWxm4axsUZX8CBvqgQ6DetV7W0CArD5x7ugFZXOEhqnSuxiUVAD8x7Y=",
            "next",
            "end",
            "",
        ])

    ticket_lines.extend([
        "```",
        "",
        "---",
        "",
        "## 4. Procedimento de Rollback e Contingência",
        "",
        "### 4.1 Script de Reversão Suave (Soft Rollback - Sem Reboot)",
        "```fortinet",
        "config firewall policy",
        'delete [ID_POLICY_MGMT_INBOUND]',
        "end",
        "config firewall address",
        'delete "MGMT.SPOKE"',
        'delete "MGMT.DC-2"',
        'delete "MGMT.DC"',
        "end",
        "config user group",
        'delete "GRP.SOCAdmins"',
        "end",
        "config user radius",
        'delete "authenticatorfn01.algar"',
        "end",
        "config system zone",
        'delete "ZN.MGMT"',
        "end",
        "config system interface",
        'delete "mgmt.algar"',
        "end",
        "config vpn ipsec phase1-interface",
        'delete "VPN.MGMT.01"',
        'delete "VPN.MGMT.02"',
        "end",
        "```",
        "",
        "### 4.2 Restauração de Backup Bruto Full (Rollback Total com Reboot)",
        "Em caso de contingência severa ou perda de conectividade:",
        "1. Localizar o arquivo de backup `.conf` gerado na etapa 0: `Atividade/backups/`",
        "2. Executar restauração via CLI ou REST API:",
        "```fortinet",
        "execute restore config tftp <nome_arquivo_backup>.conf <ip_tftp>",
        "# O equipamento irá reiniciar automaticamente restaurando o estado inicial.",
        "```",
        "",
        "---",
        "",
        "## 5. Checklist de Verificação e Provas de Conceito (Pós-Intervenção)",
        "",
        "| # | Etapa / Item | Comando de Validação | Resultado Esperado |",
        "| :---: | :--- | :--- | :--- |",
        "| 1 | Interfaces WAN | `get system interface` | WAN1 e WAN2 ativas eUP |",
        "| 2 | Túneis IPsec | `get vpn ipsec tunnel summary` | VPN.MGMT.01 (e 02) UP |",
        "| 3 | VRF 1 nos Túneis | `get system interface VPN.MGMT.01` | Parâmetro `vrf: 1` |",
        "| 4 | Roteamento Gerência | `get router info routing-table vrf 1` | Rotas 198.19.0.0/26 e 198.19.255.0/24 |",
        "| 5 | Zone ZN.MGMT | `get system zone ZN.MGMT` | Interfaces VPN.MGMT.01/02 vinculadas |",
        "| 6 | Loopback mgmt.algar | `get system interface mgmt.algar` | Interface UP em VRF 1 com IP designado |",
        "| 7 | Servidor RADIUS | `diagnose test authserver radius authenticatorfn01.algar pap test_user pass` | Resposta `successful` do RADIUS |",
        "| 8 | Grupo GRP.SOCAdmins | `get user group GRP.SOCAdmins` | Membro `authenticatorfn01.algar` e match `Grp_SOC_Operacao` |",
        "| 9 | Admin Timeout | `get system global` | `admintimeout: 31` |",
        "| 10| Objetos MGMT.DC | `get firewall address MGMT.DC` | Objetos MGMT.DC (198.19.0.0/26) e MGMT.SPOKE criados |",
        "| 11| Policy MGMT-INBOUND | `get firewall policy` | Regra MGMT-INBOUND ativa de ZN.MGMT para mgmt.algar |",
        "| 12| Perfil REST API | `get system accprofile api` | Perfil `api` com permissões read ativadas |",
        "| 13| Usuários Admin | `get system admin` | Usuários `api_soc`, `algar_soc`, `algar_atv`, `operacao_soc` criados |",
    ])

    os.makedirs(output_dir, exist_ok=True)
    filename = f"bilhete_{hostname}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("\n".join(ticket_lines))

    return filepath


def generate_all_tickets(resumo_csv_path: str, output_dir: str) -> List[str]:
    """Gera a suíte completa de bilhetes para todos os equipamentos do resumo."""
    equipments = load_resumo_csv(resumo_csv_path)
    generated_files = []

    for eq in equipments:
        # Se for o equipamento de teste Araruama
        device_name = eq.get("Device", "")
        int_w1 = "port1"
        int_w2 = "port2" if "60E" in eq.get("Serial", "") or "100F" in eq.get("Serial", "") else None
        
        filepath = generate_device_ticket(
            eq=eq,
            int_uplink_1=int_w1,
            int_uplink_2=int_w2,
            ip_loopback=None, # Mantém tag para preenchimento se ausente
            output_dir=output_dir
        )
        generated_files.append(filepath)

    return generated_files


def main():
    resumo_csv = os.path.join(current_dir, "inventario", "resumo_equipamentos.csv")
    bilhetes_dir = os.path.join(current_dir, "bilhetes")

    if not os.path.exists(resumo_csv):
        print(f"❌ Arquivo {resumo_csv} não encontrado.")
        sys.exit(1)

    print(f"📄 Gerando bilhetes de intervenção auditáveis em: {bilhetes_dir}...")
    files = generate_all_tickets(resumo_csv, bilhetes_dir)
    print(f"✅ Sucesso! Gerados {len(files)} bilhetes de intervenção em {bilhetes_dir}/")


if __name__ == "__main__":
    main()
