from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=list[ProjectRead])
def list_projects() -> list[ProjectRead]:
    with SessionLocal() as db:
        projects = db.query(Project).all()
        return [ProjectRead(id=p.id, name=p.name, url=p.url, description=p.description, is_demo=p.is_demo) for p in projects]


@router.post("/projects", response_model=ProjectRead)
def create_project(payload: ProjectCreate) -> ProjectRead:
    with SessionLocal() as db:
        project = Project(name=payload.name, url=payload.url, description=payload.description, is_demo=False)
        db.add(project)
        db.commit()
        db.refresh(project)
        return ProjectRead(id=project.id, name=project.name, url=project.url, description=project.description, is_demo=project.is_demo)


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int) -> ProjectRead:
    with SessionLocal() as db:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectRead(id=project.id, name=project.name, url=project.url, description=project.description, is_demo=project.is_demo)


@router.delete("/projects/{project_id}")
def delete_project(project_id: int) -> dict[str, str]:
    with SessionLocal() as db:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(project)
        db.commit()
        return {"status": "deleted", "project_id": str(project_id)}
