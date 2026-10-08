from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Classification:
    category: str
    subcategory: str
    confidence: float
    assignment_group: str
    knowledge_article_id: str


RULES = {
    "Access Management": {
        "keywords": {
            "password": "Password Reset",
            "locked": "Account Lockout",
            "lockout": "Account Lockout",
            "permission": "Permission",
            "access": "Permission",
            "mfa": "MFA",
            "authentication": "MFA",
        },
        "assignment": "Identity & Access",
        "knowledge": "KB-ACCESS-004",
    },
    "Network": {
        "keywords": {
            "wifi": "Wi-Fi",
            "wi-fi": "Wi-Fi",
            "vpn": "VPN",
            "dns": "DNS",
            "network": "LAN",
            "switch": "LAN",
            "internet": "LAN",
        },
        "assignment": "Network Operations",
        "knowledge": "KB-NET-002",
    },
    "Hardware": {
        "keywords": {
            "laptop": "Laptop",
            "desktop": "Desktop",
            "printer": "Printer",
            "monitor": "Peripheral",
            "keyboard": "Peripheral",
        },
        "assignment": "End User Computing",
        "knowledge": "KB-HW-001",
    },
    "Software": {
        "keywords": {
            "application": "Application Error",
            "software": "Installation",
            "install": "Installation",
            "license": "Licensing",
            "configuration": "Configuration",
        },
        "assignment": "Application Support",
        "knowledge": "KB-SW-003",
    },
    "Email & Collaboration": {
        "keywords": {
            "email": "Mailbox",
            "mailbox": "Mailbox",
            "outlook": "Mailbox",
            "teams": "Teams",
            "calendar": "Calendar",
            "meeting": "Calendar",
        },
        "assignment": "Collaboration Services",
        "knowledge": "KB-COLLAB-001",
    },
    "Server & Infrastructure": {
        "keywords": {
            "server": "Server Availability",
            "backup": "Backup",
            "storage": "Storage",
            "virtual machine": "Virtual Machine",
            "vm": "Virtual Machine",
        },
        "assignment": "Infrastructure Operations",
        "knowledge": "KB-INFRA-006",
    },
    "Security": {
        "keywords": {
            "phishing": "Phishing",
            "suspicious": "Suspicious Activity",
            "malware": "Endpoint Protection",
            "antivirus": "Endpoint Protection",
            "security": "Policy",
        },
        "assignment": "Cybersecurity",
        "knowledge": "KB-SEC-005",
    },
}


def _normalize(text: str) -> str:
    text = text.lower().replace("_", " ")
    return re.sub(r"\s+", " ", text).strip()


def classify_ticket(text: str) -> Classification:
    normalized = _normalize(text)
    best = None

    for category, config in RULES.items():
        matches = []
        for keyword, subcategory in config["keywords"].items():
            if keyword in normalized:
                matches.append((keyword, subcategory))

        if matches:
            score = sum(max(1, len(keyword.split())) for keyword, _ in matches)
            candidate = (score, category, matches)
            if best is None or candidate[0] > best[0]:
                best = candidate

    if not best:
        return Classification(
            category="General Service Desk",
            subcategory="Unclassified",
            confidence=0.35,
            assignment_group="Service Desk",
            knowledge_article_id="KB-GEN-001",
        )

    score, category, matches = best
    confidence = min(0.98, 0.58 + (0.08 * min(score, 5)))
    subcategory = matches[0][1]
    config = RULES[category]

    return Classification(
        category=category,
        subcategory=subcategory,
        confidence=round(confidence, 2),
        assignment_group=config["assignment"],
        knowledge_article_id=config["knowledge"],
    )
