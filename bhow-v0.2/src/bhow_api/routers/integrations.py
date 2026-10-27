"""Explicit unavailable states for unconnected providers; no fabricated predictions."""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.post("/breed/estimate")
def estimate_breed() -> None:
    raise HTTPException(status_code=503, detail="Model not deployed. See docs/08_AI_ML.md")


@router.get("/places/nearby")
def nearby_places() -> None:
    raise HTTPException(status_code=503, detail="Verified directory provider not connected")


@router.get("/weather/live")
def live_weather() -> None:
    raise HTTPException(status_code=503, detail="Licensed weather provider not connected")
