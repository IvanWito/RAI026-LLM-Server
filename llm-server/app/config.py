from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "rai-026-llm-server"
    env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8000

    llm_provider: str = "ollama"
    llm_model: str = "llama3.1:8b"

    ollama_base_url: str = "http://localhost:11434"

    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"

    gemini_api_key: str | None = None

    request_timeout_seconds: float = 30.0
    cors_allow_origins: str = "*"
    server_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
