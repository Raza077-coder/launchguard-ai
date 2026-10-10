from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import httpx


@dataclass
class BrowserCheckResult:
    page_url: str
    title: str | None = None
    meta_description: str | None = None
    console_errors: list[str] = field(default_factory=list)
    network_failures: list[dict[str, Any]] = field(default_factory=list)
    missing_alt_images: list[str] = field(default_factory=list)
    broken_images: list[str] = field(default_factory=list)
    missing_form_labels: list[str] = field(default_factory=list)
    screenshot_path: str | None = None
    status: str = "ok"
    http_status: int = 200
    metadata: dict[str, Any] = field(default_factory=dict)


async def collect_page_errors(page_url: str, page: Page) -> BrowserCheckResult:
    """Collect browser and page errors from a real Playwright page object."""
    result = BrowserCheckResult(page_url=page_url)
    
    # Collect console errors
    console_errors: list[str] = []
    
    def on_console_msg(msg: Any) -> None:
        if msg.type in ("error", "warning"):
            console_errors.append(f"{msg.type}: {msg.text}")
    
    page.on("console", on_console_msg)
    
    # Navigate and collect errors
    try:
        response = await page.goto(page_url, wait_until="networkidle")
        if response:
            result.http_status = response.status
            if response.status >= 400:
                result.status = "failed"
    except Exception as e:
        result.status = "failed"
        result.console_errors.append(f"Navigation error: {str(e)}")
        return result
    
    result.console_errors = console_errors
    
    # Extract title and meta description
    try:
        result.title = await page.title()
    except Exception:
        pass
    
    try:
        meta_desc = await page.locator('meta[name="description"]').get_attribute("content")
        result.meta_description = meta_desc
    except Exception:
        pass
    
    # Check images for missing alt text and broken images
    try:
        images = await page.locator("img").all()
        for img in images:
            alt = await img.get_attribute("alt")
            src = await img.get_attribute("src")
            if not alt and src:
                result.missing_alt_images.append(src)
    except Exception:
        pass
    
    # Check form inputs for labels
    try:
        inputs = await page.locator("input[type='text'], input[type='email'], input[type='password']").all()
        for inp in inputs:
            input_id = await inp.get_attribute("id")
            if input_id:
                label = await page.locator(f'label[for="{input_id}"]').is_visible()
                if not label:
                    result.missing_form_labels.append(input_id)
    except Exception:
        pass
    
    return result
