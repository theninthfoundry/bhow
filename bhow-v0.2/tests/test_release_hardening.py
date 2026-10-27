"""Deployment hardening regression tests (no live secrets or services needed)."""
from datetime import UTC, datetime

import pytest

from bhow_api.config import Settings
from bhow_api.models import utcnow


def settings_for_stage(**overrides: str) -> Settings:
    values = dict(
        app_env="staging",
        allow_dev_auth=False,
        database_url="postgresql+psycopg://bhow:password@db:5432/bhow",
        oidc_issuer="https://identity.example.org/",
        oidc_audience="bhow-api",
        oidc_jwks_url="https://identity.example.org/.well-known/jwks.json",
        allowed_origins="https://app.example.org",
    )
    return Settings(**(values | overrides))


def test_defaults_for_secure_stage():
    assert settings_for_stage().allow_dev_auth is False
    assert settings_for_stage().cors_origins == ["https://app.example.org"]


@pytest.mark.parametrize("origin", ["", "*", "http://app.example.org", "https://localhost",
                                  "https://127.0.0.1", "https://user:pass@app.example.org",
                                  "https://app.example.org/hijack", "https://app.example.org?x=1"])
def test_unsafe_staging_cors_is_rejected(origin):
    with pytest.raises(ValueError):
        settings_for_stage(allowed_origins=origin)


@pytest.mark.parametrize("url", ["http://identity.example.org/jwks", "", "https://user:pass@identity.example.org/jwks"])
def test_insecure_jwks_is_rejected(url):
    with pytest.raises(ValueError):
        settings_for_stage(oidc_jwks_url=url)


def test_dev_auth_is_never_permitted_in_staging():
    with pytest.raises(ValueError):
        settings_for_stage(allow_dev_auth=True)


def test_utc_timestamps_are_timezone_aware():
    assert utcnow().tzinfo is UTC
    assert abs((datetime.now(UTC) - utcnow()).total_seconds()) < 2


def test_backup_restore_rehearsal_on_active_db(client):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    from backup_restore import rehearse_backup_restore
    from bhow_api.db import get_engine
    assert rehearse_backup_restore(str(get_engine().url)) is True
