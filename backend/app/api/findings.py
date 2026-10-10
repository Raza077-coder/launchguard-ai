from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models.finding import Finding
from app.schemas.finding import FindingUpdate

router = APIRouter(tags=["findings"])


@router.get("/findings/{finding_id}")
def get_finding(finding_id: int) -> dict[str, object]:
    with SessionLocal() as db:
        finding = db.query(Finding).filter(Finding.id == finding_id).first()
        if not finding:
            raise HTTPException(status_code=404, detail="Finding not found")
        return {
            "id": finding.id,
            "scan_id": finding.scan_id,
            "category": finding.category,
            "title": finding.title,
            "severity": finding.severity,
            "confidence": finding.confidence,
            "affected_url": finding.affected_url,
            "description": finding.description,
            "status": finding.status,
        }


@router.patch("/findings/{finding_id}")
def update_finding(finding_id: int, payload: FindingUpdate) -> dict[str, object]:
    with SessionLocal() as db:
        finding = db.query(Finding).filter(Finding.id == finding_id).first()
        if not finding:
            raise HTTPException(status_code=404, detail="Finding not found")
        if payload.status is not None:
            finding.status = payload.status
        if payload.severity is not None:
            finding.severity = payload.severity
        db.commit()
        return {"status": "updated", "finding_id": finding_id}
