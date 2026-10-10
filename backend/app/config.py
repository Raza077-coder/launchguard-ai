from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = False
    database_url: str = "sqlite:///./launchguard.db"
    backend_cors_origins: str = "http://localhost:3000"
    scanner_timeout_seconds: int = 30
    max_pages_per_scan: int = 25
    max_crawl_depth: int = 2
    max_concurrency: int = 2
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    github_token: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
