from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

import httpx

PROHIBITED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal", "169.254.169.254"}
ALLOWED_SCHEMES = {"http", "https"}


def is_private_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
            or addr.is_unspecified
        )
    except ValueError:
        return True


def validate_target_url(url: str) -> dict[str, object]:
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")
    if not parsed.netloc:
        raise ValueError("URL must include a hostname.")

    host = parsed.hostname or ""
    if host.lower() in PROHIBITED_HOSTS:
        raise ValueError("Local or prohibited destinations are not allowed.")

    try:
        resolved = httpx.get(url, timeout=8.0)
    except httpx.HTTPError as exc:
        raise ValueError(f"Target validation failed: {exc}") from exc

    if resolved.status_code >= 400:
        raise ValueError("Target URL responded with an HTTP error during validation.")

    return {"url": url, "host": host, "status_code": resolved.status_code}


def validate_redirect_url(url: str, final_url: str | None = None) -> bool:
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False
    host = parsed.hostname or ""
    if host.lower() in PROHIBITED_HOSTS:
        return False
    if final_url:
        final_parsed = urlparse(final_url)
        if final_parsed.hostname and final_parsed.hostname.lower() in PROHIBITED_HOSTS:
            return False
    return True
