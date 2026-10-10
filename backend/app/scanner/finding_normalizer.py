from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrowserCheckResult:
    page_url: str
    console_errors: list[str] = field(default_factory=list)
    network_failures: list[str] = field(default_factory=list)
    screenshot_path: str | None = None
    status: str = "ok"
    metadata: dict[str, Any] = field(default_factory=dict)


def collect_page_errors(page_url: str, html: str | None = None) -> BrowserCheckResult:
    console_errors: list[str] = []
    if "error" in (html or "").lower():
        console_errors.append("Potential runtime issue detected in page source.")
    return BrowserCheckResult(
        page_url=page_url,
        console_errors=console_errors,
        network_failures=[],
        screenshot_path=None,
        status="ok",
        metadata={"checked": True},
    )
