from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="PCA Performance Check", alias="APP_NAME")
    api_version: str = Field(default="1.0.0", alias="API_VERSION")
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")
    data_store_path: str = Field(default="data/analysis_requests.json", alias="DATA_STORE_PATH")
    ai_enabled: bool = Field(default=False, alias="AI_ENABLED")
    ai_provider: str = Field(default="azure_openai", alias="AI_PROVIDER")
    debug: bool = Field(default=False, alias="DEBUG")
    azure_openai_endpoint: str | None = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    azure_openai_deployment: str | None = Field(default=None, alias="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_version: str = Field(
        default="2024-12-01-preview",
        alias="AZURE_OPENAI_API_VERSION",
    )
    backend_base_url: str = Field(default="http://localhost:8000", alias="BACKEND_BASE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
