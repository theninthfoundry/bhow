"""Cautious education, not a medical risk score or live forecast."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OutdoorAdvice:
    category: str
    headline: str
    reminders: tuple[str, ...]
    based_on_live_weather: bool


def offline_outdoor_advice() -> OutdoorAdvice:
    return OutdoorAdvice(
        category="conditions_unknown",
        headline="Check local weather and pavement before walking.",
        reminders=(
            "Avoid strenuous activity when conditions are hot or humid.",
            "Carry water; seek shade and cool conditions.",
            "Short-nosed, very young, senior, or unwell dogs may need extra caution.",
        ),
        based_on_live_weather=False,
    )
