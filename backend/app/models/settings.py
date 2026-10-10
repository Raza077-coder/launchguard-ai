from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RepairPlan(Base):
    __tablename__ = "repair_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), nullable=False)
    summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(default="NOW")


class RepairProposal(Base):
    __tablename__ = "repair_proposals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    patch: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(default="NOW")


class VerificationRun(Base):
    __tablename__ = "verification_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    proposal_id: Mapped[int | None] = mapped_column(ForeignKey("repair_proposals.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    output: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(default="NOW")
