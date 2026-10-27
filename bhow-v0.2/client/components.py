"""Reusable editorial controls: accessible labels, quiet surfaces, clear provenance."""
import flet as ft

from tokens import COLORS


def kicker(label: str) -> ft.Text:
    return ft.Text(label.upper(), size=11, weight=ft.FontWeight.BOLD, color=COLORS.muted)


def heading(label: str, size: int = 32) -> ft.Text:
    return ft.Text(label, size=size, weight=ft.FontWeight.BOLD, color=COLORS.ink)


def caption(label: str) -> ft.Text:
    return ft.Text(label, size=13, color=COLORS.muted)


def rule() -> ft.Container:
    return ft.Container(height=1, bgcolor=COLORS.rule)


def panel(*controls: ft.Control, accent: bool = False) -> ft.Container:
    return ft.Container(
        bgcolor=COLORS.turmeric if accent else COLORS.surface,
        border_radius=12,
        padding=20,
        content=ft.Column(spacing=10, controls=list(controls)),
    )


def primary(label: str, click, *, accent: bool = False) -> ft.Button:
    return ft.Button(
        content=label,
        bgcolor=COLORS.turmeric if accent else COLORS.ink,
        color=COLORS.ink if accent else COLORS.surface,
        on_click=click,
    )


def quiet(label: str, click) -> ft.TextButton:
    return ft.TextButton(content=label, on_click=click)


def note_headline(kind: str, body: str) -> ft.Container:
    return panel(kicker(kind), caption(body))
