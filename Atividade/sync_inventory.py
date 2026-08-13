"""
Script de Inventário de Sincronia FortiManager para ADOM Específico (DOM_ATACAREJO).

Filtra e lista exclusivamente os dispositivos gerenciados pertencentes ao ADOM DOM_ATACAREJO
no FortiManager (187.72.197.227), focando na identificação dos endereços IP dos firewalls
e mantendo a matriz de governança executiva (Terminal, CSV e Markdown).

Uso:
    python Atividade/sync_inventory.py
    ou
    python -m Atividade.sync_inventory
"""

import csv
import os
import sys
from datetime import datetime
from typing import List

# Adiciona o diretório raiz ao sys.path para importação dos módulos de src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.config import load_config
from src.client import FortiManagerClient
from src.models.sync_status import SyncDeviceStatus

TARGET_ADOM = "DOM_ATACAREJO"


def parse_conn_status(val) -> str:
    """Converte o status de conexão FGFM em indicador visual."""
    if str(val).lower() in ("up", "connected", "1"):
        return "🟢 Up"
    return "🔴 Down"


def parse_db_status(val) -> str:
    """Converte o status de sincronia de configuração em indicador visual."""
    val_str = str(val).lower()
    if val_str in ("insync", "in_sync", "in-sync", "synchronized", "1"):
        return "✅ In-Sync"
    elif val_str in ("out_of_sync", "out-of-sync", "modified", "mod_in_db", "2"):
        return "❌ Out-of-Sync"
    elif val_str in ("nomod", "no_mod"):
        return "✅ In-Sync (sem mod)"
    return f"❓ {val}" if val is not None else "❓ Unknown"


def parse_policy_status(val) -> str:
    """Formata a situação do pacote de políticas com indicadores visuais."""
    val_str = str(val).lower()
    if val_str == "installed":
        return "🟢 Installed"
    elif val_str == "modified":
        return "🟡 Modified"
    elif val_str in ("conflict", "error"):
        return "🔴 Conflict"
    elif val_str == "unknown":
        return "❓ Unknown"
    elif val_str == "n/a":
        return "⚪ N/A"
    return f"🔸 {val.capitalize()}"


def extract_firewall_ip(dev: dict) -> str:
    """
    Extrai o endereço IP do firewall com estratégias de fallback
    para garantir que a informação de IP principal/gerência seja obtida.
    """
    # 1. IP direto do dispositivo no DVMDB
    ip = dev.get("ip")
    if ip and ip not in ("0.0.0.0", "N/A", ""):
        return ip

    # 2. IP de gerenciamento secundário/auxiliar se disponível
    mgmt_ip = dev.get("mgmt_ip")
    if mgmt_ip and mgmt_ip not in ("0.0.0.0", "N/A", ""):
        return mgmt_ip

    # 3. Verificar VIP / IP em vdoms
    vdoms = dev.get("vdom", [])
    if isinstance(vdoms, list):
        for v in vdoms:
            v_ip = v.get("ip")
            if v_ip and v_ip not in ("0.0.0.0", "N/A", ""):
                return v_ip

    return ip if ip else "N/A"


