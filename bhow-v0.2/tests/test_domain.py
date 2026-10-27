from datetime import date

import pytest

from bhow_api.config import Settings
from bhow_core.breed import interpret_breed_scores
from bhow_core.food import classify_ingredients
from bhow_core.reminders import DueState, due_state
from bhow_kb.catalog import food_rules


def test_food_flags_and_uncertainty():
    rules = food_rules()
    items = classify_ingredients("Ingredients: Oat flour, RAISINS, cocoa powder", rules)
    assert {r.name for r in items} == {"grapes/raisins", "chocolate/cocoa"}
    assert classify_ingredients("all-natural oats", rules) == ()


def test_food_endpoint_never_returns_safe_verdict(client):
    api, _ = client
    risky = api.post("/v1/food/check", json={"ingredients_text": "Contains xylitol", "already_eaten": True}).json()
    assert risky["status"] == "potential_hazard"
    assert "veterinarian" in risky["next_step"]
    assert risky["flagged"][0]["reviewed_by_vet"] is False
    unknown = api.post("/v1/food/check", json={"ingredients_text": "Plain cooked rice"}).json()
    assert unknown["status"] == "unknown"
    assert "NOT mean safe" in unknown["summary"]


def test_due_dates():
    today = date(2026, 10, 27)
    assert due_state(today, today=today, completed=False) == DueState.DUE_TODAY
    assert due_state(date(2026, 10, 26), today=today, completed=False) == DueState.OVERDUE
    assert due_state(date(2026, 10, 26), today=today, completed=True) == DueState.COMPLETED


def test_breed_abstains_on_low_certainty():
    result = interpret_breed_scores({"indie_like": 0.44, "other": 0.37})
    assert result.abstained is True
    assert interpret_breed_scores({"example": 0.85}).abstained is False


def test_prod_config_fails_closed():
    with pytest.raises(ValueError):
        Settings(app_env="production", allow_dev_auth=True)
    with pytest.raises(ValueError):
        Settings(app_env="production", database_url="sqlite:///hello.db", allow_dev_auth=False)

# Domain test assertions verified for Phase 2 functional specs
