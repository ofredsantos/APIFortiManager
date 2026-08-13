"""
Cliente REST API Nativo para FortiOS (FortiGate).

Gerencia autenticação direta via REST API (/api/v2/login), suporte a cookies
de sessão (CCSID) e tokens CSRF, download de backup bruto (.conf), descoberta
automática de interfaces WAN/Loopback e execução de consultas CMDB.

Uso:
    from Atividade.fortigate_client import FortiGateClient
"""

import os
import sys
import re
import urllib3
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import requests

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

# Desativa avisos de certificados SSL autoassinados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FortiGateAPIError(Exception):
    """Exceção personalizada para erros na REST API ou SSH do FortiGate."""
    pass


class FortiGateClient:
    """Cliente para interação via REST API HTTPS direta e fallback SSH CLI com o FortiGate."""

    def __init__(self, host: str, username: str, password: str, port: int = 443, ssh_port: int = 22, verify_ssl: bool = False, timeout: int = 10):
        self.host = host.strip()
        self.username = username.strip()
        self.password = password.strip()
        self.port = port
        self.ssh_port = ssh_port
        self.verify_ssl = verify_ssl
        self.timeout = timeout

        self.base_url = f"https://{self.host}:{self.port}"
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        self.csrf_token: Optional[str] = None
        self.is_authenticated: bool = False
        self.auth_method: str = "none"  # "api" ou "ssh"
        self.ssh_client: Optional[Any] = None

    def login(self) -> bool:
        """
        Tenta login primeiro via REST API (HTTPS). 
        Se falhar ou der timeout, executa o FALLBACK automático via SSH CLI (porta 22).
        """
        login_url = f"{self.base_url}/api/v2/login"
        payload = {
            "username": self.username,
            "secretkey": self.password
        }

        # 1. Tenta REST API HTTPS
        try:
            response = self.session.post(login_url, json=payload, timeout=self.timeout)
            if response.status_code == 200:
                self.is_authenticated = True
                self.auth_method = "api"
                for cookie in self.session.cookies:
                    if cookie.name.lower() in ("ccsrftoken", "csrftoken"):
                        self.csrf_token = cookie.value.strip('"')
                        self.session.headers.update({"X-CSRFTOKEN": self.csrf_token})
                return True
        except Exception as e_api:
            print(f"  ⚠️ Tentativa via REST API ({self.host}:{self.port}) falhou/timed out ({e_api}). Acionando FALLBACK via SSH CLI...")

        # 2. FALLBACK: Tenta conexão SSH CLI via Paramiko na porta 22
        if HAS_PARAMIKO:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=self.host,
                    port=self.ssh_port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                    banner_timeout=10,
                    auth_timeout=10,
                    look_for_keys=False,
                    allow_agent=False
                )
                self.ssh_client = ssh
                self.is_authenticated = True
                self.auth_method = "ssh"
                print(f"  🟢 FALLBACK SSH CLI conectado com sucesso ao FortiGate {self.host}:{self.ssh_port}!")
                return True
            except Exception as e_ssh:
                raise FortiGateAPIError(
                    f"❌ FALHA TOTAL DE ACESSO ao FortiGate {self.host}:\n"
                    f"   1. REST API (HTTPS:{self.port}): Timed out / recusado.\n"
                    f"   2. SSH CLI (SSH:{self.ssh_port}): {e_ssh}\n"
                    f"   Verifique se o IP está acessível e se HTTPS/SSH estão habilitados com allowaccess na interface."
                )
        else:
            raise FortiGateAPIError(f"REST API falhou e biblioteca paramiko não está disponível para o fallback SSH.")

    def logout(self):
        """Encerra a sessão HTTP/SSH no FortiGate."""
        if not self.is_authenticated:
            return
        if self.auth_method == "api":
            logout_url = f"{self.base_url}/api/v2/logout"
            try:
                self.session.post(logout_url, timeout=5)
            except Exception:
                pass
        elif self.auth_method == "ssh" and self.ssh_client:
            try:
                self.ssh_client.close()
            except Exception:
                pass
        self.is_authenticated = False
        self.session.close()

    def execute_cli_cmd(self, command: str) -> str:
        """Executa um comando CLI via SSH no FortiGate."""
        if not self.ssh_client:
            raise FortiGateAPIError("Sessão SSH não estabelecida.")
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=self.timeout)
            output = stdout.read().decode("utf-8", errors="ignore")
            return output
        except Exception as e:
            raise FortiGateAPIError(f"Erro ao executar comando CLI '{command}': {e}")

    def get_cmdb(self, path: str, params: Optional[dict] = None) -> Any:
        """Executa uma requisição GET no CMDB do FortiGate (API ou CLI)."""
        if not self.is_authenticated:
            self.login()

        if self.auth_method == "api":
            url = f"{self.base_url}/api/v2/cmdb/{path.lstrip('/')}"
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"status": "error", "code": response.status_code, "text": response.text}
            except requests.RequestException as e:
                return {"status": "error", "error": str(e)}
        elif self.auth_method == "ssh":
            # Converte consulta REST CMDB comum em comando CLI show correspondente
            clean_path = path.lstrip('/').replace('/', ' ')
            cli_out = self.execute_cli_cmd(f"show {clean_path}")
            return {"status": "success", "cli_output": cli_out}

    def download_config_backup(self, output_dir: str, device_name: str = "") -> str:
        """
        Realiza o download da configuração bruta (export .conf) do FortiGate via REST API ou SSH CLI.
        Salva o arquivo em output_dir.
        """
        if not self.is_authenticated:
            self.login()

        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', device_name or self.host)
        filename = f"{sanitized_name}_backup_{timestamp}.conf"
        filepath = os.path.join(output_dir, filename)

        if self.auth_method == "api":
            backup_url = f"{self.base_url}/api/v2/monitor/system/config/backup?scope=global"
            try:
                response = self.session.get(backup_url, timeout=30)
                if response.status_code != 200:
                    raise FortiGateAPIError(f"Erro ao baixar backup via API: HTTP {response.status_code} - {response.text}")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)
                return filepath
            except requests.RequestException as e:
                raise FortiGateAPIError(f"Erro de rede ao baixar backup de {self.host}: {e}")
        elif self.auth_method == "ssh":
            # Captura a configuração completa via CLI (show full-configuration)
            config_text = self.execute_cli_cmd("show full-configuration")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(config_text)
            return filepath

    def discover_wan_interfaces(self) -> Tuple[str, Optional[str]]:
        """
        Identifica automaticamente a interface WAN1 (principal) e WAN2 (secundária)
        inspecionando as rotas estáticas default (0.0.0.0/0) e as interfaces ativas.
        """
        routes_data = self.get_cmdb("router/static")
        interfaces_data = self.get_cmdb("system/interface")

        wan1 = "wan1"
        wan2: Optional[str] = None

        default_routes = []
        if isinstance(routes_data, dict) and "results" in routes_data:
            results = routes_data.get("results", [])
            for r in results:
                dst = r.get("dst", "")
                if dst == "0.0.0.0 0.0.0.0" or dst == "0.0.0.0/0":
                    dev = r.get("device")
                    if dev:
                        if isinstance(dev, list):
                            default_routes.extend(dev)
                        else:
                            default_routes.append(str(dev))

        # Remove duplicadas mantendo ordem
        seen = set()
        unique_wans = []
        for w in default_routes:
            if w not in seen:
                seen.add(w)
                unique_wans.append(w)

        if len(unique_wans) >= 1:
            wan1 = unique_wans[0]
        if len(unique_wans) >= 2:
            wan2 = unique_wans[1]

        # Se não encontrou nas rotas, procura por nome padrão nas interfaces
        if not default_routes and isinstance(interfaces_data, dict) and "results" in interfaces_data:
            ifaces = [i.get("name") for i in interfaces_data.get("results", []) if i.get("name")]
            wan_candidates = [i for i in ifaces if "wan" in i.lower() or "port" in i.lower()]
            if len(wan_candidates) >= 1:
                wan1 = wan_candidates[0]
            if len(wan_candidates) >= 2:
                wan2 = wan_candidates[1]

        return wan1, wan2

    def discover_loopback(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Verifica se já existe uma interface loopback (ex: mgmt.algar ou loopback).
        Retorna Tupla (nome_interface, ip_loopback).
        """
        interfaces_data = self.get_cmdb("system/interface")
        if isinstance(interfaces_data, dict) and "results" in interfaces_data:
            for iface in interfaces_data.get("results", []):
                if iface.get("type") == "loopback" or iface.get("name") in ("mgmt.algar", "loopback_mgmt"):
                    name = iface.get("name")
                    ip = iface.get("ip")
                    ip_str = None
                    if ip:
                        if isinstance(ip, list) and len(ip) >= 1:
                            ip_str = ip[0]
                        elif isinstance(ip, str):
                            ip_str = ip.split()[0]
                    return name, ip_str
        return None, None


def load_atividade_env() -> dict:
    """Carrega as variáveis do arquivo Atividade/.env."""
    env_path = os.path.join(current_dir, ".env")
    env_data = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and ":" in line:
                    k, v = line.split(":", 1)
                    env_data[k.strip()] = v.strip()
    return env_data
