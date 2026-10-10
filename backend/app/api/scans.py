from __future__ import annotations

from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio

from app.database import SessionLocal
from app.jobs.queue import ScanJobQueue
from app.models.scan import Scan
from app.models.finding import Finding
from app.schemas.scan import ScanCreate, ScanRead
from app.scanner.runner import run_scan

router = APIRouter(tags=["scans"])

JOB_QUEUE = ScanJobQueue()


@router.post("/scans", response_model=ScanRead)
def create_scan(payload: ScanCreate, background_tasks: BackgroundTasks) -> ScanRead:
    with SessionLocal() as db:
        scan = Scan(
            project_id=payload.project_id,
            url=payload.url,
            status="QUEUED",
            profile=payload.profile,
            max_pages=payload.max_pages,
            viewport=payload.viewport,
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Enqueue the scan job to run in the background
        background_tasks.add_task(run_scan, scan.id, payload.url, payload.max_pages)
        JOB_QUEUE.enqueue(scan.id, payload.url)
        
        return ScanRead(
            id=scan.id,
            project_id=scan.project_id,
            url=scan.url,
            status=scan.status,
            profile=scan.profile,
            max_pages=scan.max_pages,
            viewport=scan.viewport,
        )


@router.get("/scans", response_model=list[ScanRead])
def list_scans() -> list[ScanRead]:
    with SessionLocal() as db:
        scans = db.query(Scan).all()
        return [
            ScanRead(
                id=s.id,
                project_id=s.project_id,
                url=s.url,
                status=s.status,
                profile=s.profile,
                max_pages=s.max_pages,
                viewport=s.viewport,
            )
            for s in scans
        ]


@router.get("/scans/{scan_id}", response_model=ScanRead)
def get_scan(scan_id: int) -> ScanRead:
    with SessionLocal() as db:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        return ScanRead(
            id=scan.id,
            project_id=scan.project_id,
            url=scan.url,
            status=scan.status,
            profile=scan.profile,
            max_pages=scan.max_pages,
            viewport=scan.viewport,
        )


@router.post("/scans/{scan_id}/cancel")
def cancel_scan(scan_id: int) -> dict[str, str]:
    with SessionLocal() as db:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        scan.status = "CANCELLED"
        db.commit()
        JOB_QUEUE.cancel(scan_id)
        return {"status": "cancelled", "scan_id": str(scan_id)}


@router.get("/scans/{scan_id}/events")
def scan_events(scan_id: int) -> list[dict[str, str]]:
    return JOB_QUEUE.get_events(scan_id)


@router.get("/scans/{scan_id}/findings")
def scan_findings(scan_id: int) -> list[dict[str, object]]:
    with SessionLocal() as db:
        findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
        return [
            {
                "id": f.id,
                "title": f.title,
                "severity": f.severity,
                "category": f.category,
                "status": f.status,
                "affected_url": f.affected_url,
                "description": f.description,
            }
            for f in findings
        ]


@router.get("/scans/{scan_id}/report")
def scan_report(scan_id: int) -> dict[str, object]:
    with SessionLocal() as db:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
        
        # Calculate health score based on findings
        score = 100
        weights = {"critical": 35, "high": 20, "medium": 10, "low": 5}
        for finding in findings:
            score -= weights.get(finding.severity, 5)
        score = max(0, score)
        
    return {
        "scan_id": scan_id,
        "url": scan.url,
        "status": scan.status,
        "overall_health_score": score,
        "findings_count": len(findings),
        "findings": [
            {
                "id": f.id,
                "title": f.title,
                "severity": f.severity,
                "category": f.category,
                "affected_url": f.affected_url,
                "description": f.description,
            }
            for f in findings
        ],
    }
