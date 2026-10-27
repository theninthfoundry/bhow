"""Application factory; import has no migration or network side effects."""
from uuid import uuid4

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from bhow_api.db import get_engine
from bhow_api.config import get_settings
from bhow_api.routers import account, care, dashboard, dogs, integrations, knowledge


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Bhow Care OS API",
        version="0.3.1",
        description="Dog care records and bounded educational support. Not veterinary diagnosis.",
        docs_url="/docs" if settings.app_env in {"local", "test"} else None,
        redoc_url=None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Dev-User",
            "X-Request-ID",
            "Idempotency-Key",
            "idempotency-key",
        ],
    )

    @app.middleware("http")
    async def add_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", str(uuid4()))[:64]
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/healthz", tags=["operations"])
    def healthz() -> dict[str, str]:
        return {"status": "ok"}  # process liveness, NOT database or provider readiness

    @app.get("/readyz", tags=["operations"])
    def readyz() -> dict[str, str]:
        try:
            with get_engine().connect() as conn:
                version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one_or_none()
                if version != "0002":
                    raise HTTPException(status_code=503, detail="Database schema not current")
                conn.execute(text("SELECT 1 FROM dogs LIMIT 1"))
                conn.execute(text("SELECT 1 FROM idempotency_records LIMIT 1"))
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=503, detail="Database unavailable") from exc
        return {"status": "ready"}

    app.include_router(account.router, prefix="/v1")
    app.include_router(dogs.router, prefix="/v1")
    app.include_router(care.router, prefix="/v1")
    app.include_router(dashboard.router, prefix="/v1")
    app.include_router(knowledge.router, prefix="/v1")
    app.include_router(integrations.router, prefix="/v1")
    return app


app = create_app()
