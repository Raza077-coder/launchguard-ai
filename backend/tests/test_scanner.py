from __future__ import annotations

from app.scanner.finding_normalizer import normalize_findings
from app.scanner.health_score import calculate_health_score


def test_finding_deduplication() -> None:
    findings = [
        {"category": "seo", "title": "Missing title", "severity": "medium"},
        {"category": "seo", "title": "Missing title", "severity": "medium"},
    ]
    normalized = normalize_findings(findings)
    assert len(normalized) == 1
    assert normalized[0]["duplicate_count"] == 2


def test_health_score_calculation() -> None:
    findings = [
        {"severity": "high"},
        {"severity": "medium"},
    ]
    score = calculate_health_score(findings)
    assert score == 70  # 100 - 20 - 10


def test_health_score_minimum_zero() -> None:
    findings = [
        {"severity": "critical"},
        {"severity": "critical"},
        {"severity": "critical"},
        {"severity": "high"},
    ]
    score = calculate_health_score(findings)
    assert score >= 0


def test_health_score_maximum_hundred() -> None:
    findings: list[dict[str, object]] = []
    score = calculate_health_score(findings)
    assert score == 100
