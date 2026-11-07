from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = None
    sales_copilot_model_fast: str = "gpt-5-mini"
    sales_copilot_model_reasoning: str = "gpt-5"
    sales_copilot_enable_web_search: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
