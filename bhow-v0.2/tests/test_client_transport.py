"""No local demo header should ever be sent to a remote host."""
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'client'))
from api_client import Api, ApiError  # noqa: E402


def test_local_preview_headers_do_not_become_remote_auth(monkeypatch):
    monkeypatch.setenv('BH_CLIENT_DEV_AUTH', 'true')
    with pytest.raises(RuntimeError, match='local'):
        Api('https://api.example.org')
    with pytest.raises(RuntimeError, match='local'):
        Api('http://192.168.1.10:8000')

    def respond(req: httpx.Request):
        assert req.headers.get('X-Dev-User') == 'flet-preview'
        assert 'Authorization' not in req.headers
        return httpx.Response(200, json={"items": [], "next_cursor": None})

    api = Api('http://localhost:8000', transport=httpx.MockTransport(respond))
    assert api.dogs() == []


def test_remote_bearer_requires_tls(monkeypatch):
    monkeypatch.delenv('BH_CLIENT_DEV_AUTH', raising=False)
    monkeypatch.setenv('BH_ACCESS_TOKEN', 'test-token')
    with pytest.raises(RuntimeError, match='HTTPS'):
        Api('http://bhow.example.org')
    api = Api('https://api.example.org', transport=httpx.MockTransport(
        lambda req: httpx.Response(401, json={'detail':'secret internal'})))
    with pytest.raises(ApiError, match='session') as err:
        api.dogs()
    assert 'secret internal' not in str(err.value)


def test_timeout_message_not_raw_error(monkeypatch):
    monkeypatch.setenv('BH_CLIENT_DEV_AUTH', 'true')
    monkeypatch.delenv('BH_ACCESS_TOKEN', raising=False)
    def timeout(req: httpx.Request):
        raise httpx.ReadTimeout('internal stack trace', request=req)
    api = Api('http://127.0.0.1:8000', transport=httpx.MockTransport(timeout))
    with pytest.raises(ApiError, match='timed out') as err:
        api.dogs()
    assert 'internal stack trace' not in str(err.value)
