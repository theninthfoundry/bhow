"""Deployment configuration, with fail-closed production validation."""
from functools import lru_cache
from typing import Literal
from urllib.parse import urlsplit

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
            if not self.cors_origins:
                raise ValueError("Staging/production require at least one HTTPS CORS origin")
            for origin in self.cors_origins:
                parsed = urlsplit(origin)
                if (parsed.scheme != "https" or not parsed.hostname or
                        parsed.username or parsed.password or parsed.path not in {"", "/"} or
                        parsed.query or parsed.fragment or
                        parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}):
                    raise ValueError("Staging/production CORS requires valid HTTPS public origins")
            for auth_url in (self.oidc_issuer, self.oidc_jwks_url):
                parsed = urlsplit(auth_url or "")
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError("Staging/production OIDC URLs must use valid HTTPS endpoints")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