def collect_atacarejo_sync_statuses(client: FortiManagerClient, target_adom: str = TARGET_ADOM) -> List[SyncDeviceStatus]:
    """Coleta os dados de sincronia dos dispositivos pertencentes estritamente ao ADOM especificado."""
    print(f"🔍 Consultando dispositivos do ADOM '{target_adom}' no FortiManager...")

    # Primeiro tenta listar os dispositivos do ADOM via /dvmdb/adom/{adom}/device
    response = client.get(f"/dvmdb/adom/{target_adom}/device", option=["extra info", "assignment info"])
    result_list = response.get("result", [])

    devices_raw = []
    if result_list and result_list[0].get("status", {}).get("code") == 0:
        devices_raw = result_list[0].get("data", [])
        if isinstance(devices_raw, dict):
            devices_raw = [devices_raw]

    # Se a chamada específica de ADOM retornar vazia, busca em /dvmdb/device e filtra
    if not devices_raw:
        gen_response = client.get("/dvmdb/device", option=["extra info", "assignment info"])
        gen_result = gen_response.get("result", [])
        if gen_result:
            all_devs = gen_result[0].get("data", [])
            if isinstance(all_devs, dict):
                all_devs = [all_devs]
            for d in all_devs:
                dev_adom = d.get("adom", "")
                vdoms = d.get("vdom", [])
                vdom_adoms = []
                if isinstance(vdoms, list):
                    for v in vdoms:
                        if isinstance(v, dict):
                            v_adom = v.get("extra info", {}).get("adom") or v.get("adom")
                            if v_adom:
                                vdom_adoms.append(v_adom.lower())

                if dev_adom.lower() == target_adom.lower() or target_adom.lower() in vdom_adoms:
                    devices_raw.append(d)

    if not devices_raw:
        print(f"⚠️ Nenhum dispositivo encontrado para o ADOM '{target_adom}'.")
        return []

    sync_devices: List[SyncDeviceStatus] = []

    for dev in devices_raw:
        name = dev.get("name", "Desconhecido")
        serial = dev.get("sn", "N/A")
        ip = extract_firewall_ip(dev)
        platform = dev.get("platform_str", dev.get("platform", "N/A"))
        os_ver = f"v{dev.get('os_ver', '')}.{dev.get('patch', dev.get('mr', ''))}" if dev.get("os_ver") else "N/A"

        vdoms = dev.get("vdom", [])
        adom = target_adom
        pkg_name = "N/A"
        raw_pkg_status = "N/A"

        if vdoms and isinstance(vdoms, list):
            first_vdom = vdoms[0]
            adom_found = first_vdom.get("extra info", {}).get("adom", dev.get("adom", target_adom))
            if adom_found:
                adom = adom_found
            assignments = first_vdom.get("assignment info", [])
            if isinstance(assignments, list):
                for assign in assignments:
                    if assign.get("type") == "policy":
                        pkg_name = assign.get("name", "N/A")
                        raw_pkg_status = assign.get("status", "N/A")
                        break

        conn_raw = dev.get("conn_status", "down")
        conf_raw = dev.get("conf_status", dev.get("db_status", "unknown"))

        conn_status = parse_conn_status(conn_raw)
        db_status = parse_db_status(conf_raw)
        policy_status = parse_policy_status(raw_pkg_status)

        status_obj = SyncDeviceStatus(
            name=name,
            adom=adom,
            serial=serial,
            ip=ip,
            platform=platform,
            os_ver=os_ver,
            conn_status=conn_status,
            db_status=db_status,
            policy_package=pkg_name,
            policy_status=policy_status,
        )
        sync_devices.append(status_obj)

    return sync_devices


def print_terminal_summary(devices: List[SyncDeviceStatus], adom_name: str):
    """Exibe a matriz tabular e estatísticas no terminal."""
    print("\n" + "=" * 105)
    print(f" 📊 MATRIZ DE INVENTÁRIO DE SINCRONIA DE FIREWALLS - ADOM: {adom_name}")
    print("=" * 105)

    header = f"{'DEVICE':<22} | {'ADOM':<14} | {'ENDEREÇO IP':<16} | {'PLATAFORMA':<16} | {'CONEXÃO':<8} | {'CONFIG SYNC':<14} | {'PACOTE STATUS':<14}"
    print(header)
    print("-" * 105)

    total = len(devices)
    up_count = sum(1 for d in devices if "Up" in d.conn_status)
    down_count = total - up_count
    in_sync_count = sum(1 for d in devices if "In-Sync" in d.db_status)
    out_of_sync_count = sum(1 for d in devices if "Out-of-Sync" in d.db_status)

    for d in devices:
        row = f"{d.name:<22} | {d.adom:<14} | {d.ip:<16} | {d.platform:<16} | {d.conn_status:<8} | {d.db_status:<14} | {d.policy_status:<14}"
        print(row)

    print("=" * 105)
    print(f"📈 TOTAL ({adom_name}): {total} firewalls | 🟢 Conectados: {up_count} | 🔴 Desconectados: {down_count}")
    print(f"✅ In-Sync: {in_sync_count} | ❌ Out-of-Sync: {out_of_sync_count}")
    print("=" * 105 + "\n")


