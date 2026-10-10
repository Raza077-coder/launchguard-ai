from __future__ import annotations

from urllib.parse import urljoin, urlparse
from typing import Set

from bs4 import BeautifulSoup
import httpx

from app.scanner.url_validator import validate_redirect_url


def discover_pages(base_url: str, html: str, max_pages: int = 25, max_depth: int = 2) -> list[str]:
    """Discover same-origin pages from HTML with depth and page limits."""
    soup = BeautifulSoup(html, "html.parser")
    discovered_urls: list[str] = [base_url]
    visited: Set[str] = {base_url}
    
    def get_base_url(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    base_domain = get_base_url(base_url)
    
    def crawl(url: str, depth: int) -> None:
        if depth > max_depth or len(discovered_urls) >= max_pages:
            return
        
        try:
            response = httpx.get(url, timeout=8.0, follow_redirects=True)
            if response.status_code >= 400:
                return
        except httpx.HTTPError:
            return
        
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.find_all("a", href=True):
                href = tag["href"]
                absolute = urljoin(url, href)
                
                if absolute in visited or len(discovered_urls) >= max_pages:
                    continue
                
                parsed = urlparse(absolute)
                if get_base_url(absolute) != base_domain:
                    continue
                
                # Remove fragment
                clean_url = absolute.split("#")[0]
                if clean_url not in visited:
                    visited.add(clean_url)
                    discovered_urls.append(clean_url)
                    crawl(clean_url, depth + 1)
        except Exception:
            pass
    
    # Start crawling from base URL
    crawl(base_url, 0)
    return discovered_urls[:max_pages]


def check_broken_links(urls: list[str], timeout: float = 5.0) -> dict[str, int]:
    """Check which URLs return HTTP errors."""
    broken: dict[str, int] = {}
    for url in urls:
        try:
            response = httpx.head(url, timeout=timeout, follow_redirects=True)
            if response.status_code >= 400:
                broken[url] = response.status_code
        except httpx.HTTPError:
            broken[url] = 0  # Connection failed
    return broken
