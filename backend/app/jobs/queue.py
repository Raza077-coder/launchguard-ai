from __future__ import annotations

from threading import Lock
from typing import Any


class ScanJobQueue:
    def __init__(self) -> None:
        self._jobs: dict[int, dict[str, Any]] = {}
        self._lock = Lock()

    def enqueue(self, scan_id: int, url: str) -> None:
        with self._lock:
            self._jobs[scan_id] = {
                "status": "QUEUED",
                "url": url,
                "events": [{"type": "queued", "message": f"Scan {scan_id} accepted."}],
            }

    def cancel(self, scan_id: int) -> None:
        with self._lock:
            if scan_id in self._jobs:
                self._jobs[scan_id]["status"] = "CANCELLED"
                self._jobs[scan_id]["events"].append({"type": "cancelled", "message": f"Scan {scan_id} cancelled."})

    def get_events(self, scan_id: int) -> list[dict[str, str]]:
        with self._lock:
            return self._jobs.get(scan_id, {"events": []})["events"]
    
    def add_event(self, scan_id: int, event_type: str, message: str) -> None:
        with self._lock:
            if scan_id in self._jobs:
                self._jobs[scan_id]["events"].append({"type": event_type, "message": message})
    
    def set_status(self, scan_id: int, status: str) -> None:
        with self._lock:
            if scan_id in self._jobs:
                self._jobs[scan_id]["status"] = status
