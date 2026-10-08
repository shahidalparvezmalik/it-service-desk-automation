from __future__ import annotations

from dataclasses import asdict

from classifier import classify_ticket
from priority_engine import recommend_priority
from sla_engine import get_sla_target


SAFE_ACTIONS = {
    "password reset",
    "account unlock",
    "ticket assignment",
    "knowledge article suggestion",
    "standard notification",
}

HIGH_RISK_ACTIONS = {
    "privileged access change",
    "production change",
    "security control change",
    "destructive action",
}


def determine_automation(
    priority: str,
    action: str,
    classification_confidence: float,
    priority_confidence: float,
) -> tuple[bool, bool, str]:
    action_normalized = action.strip().lower()

    if action_normalized in HIGH_RISK_ACTIONS:
        return False, True, "High-risk action requires explicit human authorization."

    if priority == "P1":
        return False, True, "P1 incidents require human control and escalation."

    if classification_confidence < 0.75 or priority_confidence < 0.80:
        return False, True, "Recommendation confidence is below the automation threshold."

    if action_normalized in SAFE_ACTIONS:
        return True, False, "Action is on the approved low-risk automation allow-list."

    return False, True, "Action is not on the approved automation allow-list."


def analyze_ticket(
    description: str,
    impact: str,
    urgency: str,
    action: str = "ticket assignment",
) -> dict:
    classification = classify_ticket(description)
    priority = recommend_priority(impact, urgency)
    sla_target = get_sla_target(priority.priority)

    automation_eligible, human_approval_required, governance_reason = determine_automation(
        priority.priority,
        action,
        classification.confidence,
        priority.confidence,
    )

    return {
        **asdict(classification),
        "priority": priority.priority,
        "priority_confidence": priority.confidence,
        "priority_rationale": priority.rationale,
        "sla_target_hours": sla_target,
        "human_approval_required": human_approval_required,
        "automation_eligible": automation_eligible,
        "automation_action": action,
        "governance_reason": governance_reason,
    }
