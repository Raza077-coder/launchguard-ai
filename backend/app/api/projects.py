from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "app": "LaunchGuard AI",
        "mode": "deterministic-local",
        "version": "0.1.0",
    }
