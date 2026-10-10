from __future__ import annotations

from app.ai.provider import AIProvider


class OllamaProvider(AIProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url
        self.model = model

    def explain(self, context: str) -> str:
        return f"Deterministic explanation unavailable for '{context[:120]}'. The scan remains evidence-based and does not depend on AI output."
