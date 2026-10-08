from __future__ import annotations

SLA_TARGET_HOURS = {
    "P1": 4,
    "P2": 8,
    "P3": 24,
    "P4": 48,
}


def get_sla_target(priority: str) -> int:
    return SLA_TARGET_HOURS.get(priority, 24)
