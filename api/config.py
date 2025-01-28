import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class Settings(BaseSettings):
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    WORKERS: int = int(os.getenv("WORKERS", "1"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API settings
    PROXY_URL: str = os.getenv("PROXY_URL", "https://www.blackbox.ai")
    APP_SECRET: str = os.getenv("APP_SECRET", "")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Headers
    HEADERS: Dict[str, str] = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.blackbox.ai",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    ALLOWED_MODELS: List[Dict[str, str]] = [
        {"id": "gpt-4o", "name": "gpt-4o"},
        {"id": "gemini-1.5-pro", "name": "gemini-pro"},
        {"id": "claude-3-5-sonnet", "name": "claude-sonnet-3.5"},
        {"id": "blackboxai", "name": "blackboxai"},
        {"id": "blackboxai-pro", "name": "blackboxai-pro"},
        {"id": "blackboxai-search", "name": "blackboxai-search"},
        {
            "id": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "name": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        },
        {
            "id": "meta-llama/Meta-Llama-3.1-405B-Instruct-Lite-Pro",
            "name": "meta-llama/Meta-Llama-3.1-405B-Instruct-Lite-Pro",
        },
        {"id": "Qwen/QwQ-32B-Preview", "name": "Qwen/QwQ-32B-Preview"},
    ]

    MODEL_MAPPING: Dict[str, str] = {
        "gpt-4o": "gpt-4o",
        "gemini-1.5-pro": "gemini-pro",
        "claude-3-5-sonnet": "claude-sonnet-3.5",
        "blackboxai": "blackboxai",
        "blackboxai-pro": "blackboxai-pro",
        "blackboxai-search": "blackboxai-search",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-405B-Instruct-Lite-Pro": "meta-llama/Meta-Llama-3.1-405B-Instruct-Lite-Pro",
        "Qwen/QwQ-32B-Preview": "Qwen/QwQ-32B-Preview",
    }

    class Config:
        env_file = ".env"
        case_sensitive = True


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