def export_csv(devices: List[SyncDeviceStatus], filepath: str):
    """Exporta os resultados para um arquivo CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "device_name", "adom", "serial", "ip", "platform",
            "os_version", "conn_status", "db_status", "policy_package", "policy_status"
        ])
        for d in devices:
            writer.writerow([
                d.name, d.adom, d.serial, d.ip, d.platform,
                d.os_ver, d.conn_status, d.db_status, d.policy_package, d.policy_status
            ])
    print(f"💾 Relatório CSV salvo em: {filepath}")


def export_markdown(devices: List[SyncDeviceStatus], filepath: str, host: str, adom_name: str):
    """Gera um relatório executivo em formato Markdown para o ADOM alvo."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    now_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    total = len(devices)
    up_count = sum(1 for d in devices if "Up" in d.conn_status)
    down_count = total - up_count
    in_sync_count = sum(1 for d in devices if "In-Sync" in d.db_status)
    out_of_sync_count = sum(1 for d in devices if "Out-of-Sync" in d.db_status)

    content = [
        f"# Relatório Executivo de Sincronia de Firewalls - ADOM {adom_name}",
        "",
        f"**Data da Coleta:** {now_str}  ",
        f"**FortiManager Host:** `{host}`  ",
        f"**ADOM Alvo:** `{adom_name}`  ",
        "",
        "---",
        "",
        "## 1. Quadro de Resumo de Governança",
        "",
        "| Métrica | Quantidade | Percentual |",
        "| :--- | :---: | :---: |",
        f"| **Total de Dispositivos** | {total} | 100% |",
        f"| 🟢 **Conectados (FGFM Up)** | {up_count} | {(up_count/total*100 if total else 0):.1f}% |",
        f"| 🔴 **Desconectados (FGFM Down)** | {down_count} | {(down_count/total*100 if total else 0):.1f}% |",
        f"| ✅ **In-Sync (Configuração Sincronizada)** | {in_sync_count} | {(in_sync_count/total*100 if total else 0):.1f}% |",
        f"| ❌ **Out-of-Sync (Configuração Divergente)** | {out_of_sync_count} | {(out_of_sync_count/total*100 if total else 0):.1f}% |",
        "",
        "---",
        "",
        "## 2. Detalhamento por Dispositivo (Endereços IP e Status)",
        "",
        "| Dispositivo | ADOM | Endereço IP | Modelo | Versão | Conexão | Config Sync | Pacote de Políticas | Status Pacote |",
        "| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :---: |",
    ]

    for d in devices:
        content.append(
            f"| `{d.name}` | `{d.adom}` | `{d.ip}` | {d.platform} | {d.os_ver} | {d.conn_status} | {d.db_status} | `{d.policy_package}` | `{d.policy_status}` |"
        )

    out_of_sync_list = [d for d in devices if "Out-of-Sync" in d.db_status or d.policy_status in ("Modified", "Conflict")]

    content.extend([
        "",
        "---",
        "",
        "## 3. Dispositivos Requerendo Ação de Sincronização",
        "",
    ])

    if not out_of_sync_list:
        content.append("🎉 **Todos os dispositivos do ADOM estão perfeitamente sincronizados!**")
    else:
        content.append("A tabela abaixo destaca os equipamentos que requerem atenção da equipe de redes/SOC:")
        content.append("")
        content.append("| Dispositivo | ADOM | Endereço IP | Config Sync | Status Pacote | Ação Recomendada |")
        content.append("| :--- | :--- | :--- | :---: | :---: | :--- |")
        for d in out_of_sync_list:
            action = "Revisar alterações pendentes no FortiManager e executar *Install Package*."
            if "Down" in d.conn_status:
                action = "Verificar conectividade de rede e túnel FGFM com a unidade."
            content.append(f"| `{d.name}` | `{d.adom}` | `{d.ip}` | {d.db_status} | `{d.policy_status}` | {action} |")

    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"📄 Relatório Markdown salvo em: {filepath}")


def main():
    """Função principal de execução do script de inventário."""
    try:
        config = load_config()
        client = FortiManagerClient(
            host=config["host"],
            api_key=config["api_key"],
            port=config["port"],
            verify_ssl=config["verify_ssl"],
        )
    except Exception as e:
        print(f"❌ Erro ao carregar configurações ou inicializar cliente FortiManager: {e}")
        sys.exit(1)

    print(f"🔌 Conectado ao FortiManager {config['host']} (Foco: ADOM '{TARGET_ADOM}')")
    sync_devices = collect_atacarejo_sync_statuses(client, TARGET_ADOM)

    if not sync_devices:
        print(f"⚠️ Nulo ou nenhum dispositivo foi encontrado no ADOM {TARGET_ADOM}.")
        return

    # Exibe a matriz no terminal
    print_terminal_summary(sync_devices, TARGET_ADOM)

    # Define o diretório de relatórios dentro de Atividade/reports
    reports_dir = os.path.join(current_dir, "reports")

    csv_file = os.path.join(reports_dir, "sync_inventory.csv")
    md_file = os.path.join(reports_dir, "sync_inventory.md")

    export_csv(sync_devices, csv_file)
    export_markdown(sync_devices, md_file, host=config["host"], adom_name=TARGET_ADOM)


if __name__ == "__main__":
    main()
