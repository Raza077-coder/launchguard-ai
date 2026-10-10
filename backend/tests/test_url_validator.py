from __future__ import annotations

import pytest

from app.scanner.url_validator import validate_target_url, validate_redirect_url, is_private_ip


def test_is_private_ip_blocks_loopback() -> None:
    assert is_private_ip("127.0.0.1") is True
    assert is_private_ip("::1") is True


def test_is_private_ip_blocks_private_ranges() -> None:
    assert is_private_ip("192.168.1.1") is True
    assert is_private_ip("10.0.0.1") is True
    assert is_private_ip("172.16.0.1") is True


def test_is_private_ip_allows_public() -> None:
    assert is_private_ip("8.8.8.8") is False
    assert is_private_ip("1.1.1.1") is False


def test_validate_target_url_blocks_localhost() -> None:
    with pytest.raises(ValueError, match="prohibited"):
        validate_target_url("http://localhost:8000")


def test_validate_target_url_blocks_loopback() -> None:
    with pytest.raises(ValueError, match="prohibited"):
        validate_target_url("http://127.0.0.1")


def test_validate_target_url_requires_http() -> None:
    with pytest.raises(ValueError, match="HTTP"):
        validate_target_url("file:///etc/passwd")


def test_validate_redirect_url_blocks_private_redirect() -> None:
    assert validate_redirect_url("https://example.com", "http://127.0.0.1") is False
    assert validate_redirect_url("https://example.com", "http://192.168.1.1") is False


def test_validate_redirect_url_allows_public() -> None:
    assert validate_redirect_url("https://example.com", "https://example.com/path") is True
