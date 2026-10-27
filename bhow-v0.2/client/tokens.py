"""Bhow Field Journal design language. No downloaded/generated art."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    paper: str = "#F4F0E7"
    ink: str = "#161713"
    muted: str = "#686A61"
    turmeric: str = "#F1BD37"
    surface: str = "#FFFFFF"
    rule: str = "#D6D3C9"
    danger: str = "#A9231B"
    forest: str = "#365B47"
    subtle: str = "#EBE5DA"


COLORS = Palette()
SPACING = (4, 8, 12, 16, 24, 32, 48, 64)
RADII = (4, 12)
