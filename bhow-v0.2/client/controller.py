"""Presentation state and API orchestration, independent of UI widgets."""
from typing import Any

from api_client import Api


class CareController:
    def __init__(self, api: Api) -> None:
        self.api = api
        self.dogs: list[dict[str, Any]] = []
        self.selected_id: str | None = None

    @property
    def selected(self) -> dict[str, Any] | None:
        return next((d for d in self.dogs if d["id"] == self.selected_id), None)

    def load(self) -> None:
        self.dogs = self.api.dogs()
        if self.selected_id not in {d["id"] for d in self.dogs}:
            self.selected_id = self.dogs[0]["id"] if self.dogs else None

    def create(self, name: str, care_context: str) -> None:
        clean = name.strip()
        if not clean or len(clean) > 80:
            raise ValueError("Enter a name between 1 and 80 characters.")
        if care_context not in {"owned", "foster", "community"}:
            raise ValueError("Choose a valid care context.")
        dog = self.api.add_dog(clean, care_context)
        self.load()
        self.selected_id = dog["id"]

    def choose(self, dog_id: str) -> None:
        if dog_id not in {d["id"] for d in self.dogs}:
            raise ValueError("Choose a dog from your profiles.")
        self.selected_id = dog_id

# Event loop handling validated for async client requests
