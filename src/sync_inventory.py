"""
Script de Inventário de Sincronia FortiManager (In-Sync vs Out-of-Sync & Policy Package Status).

Lista todos os dispositivos gerenciados, extrai o status de conexão (FGFM),
sincronia de banco de dados (Config/DB Sync) e situação do Pacote de Políticas
(Installed, Modified, Conflict, etc.), gerando relatórios no Terminal, CSV e Markdown.

Uso:
    python -m src.sync_inventory
"""

import csv
import os
import sys
from datetime import datetime
from typing import List, Tuple

from src.config import load_config
from src.client import FortiManagerClient
from src.models.sync_status import SyncDeviceStatus


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


def collect_all_sync_statuses(client: FortiManagerClient) -> List[SyncDeviceStatus]:
    """Coleta os dados de todos os dispositivos cadastrados no FortiManager."""
    print("🔍 Consultando inventário de dispositivos no FortiManager...")
    
    response = client.get("/dvmdb/device", option=["extra info", "assignment info"])
    result_list = response.get("result", [])
    
    if not result_list:
        print("⚠️ Nenhuma resposta recebida do FortiManager.")
        return []
    
    devices_raw = result_list[0].get("data", [])
    if isinstance(devices_raw, dict):
        devices_raw = [devices_raw]

    sync_devices: List[SyncDeviceStatus] = []

    for dev in devices_raw:
        name = dev.get("name", "Desconhecido")
        serial = dev.get("sn", "N/A")
        ip = dev.get("ip", "N/A")
        platform = dev.get("platform_str", dev.get("platform", "N/A"))
        os_ver = f"v{dev.get('os_ver', '')}.{dev.get('patch', dev.get('mr', ''))}" if dev.get("os_ver") else "N/A"
        
        # Extração de ADOM e Policy Package das informações estendidas de VDOM
        vdoms = dev.get("vdom", [])
        adom = "root"
        pkg_name = "N/A"
        raw_pkg_status = "N/A"

        if vdoms and isinstance(vdoms, list):
            first_vdom = vdoms[0]
            adom = first_vdom.get("extra info", {}).get("adom", dev.get("adom", "root"))
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


def print_terminal_summary(devices: List[SyncDeviceStatus]):
    """Exibe um resumo tabular e estatísticas no terminal."""
    print("\n" + "=" * 105)
    print(" 📊 RESUMO DO INVENTÁRIO DE SINCRONIA DE FIREWALLS (FORTIMANAGER)")
    print("=" * 105)
    
    header = f"{'DEVICE':<20} | {'ADOM':<10} | {'IP':<15} | {'PLATA FORMA':<18} | {'CONEXÃO':<8} | {'CONFIG SYNC':<14} | {'PACOTE STATUS':<14}"
    print(header)
    print("-" * 105)
    
    total = len(devices)
    up_count = sum(1 for d in devices if "Up" in d.conn_status)
    down_count = total - up_count
    in_sync_count = sum(1 for d in devices if "In-Sync" in d.db_status)
    out_of_sync_count = sum(1 for d in devices if "Out-of-Sync" in d.db_status)

    for d in devices:
        row = f"{d.name:<20} | {d.adom:<10} | {d.ip:<15} | {d.platform:<18} | {d.conn_status:<8} | {d.db_status:<14} | {d.policy_status:<14}"
        print(row)
        
    print("=" * 105)
    print(f"📈 TOTAL: {total} firewalls | 🟢 Conectados: {up_count} | 🔴 Desconectados: {down_count}")
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


def export_markdown(devices: List[SyncDeviceStatus], filepath: str, host: str):
    """Gera um relatório executivo em formato Markdown."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    now_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    
    total = len(devices)
    up_count = sum(1 for d in devices if "Up" in d.conn_status)
    down_count = total - up_count
    in_sync_count = sum(1 for d in devices if "In-Sync" in d.db_status)
    out_of_sync_count = sum(1 for d in devices if "Out-of-Sync" in d.db_status)

    content = [
        "# Relatório Executivo de Sincronia de Firewalls",
        "",
        f"**Data da Coleta:** {now_str}  ",
        f"**FortiManager Host:** `{host}`  ",
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
        "## 2. Detalhamento por Dispositivo",
        "",
        "| Dispositivo | ADOM | IP | Modelo | Versão | Conexão | Config Sync | Policy Package | Status Pacote |",
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
        content.append("🎉 **Todos os dispositivos estão em dia e perfeitamente sincronizados!**")
    else:
        content.append("A tabela abaixo destaca os equipamentos que requerem atenção da equipe de redes/SOC:")
        content.append("")
        content.append("| Dispositivo | ADOM | Config Sync | Status Pacote | Ação Recomendada |")
        content.append("| :--- | :--- | :---: | :---: | :--- |")
        for d in out_of_sync_list:
            action = "Revisar alterações pendentes no FortiManager e executar *Install Package*."
            if "Down" in d.conn_status:
                action = "Verificar conectividade de rede e túnel FGFM com a unidade."
            content.append(f"| `{d.name}` | `{d.adom}` | {d.db_status} | `{d.policy_status}` | {action} |")

    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"📄 Relatório Markdown salvo em: {filepath}")


def main():
    """Função principal de execução do script."""
    try:
        config = load_config()
        client = FortiManagerClient(
            host=config["host"],
            api_key=config["api_key"],
            port=config["port"],
            verify_ssl=config["verify_ssl"],
        )
    except Exception as e:
        print(f"❌ Erro ao carregar configurações ou inicializar o cliente FortiManager: {e}")
        sys.exit(1)

    sync_devices = collect_all_sync_statuses(client)

    if not sync_devices:
        print("⚠️ Nulo ou nenhum dispositivo foi encontrado.")
        return

    # Gera relatórios
    print_terminal_summary(sync_devices)
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    reports_dir = os.path.join(base_dir, "reports")
    
    csv_file = os.path.join(reports_dir, "sync_inventory.csv")
    md_file = os.path.join(reports_dir, "sync_inventory.md")

    export_csv(sync_devices, csv_file)
    export_markdown(sync_devices, md_file, host=config["host"])


if __name__ == "__main__":
    main()
