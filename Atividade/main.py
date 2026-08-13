"""
Script de Inventário de Padronização para FortiManager - ADOM DOM_ATACAREJO.

Lista exclusivamente os dispositivos gerenciados do ADOM DOM_ATACAREJO e verifica
cada um dos 13 requisitos de padronização da rede de gerência conforme a baseline
Algar (Gerencia Algar com 2 uplinks.md). Evita a duplicação ou criação desnecessária
de configurações caso elementos equivalentes/reaproveitáveis já existam.

Uso:
    python Atividade/main.py
    ou
    python -m Atividade.main
"""

import sys
import os

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
from src.models.device_inventory import DeviceInfo, DeviceInventory
from src.collectors.vpn_ipsec import collect_vpn_ipsec
from src.collectors.routes import collect_routes
from src.collectors.accprofile import collect_accprofile
from src.collectors.admin_users import collect_admin_users
from src.collectors.interfaces import collect_loopback, collect_tunnel_naming
from src.collectors.zones import collect_zones
from src.collectors.addresses import collect_addresses
from src.collectors.policies import collect_policies
from src.collectors.radius import collect_radius
from src.collectors.user_groups import collect_user_groups
from src.collectors.system_settings import collect_admintimeout, collect_sync_status
from src.reporters.markdown import save_device_report
from src.reporters.csv_writer import save_csv

TARGET_ADOM = "DOM_ATACAREJO"


def get_device_urls(device_name: str, adom: str) -> dict:
    """Retorna as URLs da API para cada requisito, baseadas no device e ADOM."""
    return {
        "vpn_ipsec": f"/pm/config/device/{device_name}/global/vpn/ipsec/phase1-interface",
        "routes": f"/pm/config/device/{device_name}/vdom/root/router/static",
        "accprofile": "/cli/global/system/accprofile",
        "admin_users": "/cli/global/system/admin",
        "interfaces": f"/pm/config/device/{device_name}/global/system/interface",
        "zones": f"/pm/config/device/{device_name}/global/system/zone",
        "addresses": f"/pm/config/adom/{adom}/obj/firewall/address",
        "policies": f"/pm/config/adom/{adom}/pkg/default/firewall/policy",
        "radius": f"/pm/config/device/{device_name}/global/user/radius",
        "user_groups": f"/pm/config/device/{device_name}/global/user/group",
        "system_global": f"/pm/config/device/{device_name}/global/system/global",
        "device_info": f"/dvmdb/device/{device_name}",
    }


def collect_device_data(client: FortiManagerClient, device_name: str, adom: str) -> dict:
    """Coleta todos os dados da API para um device."""
    urls = get_device_urls(device_name, adom)
    data = {}
    for key, url in urls.items():
        try:
            data[key] = client.get(url)
        except Exception as e:
            print(f"  ⚠️  Erro ao coletar {key} para {device_name}: {e}")
            data[key] = {"result": [{"data": {}, "status": {"code": -1, "message": str(e)}}]}
    return data


def process_device(client: FortiManagerClient, device_name: str, adom: str) -> DeviceInventory:
    """Processa um device e retorna seu inventário completo em relação às 13 atividades."""
    print(f"\n🔍 Processando: {device_name} (ADOM: {adom})...")

    # Busca detalhes do device no DVMDB
    try:
        dev_response = client.get(f"/dvmdb/device/{device_name}")
        dev_data = dev_response.get("result", [{}])[0].get("data", {})
    except Exception:
        dev_data = {}

    device_info = DeviceInfo(
        name=device_name,
        serial=dev_data.get("sn", "N/A"),
        adom=adom,
        hostname=dev_data.get("hostname"),
        version=dev_data.get("os_ver", "N/A"),
        platform=dev_data.get("platform_str"),
    )
    inventory = DeviceInventory(device=device_info)

    # Coleta dados da API
    data = collect_device_data(client, device_name, adom)

    # Aplica os 13 coletore(s) alinhados com a baseline Algar
    inventory.add_requirement(collect_vpn_ipsec(device_name, data["vpn_ipsec"]))
    inventory.add_requirement(collect_routes(device_name, data["routes"]))
    inventory.add_requirement(collect_accprofile(data["accprofile"]))
    inventory.add_requirement(collect_admin_users(data["admin_users"]))
    inventory.add_requirement(collect_loopback(data["interfaces"]))
    inventory.add_requirement(collect_tunnel_naming(data["interfaces"]))
    inventory.add_requirement(collect_zones(data["zones"]))
    inventory.add_requirement(collect_addresses(data["addresses"]))
    inventory.add_requirement(collect_policies(data["policies"]))
    inventory.add_requirement(collect_radius(data["radius"]))
    inventory.add_requirement(collect_user_groups(data["user_groups"]))
    inventory.add_requirement(collect_admintimeout(data["system_global"]))
    inventory.add_requirement(collect_sync_status(data["device_info"]))

    return inventory


