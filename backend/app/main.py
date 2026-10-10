from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.api.scans import router as scans_router
from app.api.findings import router as findings_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="LaunchGuard AI",
        description="Autonomous website reliability checks and repair planning",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/api")
    app.include_router(projects_router, prefix="/api")
    app.include_router(scans_router, prefix="/api")
    app.include_router(findings_router, prefix="/api")

    @app.on_event("startup")
    def startup() -> None:
        init_db()

    return app


app = create_app()
