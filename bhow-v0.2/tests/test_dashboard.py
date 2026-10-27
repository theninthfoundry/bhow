"""Overview aggregation is isolated, bounded, and honest about source."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def test_dashboard_uses_only_own_care_records(client):
    api, who = client
    a = api.post('/v1/dogs', json={'name': 'Kaju'}).json()['id']
    b = api.post('/v1/dogs', json={'name': 'Bunty'}).json()['id']
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    older = (today - timedelta(days=2)).isoformat()
    tomorrow = (today + timedelta(days=1)).isoformat()
    for title, due in [('Past visit', older), ('Next visit', tomorrow)]:
        response = api.post(f'/v1/dogs/{a}/tasks', json={'kind': 'appointment', 'title': title, 'due_on': due})
        assert response.status_code == 201
    completed = api.post(f'/v1/dogs/{a}/tasks', json={'kind':'grooming','title':'Done', 'due_on': older}).json()['id']
    api.post(f'/v1/dogs/{a}/tasks/{completed}/complete')
    api.post(f'/v1/dogs/{a}/events', json={'kind':'visit','notes':'Caregiver note','occurred_on':today.isoformat()})
    api.post(f'/v1/dogs/{b}/events', json={'kind':'visit','notes':'Bunty private','occurred_on':today.isoformat()})
    result = api.get(f'/v1/dogs/{a}/overview')
    assert result.status_code == 200
    body = result.json()
    assert body['dog']['name'] == 'Kaju'
    assert body['pending_count'] == 2
    assert body['overdue_count'] == 1
    assert [t['title'] for t in body['pending_tasks']] == ['Past visit','Next visit']
    assert len(body['recent_events']) == 1
    assert body['recent_events'][0]['verified'] is False
    assert body['status'] == 'records_only_no_clinical_assessment'
    who['sub'] = 'someone-else'
    assert api.get(f'/v1/dogs/{a}/overview').status_code == 404


def test_empty_overview_has_no_false_green_health_signal(client):
    api, _ = client
    dog_id = api.post('/v1/dogs', json={'name': 'Poppy'}).json()['id']
    body = api.get(f'/v1/dogs/{dog_id}/overview').json()
    assert body['pending_count'] == body['overdue_count'] == 0
    assert body['recent_events'] == []
    assert body['status'] == 'records_only_no_clinical_assessment'


def test_overview_rejects_unknown_timezone(client):
    api, _ = client
    dog_id = api.post('/v1/dogs', json={'name': 'Tara'}).json()['id']
    assert api.get(f'/v1/dogs/{dog_id}/overview?tz=NoSuch/Zone').status_code == 422
    assert api.get(f'/v1/dogs/{dog_id}/overview?tz=Asia/Kolkata').status_code == 200

# UI regression assertions for summary widgets
