"""
Script de Backup Completo das Configurações de Firewalls FortiGate via FortiManager.

Realiza o download concorrente do arquivo de configuração CLI (.conf) de todos os
dispositivos gerenciados pelo FortiManager, salvando os backups em subpastas
organizadas por Timestamp e ADOM (ex: backups/YYYY-MM-DD_HH-MM-SS/<ADOM>/<hostname>_<timestamp>.conf).

Também produz relatórios de auditoria em CSV e Markdown contendo tamanho de arquivo,
número de série e validação de integridade.

Uso:
    python -m src.backup_devices
"""

import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os
import sys
import time
from typing import List

from src.config import load_config
from src.client import FortiManagerClient
from src.models.backup_status import BackupResult


def backup_single_device(
    config: dict,
    dev_data: dict,
    date_str: str,
    time_str: str,
    base_backup_dir: str
) -> BackupResult:
    """
    Executa o backup da configuração CLI de um único FortiGate e salva no disco.
    Cria uma instância isolada do cliente por thread para garantir thread-safety.
    """
    client = FortiManagerClient(
        host=config["host"],
        api_key=config["api_key"],
        port=config["port"],
        verify_ssl=config["verify_ssl"],
    )

    device_name = dev_data.get("name", "desconhecido")
    hostname = dev_data.get("hostname") or device_name
    serial = dev_data.get("sn", "N/A")
    platform = dev_data.get("platform_str", dev_data.get("platform", "N/A"))
    os_ver = f"v{dev_data.get('os_ver', '')}.{dev_data.get('patch', dev_data.get('mr', ''))}" if dev_data.get("os_ver") else "N/A"
    
    # Extrai a ADOM do dispositivo
    vdoms = dev_data.get("vdom", [])
    adom = dev_data.get("adom", "root")
    if vdoms and isinstance(vdoms, list):
        adom = vdoms[0].get("extra info", {}).get("adom", adom)

    adom_dir = os.path.join(base_backup_dir, adom)
    os.makedirs(adom_dir, exist_ok=True)

    file_name = f"{hostname}-{time_str}.conf"
    file_path = os.path.join(adom_dir, file_name)

    content = ""
    error_msg = None

    # Tenta obter a configuração CLI com até 3 tentativas (retry com backoff curto)
    for attempt in range(1, 4):
        # Requisição principal: /deployment/export/config
        try:
            res = client.call("exec", "/deployment/export/config", data={"device": device_name})
            result_list = res.get("result", [])
            if result_list and isinstance(result_list, list):
                res_obj = result_list[0]
                code = res_obj.get("status", {}).get("code", -1)
                if code == 0:
                    data_obj = res_obj.get("data")
                    if isinstance(data_obj, dict):
                        content = data_obj.get("content", "")
                    elif isinstance(data_obj, str):
                        content = data_obj
                    if content and len(content) > 100:
                        error_msg = None
                        break
                else:
                    error_msg = res_obj.get("status", {}).get("message", f"Code {code}")
        except Exception as e:
            error_msg = str(e)

        # Fallback: /deployment/checkout/revision
        if not content:
            try:
                res_fb = client.call("exec", "/deployment/checkout/revision", data={"device": device_name, "revision": -1})
                result_list = res_fb.get("result", [])
                if result_list and isinstance(result_list, list):
                    res_obj = result_list[0]
                    code = res_obj.get("status", {}).get("code", -1)
                    if code == 0:
                        data_obj = res_obj.get("data")
                        if isinstance(data_obj, dict):
                            content = data_obj.get("content", "")
                        elif isinstance(data_obj, str):
                            content = data_obj
                        if content and len(content) > 100:
                            error_msg = None
                            break
            except Exception as e:
                if not error_msg:
                    error_msg = str(e)
        
        # Pausa curta antes de tentar novamente
        time.sleep(0.3 * attempt)

    # Validação e Gravação do Arquivo
    if content and len(content) > 100:
        try:
            with open(file_path, mode="w", encoding="utf-8") as f:
                f.write(content)
            
            size_bytes = len(content.encode("utf-8"))
            status = "✅ Sucesso"
            if len(content) < 1000 or not ("#config-version=" in content[:200] or "#" in content[:50]):
                status = "⚠️ Vazio/Incompleto"
                
            return BackupResult(
                device_name=device_name,
                hostname=hostname,
                adom=adom,
                serial=serial,
                platform=platform,
                os_ver=os_ver,
                file_path=file_path,
                file_size_bytes=size_bytes,
                status=status,
                error_message=None
            )
        except Exception as e:
            return BackupResult(
                device_name=device_name,
                hostname=hostname,
                adom=adom,
                serial=serial,
                platform=platform,
                os_ver=os_ver,
                file_path=file_path,
                file_size_bytes=0,
                status="❌ Falha",
                error_message=f"Erro ao salvar arquivo: {e}"
            )
    else:
        return BackupResult(
            device_name=device_name,
            hostname=hostname,
            adom=adom,
            serial=serial,
            platform=platform,
            os_ver=os_ver,
            file_path=file_path,
            file_size_bytes=0,
            status="❌ Falha",
            error_message=error_msg or "Configuração retornou vazia da API"
        )


