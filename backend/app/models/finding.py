from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="QUEUED")
    profile: Mapped[str] = mapped_column(String(50), default="standard")
    max_pages: Mapped[int] = mapped_column(default=25)
    viewport: Mapped[str] = mapped_column(String(50), default="desktop")
    created_at: Mapped[str] = mapped_column(default="NOW")
    updated_at: Mapped[str] = mapped_column(default="NOW")

    project: Mapped["Project"] = relationship(backref="scans")
