"""Product state and safety messaging are testable without native UI dependencies."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'client'))
from controller import CareController  # noqa: E402
from view_models import event_source, friendly_date, next_action, safe_ingredient_status  # noqa: E402


class FakeApi:
    def __init__(self):
        self.records = []

    def dogs(self):
        return self.records.copy()

    def add_dog(self, name, context):
        d = {'id':str(len(self.records)+1),'name':name,'care_context':context}
        self.records.append(d)
        return d


def test_profile_switch_and_creation():
    service = FakeApi()
    s = CareController(service)
    s.load()
    assert s.selected is None
    s.create(' Kaju ', 'owned')
    s.create('Tara', 'foster')
    assert s.selected['name'] == 'Tara'
    s.choose('1')
    assert s.selected['name'] == 'Kaju'
    try:
        s.choose('guess')
        assert False
    except ValueError:
        pass


def test_care_overview_wording():
    assert friendly_date('2026-10-27', today=date(2026, 10, 27)) == 'Today'
    assert friendly_date('2026-10-26', today=date(2026, 10, 27)).startswith('Overdue')
    assert next_action({'pending_tasks': []})[1] == 'Add your first reminder'
    assert event_source({'verified': False}).endswith('not vet verified')
    assert safe_ingredient_status({'status': 'unknown'})[0] == 'NOT ASSESSED AS SAFE'
    assert safe_ingredient_status({'status': 'potential_hazard'})[0] == 'POTENTIAL HAZARD'
    assert safe_ingredient_status({'status': 'invalid'})[0] == 'NOT ASSESSED AS SAFE'
