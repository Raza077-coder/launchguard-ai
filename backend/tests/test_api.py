from __future__ import annotations

import pytest

from app.scanner.url_validator import validate_target_url, validate_redirect_url


def test_validate_target_url_allows_public_http_site() -> None:
    result = validate_target_url("https://example.com")
    assert result["host"] == "example.com"


def test_validate_target_url_blocks_localhost() -> None:
    with pytest.raises(ValueError):
        validate_target_url("http://localhost:8000")


def test_validate_redirect_url_blocks_private_redirect() -> None:
    assert validate_redirect_url("https://example.com", "http://127.0.0.1") is False
