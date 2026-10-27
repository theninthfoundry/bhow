"""External OIDC access tokens; local dev-header is explicit and blocked outside local."""
from dataclasses import dataclass
from functools import lru_cache
from ipaddress import ip_address
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from bhow_api.config import Settings, get_settings

bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str


@lru_cache
def _jwks_client(url: str) -> PyJWKClient:
    return PyJWKClient(url, cache_jwk_set=True, lifespan=300, timeout=3)


def current_principal(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
    dev_subject: Annotated[str | None, Header(alias="X-Dev-User")] = None,
) -> Principal:
    if settings.app_env == "local" and settings.allow_dev_auth and dev_subject:
        # Only the actual ASGI peer may use a development identity. Never trust
        # X-Forwarded-For (a client-controlled value in untrusted deployments).
        try:
            loopback_peer = request.client is not None and ip_address(request.client.host).is_loopback
        except ValueError:
            loopback_peer = False
        if not loopback_peer:
            raise HTTPException(status_code=403, detail="Development identity requires a loopback peer")
        if not (1 <= len(dev_subject) <= 128 and all(ch.isalnum() or ch in "_-.@" for ch in dev_subject)):
            raise HTTPException(status_code=400, detail="Invalid local development subject")
        return Principal(subject=f"dev:{dev_subject}")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    if not all((settings.oidc_jwks_url, settings.oidc_audience, settings.oidc_issuer)):
        raise HTTPException(status_code=503, detail="Identity provider is not configured")
    try:
        assert settings.oidc_jwks_url is not None
        assert settings.oidc_audience is not None
        assert settings.oidc_issuer is not None
        key = _jwks_client(settings.oidc_jwks_url).get_signing_key_from_jwt(token.credentials)
        payload = jwt.decode(
            token.credentials,
            key.key,
            algorithms=["RS256"],
            audience=settings.oidc_audience,
            issuer=settings.oidc_issuer,
            options={"require": ["sub", "iss", "aud", "exp"]},
        )
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise ValueError("Missing valid subject")
        return Principal(subject=subject)
    except (jwt.PyJWTError, ValueError, OSError) as exc:
        raise HTTPException(status_code=401, detail="Invalid access token") from exc
