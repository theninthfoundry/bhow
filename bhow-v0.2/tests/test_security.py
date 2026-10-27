import pytest
from fastapi import HTTPException

from bhow_api.config import Settings
from bhow_api.security import current_principal


def test_local_demo_requires_explicit_opt_in():
    settings = Settings(app_env="local", allow_dev_auth=False)
    with pytest.raises(HTTPException) as error:
        current_principal(None, settings, "someone")
    assert error.value.status_code == 401


def test_local_demo_validates_identity_input():
    settings = Settings(app_env="local", allow_dev_auth=True)
    assert current_principal(None, settings, "owner_01").subject == "dev:owner_01"
    with pytest.raises(HTTPException) as error:
        current_principal(None, settings, "owner\nSet-Cookie:evil")
    assert error.value.status_code == 400


def test_dev_identity_rejected_when_staging():
    with pytest.raises(ValueError):
        Settings(app_env="staging", allow_dev_auth=True)


def test_food_input_size_limit(client):
    api, _ = client
    response = api.post("/v1/food/check", json={"ingredients_text": "a" * 3001})
    assert response.status_code == 422
