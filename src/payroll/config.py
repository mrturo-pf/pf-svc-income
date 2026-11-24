"""Application settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Represent Settings."""

    env: str = "development"
    database_url: str = Field(
        default="postgresql+asyncpg://pf:pf@localhost:5432/pf",
        validation_alias="PF_DATABASE_URL",
    )
    api_base_url: str = "http://127.0.0.1:8000"
    log_level: str = "INFO"
    pf_svc_reference_base_url: str = Field(
        default="", validation_alias="PF_SVC_REFERENCE_URL"
    )
    pf_svc_reference_cache_ttl_seconds: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PAYROLL_",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
