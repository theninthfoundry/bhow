"""Minimal real-server smoke test (local demo auth only)."""
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

base = os.getenv("BH_SMOKE_URL", "http://127.0.0.1:8000")
for path in ("/healthz", "/openapi.json"):
    try:
        with urlopen(Request(base + path), timeout=3) as response:
            assert response.status == 200, f"Expected 200 for {path}"
            print(f"PASS {path}")
    except URLError as exc:
        raise SystemExit(f"Server unavailable at {base}: {exc}") from exc
