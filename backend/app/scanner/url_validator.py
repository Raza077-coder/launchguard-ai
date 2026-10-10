from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import httpx

PROHIBITED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal", "169.254.169.254"}
ALLOWED_SCHEMES = {"http", "https"}


def is_private_ip(ip: str) -> bool:
    """Check if an IP address is private, reserved, or unsafe to scan."""
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


def resolve_hostname(hostname: str) -> str:
    """Resolve hostname to IP and validate it is public."""
    try:
        ip = socket.gethostbyname(hostname)
        if is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")
        return ip
    except socket.gaierror as e:
        raise ValueError(f"Failed to resolve hostname {hostname}: {e}") from e


def validate_target_url(url: str, timeout: float = 8.0) -> dict[str, object]:
    """Validate that a URL is safe to scan and reachable."""
    parsed = urlparse(url)
    
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")
    if not parsed.netloc:
        raise ValueError("URL must include a hostname.")

    host = parsed.hostname or ""
    if host.lower() in PROHIBITED_HOSTS:
        raise ValueError("Local or prohibited destinations are not allowed.")
    
    # Resolve hostname and check IP
    try:
        resolve_hostname(host)
    except ValueError as e:
        raise ValueError(f"Target hostname validation failed: {e}") from e

    # Attempt connection to verify URL is reachable
    try:
        response = httpx.get(url, timeout=timeout, follow_redirects=False)
    except httpx.HTTPError as exc:
        raise ValueError(f"Target validation failed: {exc}") from exc

    # If we get a redirect, validate the redirect target
    if response.is_redirect and "location" in response.headers:
        redirect_url = response.headers["location"]
        if not validate_redirect_url(url, redirect_url):
            raise ValueError(f"Redirect to {redirect_url} is not allowed.")

    return {"url": url, "host": host, "status_code": response.status_code}


def validate_redirect_url(original_url: str, final_url: str | None = None) -> bool:
    """Validate that a redirect is safe to follow."""
    parsed = urlparse(original_url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False
    host = parsed.hostname or ""
    if host.lower() in PROHIBITED_HOSTS:
        return False
    if final_url:
        final_parsed = urlparse(final_url)
        final_host = final_parsed.hostname or ""
        if final_host.lower() in PROHIBITED_HOSTS:
            return False
        if final_parsed.scheme.lower() not in ALLOWED_SCHEMES:
            return False
    return True