def export_summary_csv(results: List[BackupResult], csv_path: str):
    """Exporta o relatório de auditoria de backup em CSV."""
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "device_name", "hostname", "adom", "serial", "platform",
            "os_version", "status", "file_size_bytes", "file_size_kb", "file_path", "error_message"
        ])
        for r in results:
            kb_size = round(r.file_size_bytes / 1024.0, 2)
            writer.writerow([
                r.device_name, r.hostname, r.adom, r.serial, r.platform,
                r.os_ver, r.status, r.file_size_bytes, kb_size, r.file_path, r.error_message or ""
            ])


def export_summary_markdown(
    results: List[BackupResult],
    md_path: str,
    host: str,
    date_str: str,
    time_str: str,
    duration_sec: float
):
    """Gera o relatório executivo de auditoria de backup em Markdown."""
    now_formatted = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    total = len(results)
    success_count = sum(1 for r in results if "Sucesso" in r.status)
    warning_count = sum(1 for r in results if "Vazio" in r.status)
    failed_count = sum(1 for r in results if "Falha" in r.status)
    total_bytes = sum(r.file_size_bytes for r in results)
    total_mb = round(total_bytes / (1024.0 * 1024.0), 2)

    content = [
        "# Relatório Executivo de Auditoria de Backup dos Firewalls",
        "",
        f"**Data da Execução:** {now_formatted}  ",
        f"**Data:** `{date_str}` | **Hora:** `{time_str}`  ",
        f"**FortiManager Host:** `{host}`  ",
        f"**Tempo Total de Execução:** `{duration_sec:.2f} segundos`  ",
        "",
        "---",
        "",
        "## 1. Resumo Geral de Governança de Backup",
        "",
        "| Métrica | Quantidade | Percentual / Detalhe |",
        "| :--- | :---: | :---: |",
        f"| **Total de Dispositivos Inventariados** | {total} | 100% |",
        f"| ✅ **Backups Concluídos com Sucesso** | {success_count} | {(success_count/total*100 if total else 0):.1f}% |",
        f"| ⚠️ **Backups Alertas / Incompletos** | {warning_count} | {(warning_count/total*100 if total else 0):.1f}% |",
        f"| ❌ **Falhas no Backup** | {failed_count} | {(failed_count/total*100 if total else 0):.1f}% |",
        f"| 💾 **Volume Total Armazenado** | **{total_mb} MB** | `{total_bytes:,} bytes` |",
        "",
        "---",
        "",
        "## 2. Detalhamento dos Backups Realizados",
        "",
        "| Hostname | ADOM | Modelo | Versão | Tamanho | Status | Arquivo Salvo |",
        "| :--- | :--- | :--- | :--- | :---: | :---: | :--- |",
    ]

    for r in results:
        kb_str = f"{r.file_size_bytes / 1024.0:.1f} KB" if r.file_size_bytes > 0 else "0 KB"
        rel_path = os.path.basename(r.file_path)
        content.append(
            f"| `{r.hostname}` | `{r.adom}` | {r.platform} | {r.os_ver} | {kb_str} | {r.status} | `{rel_path}` |"
        )

    failed_list = [r for r in results if "Falha" in r.status or "Vazio" in r.status]
    content.extend([
        "",
        "---",
        "",
        "## 3. Registro de Falhas ou Anomalias",
        "",
    ])

    if not failed_list:
        content.append("🎉 **Todos os backups de todos os equipamentos foram gerados com 100% de sucesso!**")
    else:
        content.append("A tabela abaixo detalha os equipamentos que falharam durante a extração do backup:")
        content.append("")
        content.append("| Hostname | ADOM | Serial | Mensagem de Erro / Motivo |")
        content.append("| :--- | :--- | :--- | :--- |")
        for r in failed_list:
            content.append(f"| `{r.hostname}` | `{r.adom}` | `{r.serial}` | `{r.error_message or 'Retorno nulo da API'}` |")

    with open(md_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(content))


