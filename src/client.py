import json
from typing import Optional, Union
import urllib3
import requests

# Desabilita warnings de SSL para conexões com certificado auto-assinado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FortiManagerClient:
    """Cliente para a API JSON RPC do FortiManager"""

    def __init__(self, host: str, api_key: str, port: int = 443, verify_ssl: bool = False):
        self.base_url = f"https://{host}:{port}/jsonrpc"
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def call(self, method: str, url: str, data: Optional[Union[dict, list]] = None, **kwargs) -> dict:
        """
        Executa uma chamada JSON RPC ao FortiManager.

        Args:
            method: Método JSON RPC (get, set, add, update, delete, exec)
            url: URL do recurso (ex: /dvmdb/adom)
            data: Dados opcionais para o payload
            **kwargs: Parâmetros adicionais (filter, fields, option, etc.)

        Returns:
            Resposta completa da API em dict
        """
        params = {"url": url}

        if data is not None:
            params["data"] = data

        # Adiciona parâmetros extras (filter, fields, option, etc.)
        params.update(kwargs)

        payload = {
            "id": 1,
            "method": method,
            "params": [params],
            "verbose": 1,
        }

        response = requests.post(
            self.base_url,
            headers=self.headers,
            data=json.dumps(payload),
            verify=self.verify_ssl,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get(self, url: str, **kwargs) -> dict:
        """Atalho para chamadas GET"""
        return self.call("get", url, **kwargs)