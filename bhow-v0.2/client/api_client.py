"""Strict, replaceable HTTP boundary for the prototype Flet client.

No login is built here; nonlocal use requires a real short-lived access token.
Local identity headers are allowed only to localhost/127.0.0.1 and never
shipped as an authentication mechanism to public environments.
"""
import os
from datetime import datetime
from typing import Any
from urllib.parse import urlsplit

import httpx


class ApiError(Exception):
    """Safe-to-display API error without personal or server response content."""


class Api:
    def __init__(self, base: str | None = None, *, transport: httpx.BaseTransport | None = None) -> None:
        self.base = (base or os.getenv("BH_API_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.token = os.getenv("BH_ACCESS_TOKEN", "")
        self.dev = os.getenv("BH_CLIENT_DEV_AUTH", "false").lower() == "true"
        parsed = urlsplit(self.base)
        local = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        if self.dev and (parsed.scheme != "http" or not local):
            raise RuntimeError("Preview identity requires a local HTTP backend")
        if not self.dev and not self.token:
            raise RuntimeError("Authentication is not configured")
        if not self.dev and not local and parsed.scheme != "https":
            raise RuntimeError("Remote authentication requires HTTPS")
        self.transport = transport

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers = (
            {"X-Dev-User": "flet-preview"}
            if self.dev
            else {"Authorization": f"Bearer {self.token}"}
        )
        try:
            with httpx.Client(
                base_url=self.base,
                headers=headers,
                timeout=8.0,
                transport=self.transport,
                follow_redirects=False,
            ) as client:
                response = client.request(method, path, **kwargs)
                response.raise_for_status()
                return response.json() if response.content else None
        except httpx.TimeoutException as exc:
            raise ApiError("Connection timed out. Try again.") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in {401, 403}:
                raise ApiError("Your session is unavailable. Sign in again.") from exc
            if exc.response.status_code == 404:
                raise ApiError("Record unavailable or no longer accessible.") from exc
            if exc.response.status_code == 422:
                raise ApiError("Please check the information you entered.") from exc
            raise ApiError("Service unavailable. Try again.") from exc
        except httpx.RequestError as exc:
            raise ApiError("Can't connect to Bhow. Check your connection.") from exc

    def dogs(self) -> list[dict[str, Any]]:
        return self.request("GET", "/v1/dogs")

    def add_dog(self, name: str, care_context: str) -> dict[str, Any]:
        return self.request("POST", "/v1/dogs", json={"name": name, "care_context": care_context})

    def overview(self, dog_id: str) -> dict[str, Any]:
        tz = datetime.now().astimezone().tzinfo
        # Offset-only zones are not IANA IDs. The initial India pilot uses Asia/Kolkata.
        key = getattr(tz, "key", None) or os.getenv("BH_TIMEZONE", "Asia/Kolkata")
        return self.request("GET", f"/v1/dogs/{dog_id}/overview", params={"tz": key})

    def events(self, dog_id: str) -> list[dict[str, Any]]:
        return self.request("GET", f"/v1/dogs/{dog_id}/events")

    def add_event(self, dog_id: str, kind: str, notes: str, occurred_on: str) -> dict[str, Any]:
        return self.request("POST", f"/v1/dogs/{dog_id}/events", json={"kind": kind, "notes": notes, "occurred_on": occurred_on})

    def tasks(self, dog_id: str) -> list[dict[str, Any]]:
        return self.request("GET", f"/v1/dogs/{dog_id}/tasks")

    def add_task(self, dog_id: str, kind: str, title: str, due_on: str) -> dict[str, Any]:
        return self.request("POST", f"/v1/dogs/{dog_id}/tasks", json={"kind": kind, "title": title, "due_on": due_on})

    def complete_task(self, dog_id: str, task_id: str) -> dict[str, Any]:
        return self.request("POST", f"/v1/dogs/{dog_id}/tasks/{task_id}/complete")

    def food(self, text: str, already_eaten: bool = False) -> dict[str, Any]:
        return self.request("POST", "/v1/food/check", json={"ingredients_text": text, "already_eaten": already_eaten})

    def outdoor_advice(self) -> dict[str, Any]:
        return self.request("GET", "/v1/outdoor/advice")