def backup_all_devices(max_workers: int = 3):
    """Função principal para executar o backup de todos os firewalls."""
    start_time = time.time()
    
    try:
        config = load_config()
        client = FortiManagerClient(
            host=config["host"],
            api_key=config["api_key"],
            port=config["port"],
            verify_ssl=config["verify_ssl"],
        )
    except Exception as e:
        print(f"❌ Erro ao inicializar a API do FortiManager: {e}")
        sys.exit(1)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    execution_backup_dir = os.path.join(base_dir, "backups", date_str)
    os.makedirs(execution_backup_dir, exist_ok=True)

    print("=" * 95)
    print(f"🚀 INICIANDO BACKUP CONCORRENTE DE FIREWALLS - DATA: {date_str} HORA: {time_str}")
    print("=" * 95)
    print("📡 Consultando lista de dispositivos no FortiManager...")

    res_dev = client.get("/dvmdb/device", option=["extra info", "assignment info"])
    result_list = res_dev.get("result", [])
    
    if not result_list:
        print("❌ Nenhum dispositivo retornado pelo FortiManager.")
        sys.exit(1)

    devices_raw = result_list[0].get("data", [])
    if isinstance(devices_raw, dict):
        devices_raw = [devices_raw]

    total_devices = len(devices_raw)
    print(f"📦 {total_devices} dispositivos encontrados. Iniciando downloads paralelos ({max_workers} threads)...\n")

    results: List[BackupResult] = []
    completed_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_dev = {
            executor.submit(backup_single_device, config, dev, date_str, time_str, execution_backup_dir): dev
            for dev in devices_raw
        }
        
        for future in as_completed(future_to_dev):
            completed_count += 1
            res = future.result()
            results.append(res)
            kb_size = f"{res.file_size_bytes / 1024.0:.1f} KB" if res.file_size_bytes > 0 else "0 KB"
            print(f"[{completed_count}/{total_devices}] {res.status} | {res.hostname:<35} ({res.adom:<15}) -> {kb_size}")

    duration = time.time() - start_time
    
    # Ordena resultados por ADOM e Hostname
    results.sort(key=lambda x: (x.adom, x.hostname))

    # Gerar relatórios de auditoria
    csv_file = os.path.join(execution_backup_dir, f"backup_summary_{time_str}.csv")
    md_file = os.path.join(execution_backup_dir, f"backup_summary_{time_str}.md")

    export_summary_csv(results, csv_file)
    export_summary_markdown(results, md_file, host=config["host"], date_str=date_str, time_str=time_str, duration_sec=duration)

    successes = sum(1 for r in results if "Sucesso" in r.status)
    failures = total_devices - successes
    total_mb = sum(r.file_size_bytes for r in results) / (1024.0 * 1024.0)

    print("\n" + "=" * 95)
    print(f"🏁 BACKUP CONCLUÍDO EM {duration:.2f} SEGUNDOS!")
    print(f"📊 Sucesso: {successes}/{total_devices} | ❌ Falhas: {failures} | 💾 Volume Total: {total_mb:.2f} MB")
    print(f"📁 Pasta dos arquivos de backup: {execution_backup_dir}")
    print(f"📄 Relatório de Auditoria: {md_file}")
    print("=" * 95 + "\n")


if __name__ == "__main__":
    backup_all_devices()

