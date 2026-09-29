from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    use_local_explanation: bool = False
    max_input_chars: int = 20000
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
