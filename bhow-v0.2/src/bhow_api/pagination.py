"""Stable keyset cursors: opaque encoding, not a security token."""
import base64
import json
from datetime import date, datetime
from uuid import UUID
from fastapi import HTTPException


def encode_cursor(*values: object) -> str:
    blob = json.dumps([str(value) for value in values], separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(blob).decode().rstrip("=")


def decode_cursor(raw: str, fields: tuple[type, ...]) -> tuple[object, ...]:
    try:
        if len(raw) > 256:
            raise ValueError("Cursor too long")
        values = json.loads(base64.b64decode(raw + "=" * (-len(raw) % 4), altchars=b"-_", validate=True))
        if not isinstance(values, list) or len(values) != len(fields):
            raise ValueError("Cursor length mismatch")
        converted = []
        for text, kind in zip(values, fields):
            if not isinstance(text, str):
                raise ValueError("Invalid value")
            if kind is date:
                converted.append(date.fromisoformat(text))
            elif kind is datetime:
                converted.append(datetime.fromisoformat(text))
            elif kind is UUID:
                converted.append(str(UUID(text)))
            else:
                raise ValueError("Unsupported field")
        return tuple(converted)
    except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=422, detail="Invalid page cursor") from exc
