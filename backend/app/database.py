from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from app.models.project import Project
    from app.models.scan import Scan
    from app.models.finding import Finding
    from app.models.repair import RepairPlan, RepairProposal, VerificationRun
    from app.models.settings import AppSetting

    Base.metadata.create_all(bind=engine)
