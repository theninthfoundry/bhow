"""Deterministic hazard matching. Never returns a 'safe to eat' guarantee."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class IngredientMatch:
    name: str
    source_url: str
    reviewed_by_vet: bool


@dataclass(frozen=True)
class IngredientRule:
    name: str
    aliases: tuple[str, ...]
    source_url: str
    reviewed_by_vet: bool = False


def classify_ingredients(text: str, rules: tuple[IngredientRule, ...]) -> tuple[IngredientMatch, ...]:
    """Bounded literal token-phrase matching; punctuation and case are normalized.

    This is NOT a complete ingredient parser. OCR must require human confirmation.
    Don't do substring matches: 'cocoa' should not match arbitrary longer words.
    """
    normalized = re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()
    matches: list[IngredientMatch] = []
    for rule in rules:
        if any(re.search(r"(?:^|\s)" + re.escape(alias.lower()) + r"(?:\s|$)", normalized) for alias in rule.aliases):
            matches.append(IngredientMatch(rule.name, rule.source_url, rule.reviewed_by_vet))
    return tuple(matches)
