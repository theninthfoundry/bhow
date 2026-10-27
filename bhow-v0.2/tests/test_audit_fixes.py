from datetime import date, timedelta

from bhow_core.food import classify_ingredients
from bhow_kb.catalog import food_rules


def test_alias_e_code():
    assert any(x.name == "xylitol" for x in classify_ingredients("E-967", food_rules()))
    assert any(x.name == "xylitol" for x in classify_ingredients("E 967", food_rules()))


def test_names_are_trimmed_and_blank_rejected(client):
    api, _ = client
    assert api.post("/v1/dogs", json={"name": "   "}).status_code == 422
    result = api.post("/v1/dogs", json={"name": "  Bruno  "})
    assert result.status_code == 201
    dog_id = result.json()["id"]
    assert result.json()["name"] == "Bruno"
    assert api.patch(f"/v1/dogs/{dog_id}", json={"name": "  "}).status_code == 422
    assert api.patch(f"/v1/dogs/{dog_id}", json={"name": "  Bud  "}).json()["name"] == "Bud"


def test_tasks_and_events_idempotency(client):
    api, _ = client
    dog = api.post("/v1/dogs", json={"name": "Milo"}).json()["id"]
    body = {"kind": "appointment", "title": "Call vet", "due_on": "2026-12-01"}
    headers = {"Idempotency-Key": "same-task-12345"}
    a = api.post(f"/v1/dogs/{dog}/tasks", json=body, headers=headers)
    b = api.post(f"/v1/dogs/{dog}/tasks", json=body, headers=headers)
    assert a.status_code == b.status_code == 201
    assert a.json()["id"] == b.json()["id"]
    assert len(api.get(f"/v1/dogs/{dog}/tasks").json()) == 1
    assert api.post(f"/v1/dogs/{dog}/tasks", json={**body, "title": "Changed"}, headers=headers).status_code == 409
    ebody = {"kind": "other", "notes": "Still playing", "occurred_on": "2026-10-20"}
    eheaders = {"Idempotency-Key": "same-event-1234"}
    a = api.post(f"/v1/dogs/{dog}/events", json=ebody, headers=eheaders)
    b = api.post(f"/v1/dogs/{dog}/events", json=ebody, headers=eheaders)
    assert a.status_code == b.status_code == 201
    assert a.json()["id"] == b.json()["id"]
    assert len(api.get(f"/v1/dogs/{dog}/events").json()) == 1


def test_complete_history_across_pages_and_user_isolation(client):
    api, who = client
    dog = api.post("/v1/dogs", json={"name": "Puppy"}).json()["id"]
    for i in range(201):
        result = api.post(f"/v1/dogs/{dog}/events", json={"kind": "other", "notes": f"note-{i}", "occurred_on": "2026-10-20"})
        assert result.status_code == 201
    all_ids = set()
    next_cursor = None
    for _ in range(10):
        params = {"limit": 37}
        if next_cursor:
            params["cursor"] = next_cursor
        resp = api.get(f"/v1/dogs/{dog}/events/page", params=params)
        assert resp.status_code == 200, resp.text
        page = resp.json()
        for item in page["items"]:
            assert item["id"] not in all_ids
            all_ids.add(item["id"])
        next_cursor = page["next_cursor"]
        if not next_cursor:
            break
    assert len(all_ids) == 201
    assert not next_cursor
    who["sub"] = "other-user"
    assert api.get(f"/v1/dogs/{dog}/events/page").status_code == 404


def test_task_paging_and_filters(client):
    api, _ = client
    dog = api.post("/v1/dogs", json={"name": "Suki"}).json()["id"]
    ids = []
    for i in range(103):
        d = (date(2026, 10, 27) + timedelta(days=i % 3)).isoformat()
        created = api.post(f"/v1/dogs/{dog}/tasks", json={"kind": "other", "title": f"Task-{i}", "due_on": d})
        ids.append(created.json()["id"])
    api.post(f"/v1/dogs/{dog}/tasks/{ids[0]}/complete")
    found, cursor = set(), None
    for _ in range(10):
        params = {"limit": 19, "status": "pending"}
        if cursor:
            params["cursor"] = cursor
        response = api.get(f"/v1/dogs/{dog}/tasks/page", params=params)
        assert response.status_code == 200
        data = response.json()
        found.update(x["id"] for x in data["items"])
        cursor = data["next_cursor"]
        if not cursor:
            break
    assert len(found) == 102 and ids[0] not in found
    assert api.get(f"/v1/dogs/{dog}/tasks/page?cursor=%$#").status_code == 422


def test_unreviewed_food_does_not_claim_safe(client):
    api, _ = client
    response = api.post("/v1/food/check", json={"ingredients_text": "unknown ingredient"})
    assert response.json()["status"] == "unknown"
    assert response.json()["kb_release_status"] == "educational_preview_not_vet_reviewed"


def test_dog_list_across_pages(client):
    api, _ = client
    for n in range(11):
        assert api.post("/v1/dogs", json={"name": f"Dog {n}"}).status_code == 201
    result = []
    cursor = None
    for _ in range(5):
        params = {"limit": 4}
        if cursor:
            params["cursor"] = cursor
        response = api.get("/v1/dogs/page", params=params)
        assert response.status_code == 200, response.text
        page = response.json()
        result.extend(d["id"] for d in page["items"])
        cursor = page["next_cursor"]
        if not cursor:
            break
    assert len(result) == 11 and len(result) == len(set(result))
