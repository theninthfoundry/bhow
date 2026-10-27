"""Deployment configuration, with fail-closed production validation."""
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BH_", env_file=".env", extra="ignore")

    app_env: Literal["local", "test", "staging", "production"] = "local"
    database_url: str = "sqlite:///./bhow.db"
    allow_dev_auth: bool = False
    allowed_origins: str = "http://localhost:8550"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

    @model_validator(mode="after")
    def validate_environment(self) -> "Settings":
        if self.allow_dev_auth and self.app_env != "local":
            raise ValueError("Development authentication is allowed ONLY in local mode")
        if self.app_env in {"production", "staging"}:
            if not self.database_url.startswith("postgresql+psycopg://"):
                raise ValueError("Staging/production require PostgreSQL via psycopg")
            if not all((self.oidc_issuer, self.oidc_audience, self.oidc_jwks_url)):
                raise ValueError("Staging/production require OIDC issuer, audience and JWKS URL")
            if any(x == "*" or "localhost" in x or not x.startswith("https://") for x in self.cors_origins):
                raise ValueError("Staging/production CORS must list HTTPS origins, not wildcard")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
