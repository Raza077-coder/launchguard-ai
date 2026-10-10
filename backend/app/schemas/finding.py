from __future__ import annotations

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    project_id: int | None = None
    url: str = Field(..., min_length=1, max_length=2048)
    profile: str = "standard"
    max_pages: int = Field(25, ge=1, le=200)
    viewport: str = "desktop"


class ScanRead(BaseModel):
    id: int
    project_id: int | None = None
    url: str
    status: str
    profile: str
    max_pages: int
    viewport: str