def main():
    try:
        config = load_config()
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        print("   Certifique-se de que o arquivo .env existe com FMGR_HOST e FMGR_API_KEY.")
        sys.exit(1)

    print(f"🔌 Conectando ao FortiManager em {config['host']} (Foco: ADOM '{TARGET_ADOM}')...")

    client = FortiManagerClient(
        host=config["host"],
        api_key=config["api_key"],
        port=config["port"],
        verify_ssl=config["verify_ssl"],
    )

    # ─── Buscando ADOMs e filtrando exclusivamente o TARGET_ADOM ─────────────
    print(f"\n📡 Buscando dispositivos do ADOM '{TARGET_ADOM}'...")
    try:
        adom_response = client.get(f"/dvmdb/adom/{TARGET_ADOM}/device", option=["object member"])
        result_list = adom_response.get("result", [])
    except Exception as e:
        print(f"⚠️ Erro ao consultar via /dvmdb/adom/{TARGET_ADOM}/device: {e}. Tentando fallback geral...")
        result_list = []

    devices_list = []
    if result_list and result_list[0].get("status", {}).get("code") == 0:
        raw = result_list[0].get("data", [])
        if isinstance(raw, dict):
            raw = [raw]
        for dev in raw:
            dev_name = dev.get("name")
            if dev_name:
                devices_list.append((dev_name, TARGET_ADOM))

    # Fallback: consultar /dvmdb/adom com membros
    if not devices_list:
        try:
            adom_response_gen = client.get("/dvmdb/adom", option=["object member"])
            adom_data = adom_response_gen.get("result", [{}])[0].get("data", [])
            for adom_entry in adom_data:
                adom_name = adom_entry.get("name", "")
                if adom_name.lower() == TARGET_ADOM.lower():
                    members = adom_entry.get("object member", [])
                    for m in members:
                        m_name = m.get("name") if isinstance(m, dict) else str(m)
                        if m_name:
                            devices_list.append((m_name, adom_name))
        except Exception as e:
            print(f"❌ Erro ao listar ADOMs: {e}")
            sys.exit(1)

    if not devices_list:
        print(f"❌ Nenhum dispositivo encontrado para o ADOM '{TARGET_ADOM}'.")
        sys.exit(1)

    print(f"✅ Encontrados {len(devices_list)} dispositivos no ADOM '{TARGET_ADOM}'.")

    # ─── Processar cada dispositivo ─────────────────────────────────────────
    all_inventories = []
    for device_name, adom_name in devices_list:
        inventory = process_device(client, device_name, adom_name)
        all_inventories.append(inventory)

    # ─── Gerar relatórios ───────────────────────────────────────────────────
    if not all_inventories:
        print("\n❌ Nenhum inventário gerado.")
        sys.exit(1)

    output_dir = os.path.join(current_dir, "inventario")
    print(f"\n{'='*60}")
    print(f"📝 Gerando relatórios em: {output_dir}")
    print(f"{'='*60}")

    # Gera relatórios Markdown por ADOM
    for inv in all_inventories:
        adom_dir = os.path.join(output_dir, inv.device.adom)
        filepath = save_device_report(inv, adom_dir)
        print(f"  ✅ Relatório salvo: {filepath}")

    # Gera CSV resumo
    csv_path = save_csv(all_inventories, output_dir)
    print(f"  ✅ CSV resumo salvo: {csv_path}")

    # ─── Resumo Final ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"📊 RESUMO FINAL - ADOM {TARGET_ADOM}")
    print(f"{'='*60}")
    print(f"  Total de devices inventariados: {len(all_inventories)}")
    print(f"  Relatórios salvos em: {output_dir}/")
    print(f"  CSV resumo: {os.path.join(output_dir, 'resumo_equipamentos.csv')}")

    # Tabela resumo no console
    print(f"\n{'ADOM':<20} {'Device':<35} {'OK':<5} {'PARCIAL':<8} {'AUSENTE':<8}")
    print("-" * 80)
    for inv in all_inventories:
        ok_count = sum(1 for r in inv.requirements if r.status == "✅ OK")
        parcial_count = sum(1 for r in inv.requirements if r.status == "⚠️ Parcial")
        ausente_count = sum(1 for r in inv.requirements if r.status == "❌ Ausente")
        print(f"{inv.device.adom:<20} {inv.device.name:<35} {ok_count:<5} {parcial_count:<8} {ausente_count:<8}")


if __name__ == "__main__":
    main()
