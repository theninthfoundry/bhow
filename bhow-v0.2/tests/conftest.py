"""HTTP integration tests exercise the real DB and object-level permissions."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from bhow_api.db import Base, get_db
from bhow_api.main import create_app
from bhow_api.security import Principal, current_principal


@pytest.fixture
def client():
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.state.disable_rate_limit = True
    who = {"sub": "user-a"}

    def session_override():
        with Session(engine, expire_on_commit=False) as session:
            yield session

    def identity_override():
        return Principal(subject=who["sub"])

    app.dependency_overrides[get_db] = session_override
    app.dependency_overrides[current_principal] = identity_override
    with TestClient(app) as test_client:
        yield test_client, who
    engine.dispose()
