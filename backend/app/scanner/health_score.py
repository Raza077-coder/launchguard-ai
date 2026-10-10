from __future__ import annotations

from collections import defaultdict


def normalize_findings(findings: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for finding in findings:
        key = f"{finding.get('category')}:{(finding.get('title') or '').lower()}"
        grouped[key].append(finding)

    normalized: list[dict[str, object]] = []
    for group in grouped.values():
        primary = group[0].copy()
        primary["duplicate_count"] = len(group)
        normalized.append(primary)
    return normalized
