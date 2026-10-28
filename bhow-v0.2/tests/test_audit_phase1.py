"""Phase 1 verification: Care Passport, Event Corrections, Food Ingestion Escalation, and Dual-DB Backup Rehearsal."""
from datetime import date
from uuid import uuid4

from tools.backup_restore import restore_and_verify


def test_dog_care_passport_extended_fields(client):
    api, _ = client
    payload = {
        "name": "Sheru",
        "breed_reported": "Indie",
        "weight_kg": 18.5,
        "care_context": "owned",
        "allergies_reported": "Chicken protein sensitivity",
        "conditions_reported": "Mild hip dysplasia",
        "medications_reported": "Omega-3 fish oil daily",
        "microchip_id": "985141002938123",
        "veterinarian_contact": "Dr. Sharma, Pet Care Clinic (+91-9876543210)",
    }
    create_res = api.post("/v1/dogs", json=payload)
    assert create_res.status_code == 201, create_res.text
    dog = create_res.json()
    assert dog["name"] == "Sheru"
    assert dog["allergies_reported"] == "Chicken protein sensitivity"
    assert dog["microchip_id"] == "985141002938123"

    # Verify retrieval
    get_res = api.get(f"/v1/dogs/{dog['id']}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["conditions_reported"] == "Mild hip dysplasia"
    assert retrieved["medications_reported"] == "Omega-3 fish oil daily"

    # Verify patch
    patch_res = api.patch(f"/v1/dogs/{dog['id']}", json={"allergies_reported": "Chicken and dairy sensitivity"})
    assert patch_res.status_code == 200
    assert patch_res.json()["allergies_reported"] == "Chicken and dairy sensitivity"


def test_care_event_correction_workflow_preserves_history(client):
    api, who = client
    dog = api.post("/v1/dogs", json={"name": "Kaju"}).json()
    dog_id = dog["id"]

    # 1. Create original care event
    event1 = api.post(
        f"/v1/dogs/{dog_id}/events",
        json={"kind": "weight", "notes": "Recorded 25kg", "occurred_on": "2026-10-25"},
    ).json()
    assert event1["supersedes_event_id"] is None
    assert event1["correction_reason"] is None

    # 2. Submit a correction linking to the original event
    corr_payload = {
        "kind": "weight",
        "notes": "Correction: Scale was uncalibrated; true weight 22.5kg",
        "occurred_on": "2026-10-25",
        "correction_reason": "Scale calibration offset error noticed by caregiver",
    }
    corr_res = api.post(f"/v1/dogs/{dog_id}/events/{event1['id']}/correct", json=corr_payload)
    assert corr_res.status_code == 201, corr_res.text
    event2 = corr_res.json()

    assert event2["supersedes_event_id"] == event1["id"]
    assert event2["correction_reason"] == "Scale calibration offset error noticed by caregiver"
    assert event2["notes"] == "Correction: Scale was uncalibrated; true weight 22.5kg"

    # 3. Verify history preserves BOTH events (original is not destroyed)
    page_res = api.get(f"/v1/dogs/{dog_id}/events/page")
    assert page_res.status_code == 200
    items = page_res.json()["items"]
    event_ids = [e["id"] for e in items]
    assert event1["id"] in event_ids
    assert event2["id"] in event_ids

    # 4. Cross-user IDOR check on event correction
    who["sub"] = "unauthorized-user"
    idor_res = api.post(
        f"/v1/dogs/{dog_id}/events/{event1['id']}/correct",
        json=corr_payload,
    )
    assert idor_res.status_code == 404


def test_food_ingestion_emergency_guidance(client):
    api, _ = client

    # Pre-feeding check with hazard
    pre_feed = api.post("/v1/food/check", json={"ingredients_text": "chocolate cocoa", "already_eaten": False})
    assert pre_feed.status_code == 200
    pre_data = pre_feed.json()
    assert pre_data["status"] == "potential_hazard"
    assert pre_data["emergency_escalation"] is None

    # Suspected ingestion of hazard
    eaten_hazard = api.post("/v1/food/check", json={"ingredients_text": "chocolate cocoa", "already_eaten": True})
    assert eaten_hazard.status_code == 200
    hazard_data = eaten_hazard.json()
    assert hazard_data["status"] == "potential_hazard"
    assert hazard_data["emergency_escalation"] is not None
    assert hazard_data["emergency_escalation"]["urgency"] == "immediate"
    assert "licensed emergency veterinarian" in hazard_data["emergency_escalation"]["action"]

    # Suspected ingestion of unknown substance
    eaten_unknown = api.post("/v1/food/check", json={"ingredients_text": "strange unknown plant leaf", "already_eaten": True})
    assert eaten_unknown.status_code == 200
    unknown_data = eaten_unknown.json()
    assert unknown_data["status"] == "unknown"
    assert unknown_data["emergency_escalation"] is not None
    assert unknown_data["emergency_escalation"]["urgency"] == "immediate"


def test_database_backup_restore_rehearsal():
    # Test dual-target in-memory rehearsal
    source_url = "sqlite+pysqlite:///:memory:"
    target_url = "sqlite+pysqlite:///:memory:"

    from sqlalchemy import create_engine
    from bhow_api.db import Base
    from bhow_api.models import Dog, DogCaregiver, CareEvent

    # Setup source with representative schema and records
    source_engine = create_engine(source_url)
    Base.metadata.create_all(bind=source_engine)

    from sqlalchemy.orm import Session
    with Session(source_engine) as session:
        dog = Dog(name="Leo", care_context="owned")
        session.add(dog)
        session.flush()
        session.add(DogCaregiver(dog_id=dog.id, subject="owner-user", role="owner"))
        session.add(CareEvent(dog_id=dog.id, kind="walk", notes="Morning park walk", occurred_on=date.today(), created_by="owner-user"))
        session.commit()

    # Rehearse backup and restore into target
    metrics = restore_and_verify(source_url, target_url)
    assert metrics["status"] == "PASS"
    assert metrics["verified_tables"] >= 5
    assert metrics["table_counts"]["dogs"] == 1
    assert metrics["table_counts"]["dog_caregivers"] == 1
    assert metrics["table_counts"]["care_events"] == 1
