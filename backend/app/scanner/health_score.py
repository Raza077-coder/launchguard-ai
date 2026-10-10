from __future__ import annotations


def calculate_health_score(findings: list[dict[str, object]]) -> int:
    """Calculate LaunchGuard Health Score based on findings.
    
    Start at 100 and subtract weighted penalties:
    - Critical: 35 points
    - High: 20 points
    - Medium: 10 points
    - Low: 5 points
    
    Minimum: 0, Maximum: 100
    """
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
