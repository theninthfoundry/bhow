"""Educational food hazard flags and offline outdoor guidance; no fake certainty."""
from fastapi import APIRouter

from bhow_api.schemas import FoodCheckIn, FoodCheckOut, FoodFlag
from bhow_core.food import classify_ingredients
from bhow_core.walk import offline_outdoor_advice
from bhow_kb.catalog import food_rules

router = APIRouter(tags=["knowledge"])


@router.post("/food/check", response_model=FoodCheckOut)
def check_food(payload: FoodCheckIn) -> FoodCheckOut:
    flagged = classify_ingredients(payload.ingredients_text, food_rules())
    if flagged:
        return FoodCheckOut(
            status="potential_hazard",
            flagged=[FoodFlag(ingredient=x.name, reference="ASPCA educational reference", source_url=x.source_url, reviewed_by_vet=False) for x in flagged],
            summary="One or more ingredients are listed as potential hazards. This is not a comprehensive assessment.",
            next_step=(
                "If your dog may have eaten this, contact a veterinarian or animal poison service immediately."
                if payload.already_eaten else
                "Do not offer this food. Check the full label with a veterinary professional if uncertain."
            ),
        )
    return FoodCheckOut(
        status="unknown",
        flagged=[],
        summary="No match in our LIMITED preview reference; this does NOT mean safe for dogs.",
        next_step=("If potentially harmful food was eaten, call a veterinarian now." if payload.already_eaten else "Ask a veterinarian before offering unfamiliar products."),
    )


@router.get("/outdoor/advice")
def outdoor_advice() -> dict[str, object]:
    advice = offline_outdoor_advice()
    return {
        "category": advice.category,
        "headline": advice.headline,
        "reminders": list(advice.reminders),
        "based_on_live_weather": advice.based_on_live_weather,
    }
