from __future__ import annotations


def calculate_health_score(findings: list[dict[str, object]]) -> int:
    score = 100
    weights = {
        "critical": 35,
        "high": 20,
        "medium": 10,
        "low": 5,
    }
    for finding in findings:
        severity = str(finding.get("severity", "low")).lower()
        score -= weights.get(severity, 5)
    return max(0, score)
