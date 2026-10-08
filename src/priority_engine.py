from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityRecommendation:
    priority: str
    confidence: float
    rationale: str


PRIORITY_MATRIX = {
    ("High", "High"): ("P1", 0.95, "High business impact and high urgency"),
    ("High", "Medium"): ("P2", 0.90, "High business impact requires expedited response"),
    ("High", "Low"): ("P3", 0.84, "High impact but limited urgency"),
    ("Medium", "High"): ("P2", 0.90, "Moderate impact with high urgency"),
    ("Medium", "Medium"): ("P3", 0.88, "Moderate impact and urgency"),
    ("Medium", "Low"): ("P4", 0.84, "Moderate impact with low urgency"),
    ("Low", "High"): ("P3", 0.86, "Low impact but high urgency"),
    ("Low", "Medium"): ("P4", 0.86, "Low impact and moderate urgency"),
    ("Low", "Low"): ("P4", 0.90, "Low impact and low urgency"),
}


def recommend_priority(impact: str, urgency: str) -> PriorityRecommendation:
    result = PRIORITY_MATRIX.get((impact.title(), urgency.title()))
    if result is None:
        return PriorityRecommendation(
            priority="P3",
            confidence=0.50,
            rationale="Unknown impact/urgency combination; routed for human review.",
        )

    priority, confidence, rationale = result
    return PriorityRecommendation(priority, confidence, rationale)
