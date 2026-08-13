import os
from dotenv import load_dotenv


def load_config() -> dict:
    """Carrega as configurações do arquivo .env"""
    load_dotenv()

    host = os.getenv("FMGR_HOST")
    api_key = os.getenv("FMGR_API_KEY")

    if not host:
        raise ValueError("FMGR_HOST não definido no arquivo .env")
    if not api_key:
        raise ValueError("FMGR_API_KEY não definido no arquivo .env")

    return {
        "host": host,
        "api_key": api_key,
        "port": int(os.getenv("FMGR_PORT", "443")),
        "verify_ssl": os.getenv("FMGR_VERIFY_SSL", "false").lower() == "true",
    }