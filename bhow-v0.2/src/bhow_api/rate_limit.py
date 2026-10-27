"""In-memory rate limiter middleware for abuse prevention and endpoint throttling."""
import time
from collections import defaultdict
from threading import Lock

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._history: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Never throttle internal operational probes
        if request.url.path in {"/healthz", "/readyz"}:
            return await call_next(request)

        # Identify client by dev/auth header or peer IP
        client_key = request.headers.get("X-Dev-User") or (
            request.client.host if request.client else "unknown"
        )
        now = time.monotonic()
        cutoff = now - 60.0

        with self._lock:
            # Purge requests older than 1 minute
            timestamps = [t for t in self._history[client_key] if t > cutoff]
            if len(timestamps) >= self.requests_per_minute:
                response = Response(
                    content='{"detail": "Rate limit exceeded. Please retry later."}',
                    status_code=429,
                    media_type="application/json",
                )
                response.headers["Retry-After"] = "60"
                response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
                return response

            timestamps.append(now)
            self._history[client_key] = timestamps

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        return response
