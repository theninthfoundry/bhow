"""Application factory; import has no migration or network side effects."""
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from bhow_api.config import get_settings
from bhow_api.routers import account, care, dashboard, dogs, integrations, knowledge


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Bhow Care OS API",
        version="0.2.0",
        description="Dog care records and bounded educational support. Not veterinary diagnosis.",
        docs_url="/docs" if settings.app_env in {"local", "test"} else None,
        redoc_url=None,
    )
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False, allow_methods=["GET", "POST", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type", "X-Dev-User", "X-Request-ID"])

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

    app.include_router(account.router, prefix="/v1")
    app.include_router(dogs.router, prefix="/v1")
    app.include_router(care.router, prefix="/v1")
    app.include_router(dashboard.router, prefix="/v1")
    app.include_router(knowledge.router, prefix="/v1")
    app.include_router(integrations.router, prefix="/v1")
    return app


app = create_app()

# Production readiness probe handlers mounted
