"""Typed ports for future vendor adapters.

Keep integrations replaceable and distinguish absence from unreliable results.
These protocols are not live service integrations.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class WeatherSnapshot:
    temperature_c: float
    relative_humidity_pct: float
    observed_at: datetime
    source: str
    license_id: str


@dataclass(frozen=True)
class BreedPrediction:
    label: str
    calibrated_score: float
    model_version: str


@dataclass(frozen=True)
class VerifiedPlace:
    id: str
    name: str
    address: str
    contact_number: str | None
    last_verified_at: datetime | None
    provides_emergency_care: bool | None  # None means unknown, not False.


class WeatherProvider(Protocol):
    def current(self, latitude: float, longitude: float) -> WeatherSnapshot: ...


class BreedInferenceProvider(Protocol):
    def predict(self, image_bytes: bytes) -> tuple[BreedPrediction, ...]: ...


class PlaceDirectory(Protocol):
    def nearby(self, latitude: float, longitude: float, radius_km: float) -> list[VerifiedPlace]: ...


class PrivateAssetStore(Protocol):
    def presign_upload(self, owner_subject: str, object_id: str, content_type: str) -> str: ...
    def delete(self, object_id: str) -> None: ...


class NotificationProvider(Protocol):
    def send(self, destination_token: str, message: str, idempotency_key: str) -> str: ...
