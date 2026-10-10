from __future__ import annotations

import asyncio
from app.database import SessionLocal
from app.models.scan import Scan
from app.models.finding import Finding
from app.jobs.queue import ScanJobQueue
from app.scanner.url_validator import validate_target_url
from app.scanner.crawler import discover_pages, check_broken_links
from app.scanner.finding_normalizer import normalize_findings

JOB_QUEUE = ScanJobQueue()


def run_scan(scan_id: int, url: str, max_pages: int = 25) -> None:
    """Run a deterministic website scan without Playwright (for initial MVP)."""
    findings_list: list[dict[str, object]] = []
    
    try:
        with SessionLocal() as db:
            scan = db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                return
            
            scan.status = "VALIDATING"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "validating", "Validating target URL...")
            
            # Step 1: Validate URL
            try:
                result = validate_target_url(url)
                JOB_QUEUE.add_event(scan_id, "validated", f"Target validated: {result['host']}")
            except ValueError as e:
                scan.status = "FAILED"
                db.commit()
                JOB_QUEUE.add_event(scan_id, "error", f"Validation failed: {str(e)}")
                return
            
            # Step 2: Discover pages
            scan.status = "DISCOVERING"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "discovering", "Discovering pages...")
            
            try:
                import httpx
                response = httpx.get(url, timeout=10.0)
                pages = discover_pages(url, response.text, max_pages=max_pages)
                JOB_QUEUE.add_event(scan_id, "discovered", f"Found {len(pages)} pages")
            except Exception as e:
                scan.status = "FAILED"
                db.commit()
                JOB_QUEUE.add_event(scan_id, "error", f"Page discovery failed: {str(e)}")
                return
            
            # Step 3: Check for broken links
            scan.status = "CHECKING"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "checking", "Checking links...")
            
            broken = check_broken_links(pages)
            for broken_url, status in broken.items():
                finding_dict = {
                    "category": "broken-link",
                    "title": f"Link returned HTTP {status}",
                    "severity": "medium" if status == 404 else "low",
                    "confidence": "high",
                    "affected_url": broken_url,
                    "description": f"Link check returned status {status}",
                }
                findings_list.append(finding_dict)
            
            JOB_QUEUE.add_event(scan_id, "checked", f"Found {len(broken)} broken links")
            
            # Step 4: Check metadata (basic SEO)
            scan.status = "ANALYZING"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "analyzing", "Checking metadata...")
            
            try:
                response = httpx.get(url, timeout=10.0)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Check for title
                title = soup.find("title")
                if not title or not title.string or title.string.strip() == "":
                    findings_list.append({
                        "category": "seo",
                        "title": "Missing or empty page title",
                        "severity": "medium",
                        "confidence": "high",
                        "affected_url": url,
                        "description": "The page title (in <title> tag) is missing or empty. Search engines and users rely on it.",
                    })
                
                # Check for meta description
                meta_desc = soup.find("meta", {"name": "description"})
                if not meta_desc or not meta_desc.get("content"):
                    findings_list.append({
                        "category": "seo",
                        "title": "Missing meta description",
                        "severity": "low",
                        "confidence": "high",
                        "affected_url": url,
                        "description": "The meta description is missing. This affects search engine snippets.",
                    })
                
                # Check images for missing alt text
                images = soup.find_all("img")
                missing_alt_count = 0
                for img in images:
                    if not img.get("alt"):
                        missing_alt_count += 1
                
                if missing_alt_count > 0:
                    findings_list.append({
                        "category": "accessibility",
                        "title": f"{missing_alt_count} images missing alt text",
                        "severity": "medium",
                        "confidence": "high",
                        "affected_url": url,
                        "description": f"Found {missing_alt_count} images without alt text. This hurts accessibility and SEO.",
                    })
            except Exception as e:
                JOB_QUEUE.add_event(scan_id, "warning", f"Metadata check partial: {str(e)}")
            
            # Step 5: Normalize findings
            scan.status = "NORMALIZING"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "normalizing", "Deduplicating findings...")
            
            normalized = normalize_findings(findings_list)
            
            # Step 6: Persist findings
            for finding_dict in normalized:
                finding = Finding(
                    scan_id=scan_id,
                    category=str(finding_dict.get("category", "general")),
                    title=str(finding_dict.get("title", "Issue")),
                    severity=str(finding_dict.get("severity", "low")),
                    confidence=str(finding_dict.get("confidence", "medium")),
                    affected_url=finding_dict.get("affected_url"),
                    description=str(finding_dict.get("description", "")),
                    evidence=finding_dict.get("evidence"),
                )
                db.add(finding)
            
            db.commit()
            JOB_QUEUE.add_event(scan_id, "saved", f"Saved {len(normalized)} findings")
            
            # Step 7: Complete
            scan.status = "COMPLETED"
            db.commit()
            JOB_QUEUE.add_event(scan_id, "completed", "Scan completed successfully")
    
    except Exception as e:
        with SessionLocal() as db:
            scan = db.query(Scan).filter(Scan.id == scan_id).first()
            if scan:
                scan.status = "FAILED"
                db.commit()
        JOB_QUEUE.add_event(scan_id, "error", f"Unexpected error: {str(e)}")
