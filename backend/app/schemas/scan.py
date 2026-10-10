from __future__ import annotations

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=2048)
    description: str | None = None


class ProjectRead(BaseModel):
    id: int
    name: str
    url: str
    description: str | None = None
    is_demo: bool = False
