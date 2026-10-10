from __future__ import annotations

from pydantic import BaseModel, Field


class FindingUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(open|reviewed|accepted|false_positive|fixed)$")
    severity: str | None = Field(default=None)
