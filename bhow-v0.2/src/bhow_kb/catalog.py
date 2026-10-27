"""Versioned, traceable educational reference data; veterinary approval pending."""
import json
from functools import lru_cache
from importlib.resources import files

from bhow_core.food import IngredientRule


@lru_cache
def food_rules() -> tuple[IngredientRule, ...]:
    path = files("bhow_kb").joinpath("data/food_ingredients.json")
    source = json.loads(path.read_text(encoding="utf-8"))
    if source["review_status"] != "pending_veterinary_approval":
        raise ValueError("Unexpected KB release status; veterinary sign-off workflow required")
    return tuple(
        IngredientRule(
            name=record["name"],
            aliases=tuple(record["aliases"]),
            source_url=record["source_url"],
            reviewed_by_vet=False,
        )
        for record in source["ingredients"]
    )
