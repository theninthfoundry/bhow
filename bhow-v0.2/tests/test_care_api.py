from datetime import date, timedelta
from uuid import uuid4


def test_full_care_flow_and_export(client):
    api, _ = client
    create = api.post("/v1/dogs", json={"name": "Kaju", "care_context": "community", "estimated_age_months": 20})
    assert create.status_code == 201, create.text
    dog = create.json()
    dog_id = dog["id"]
    assert dog["care_context"] == "community"
    assert len(api.get("/v1/dogs").json()) == 1
    event = api.post(f"/v1/dogs/{dog_id}/events", json={"kind": "visit", "notes": "Caregiver-reported visit", "occurred_on": "2026-10-27"})
    assert event.status_code == 201, event.text
    assert event.json()["verified"] is False
    task = api.post(f"/v1/dogs/{dog_id}/tasks", json={"kind": "appointment", "title": "Ask clinic about next checkup", "due_on": "2026-12-12"})
    assert task.status_code == 201, task.text
    done = api.post(f"/v1/dogs/{dog_id}/tasks/{task.json()['id']}/complete")
    assert done.json()["status"] == "completed"
    export = api.get("/v1/account/export").json()
    assert len(export["dogs"][0]["events"]) == 1
    assert len(export["dogs"][0]["tasks"]) == 1
    assert api.delete(f"/v1/dogs/{dog_id}").status_code == 204
    assert api.get("/v1/dogs").json() == []


def test_no_idor_cross_user_access(client):
    api, who = client
    dog_id = api.post("/v1/dogs", json={"name": "Bunty"}).json()["id"]
    who["sub"] = "user-b"
    assert api.get(f"/v1/dogs/{dog_id}").status_code == 404
    assert api.patch(f"/v1/dogs/{dog_id}", json={"name": "Stolen"}).status_code == 404
    assert api.get(f"/v1/dogs/{dog_id}/events").status_code == 404
    assert api.delete(f"/v1/dogs/{dog_id}").status_code == 404
    assert api.get("/v1/dogs").json() == []
    who["sub"] = "user-a"
    assert api.get(f"/v1/dogs/{dog_id}").json()["name"] == "Bunty"


def test_validation_and_no_fake_integrations(client):
    api, _ = client
    assert api.post("/v1/dogs", json={"name": "", "weight_kg": -2}).status_code == 422
    assert api.post("/v1/dogs", json={"name": "Kaju", "date_of_birth": str(date.today() + timedelta(days=1))}).status_code == 422
    assert api.get(f"/v1/dogs/{uuid4()}").status_code == 404
    assert api.post("/v1/integrations/breed/estimate").status_code == 503
    assert api.get("/v1/integrations/weather/live").status_code == 503
    assert api.get("/v1/outdoor/advice").json()["based_on_live_weather"] is False


def test_account_deletion(client):
    api, _ = client
    api.post("/v1/dogs", json={"name": "Luna"})
    assert api.delete("/v1/account/me").status_code == 204
    assert api.get("/v1/account/export").json()["dogs"] == []

# Edge case regression tests for care schedule intervals
