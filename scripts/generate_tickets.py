from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 20261008
ROWS = 1000
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "tickets.csv"

random.seed(SEED)

TEMPLATES = [
    ("Access Management", "Password Reset", "My password expired and I cannot sign in", "Identity & Access", "KB-ACCESS-004", "password reset"),
    ("Access Management", "Permission", "Finance users cannot access the shared folder after a permissions change", "Identity & Access", "KB-ACCESS-004", "privileged access change"),
    ("Access Management", "Account Lockout", "My account is locked after several failed attempts", "Identity & Access", "KB-ACCESS-004", "account unlock"),
    ("Access Management", "MFA", "MFA code is not being accepted", "Identity & Access", "KB-ACCESS-004", "ticket assignment"),
    ("Network", "Wi-Fi", "Wi-Fi disconnects repeatedly in the office", "Network Operations", "KB-NET-002", "ticket assignment"),
    ("Network", "VPN", "VPN connection fails from a remote location", "Network Operations", "KB-NET-002", "ticket assignment"),
    ("Network", "DNS", "The business application cannot resolve its service name", "Network Operations", "KB-NET-002", "ticket assignment"),
    ("Hardware", "Laptop", "Laptop will not start after reboot", "End User Computing", "KB-HW-001", "ticket assignment"),
    ("Hardware", "Printer", "Department printer is offline", "End User Computing", "KB-HW-001", "ticket assignment"),
    ("Hardware", "Peripheral", "Monitor and keyboard intermittently disconnect", "End User Computing", "KB-HW-001", "ticket assignment"),
    ("Software", "Application Error", "ERP application shows an unexpected error", "Application Support", "KB-SW-003", "ticket assignment"),
    ("Software", "Installation", "User needs an approved software package installed", "Application Support", "KB-SW-003", "ticket assignment"),
    ("Email & Collaboration", "Mailbox", "Outlook is not receiving new messages", "Collaboration Services", "KB-COLLAB-001", "ticket assignment"),
    ("Email & Collaboration", "Teams", "Teams calls have no audio", "Collaboration Services", "KB-COLLAB-001", "ticket assignment"),
    ("Email & Collaboration", "Calendar", "A calendar meeting disappeared", "Collaboration Services", "KB-COLLAB-001", "ticket assignment"),
    ("Server & Infrastructure", "Server Availability", "Application server is unavailable", "Infrastructure Operations", "KB-INFRA-006", "production change"),
    ("Server & Infrastructure", "Backup", "Nightly backup job failed", "Infrastructure Operations", "KB-INFRA-006", "ticket assignment"),
    ("Server & Infrastructure", "Storage", "File server storage is nearly full", "Infrastructure Operations", "KB-INFRA-006", "ticket assignment"),
    ("Security", "Phishing", "User received a suspicious email requesting credentials", "Cybersecurity", "KB-SEC-005", "security control change"),
    ("Security", "Endpoint Protection", "Endpoint protection reports malware activity", "Cybersecurity", "KB-SEC-005", "security control change"),
]

IMPACT_WEIGHT = [("High", 20), ("Medium", 50), ("Low", 30)]
URGENCY_WEIGHT = [("High", 20), ("Medium", 50), ("Low", 30)]
PRIORITY = {
    ("High", "High"): "P1",
    ("High", "Medium"): "P2",
    ("High", "Low"): "P3",
    ("Medium", "High"): "P2",
    ("Medium", "Medium"): "P3",
    ("Medium", "Low"): "P4",
    ("Low", "High"): "P3",
    ("Low", "Medium"): "P4",
    ("Low", "Low"): "P4",
}
SLA = {"P1": 4, "P2": 8, "P3": 24, "P4": 48}

DEPARTMENTS = ["Finance", "HR", "Procurement", "Engineering", "Operations", "Administration", "Project Management", "IT"]
LOCATIONS = ["Head Office", "Site A", "Site B", "Remote", "Regional Office"]
SERVICES = ["Active Directory", "Corporate Network", "ERP", "Email & Collaboration", "File Services", "Service Desk", "Virtual Infrastructure", "Endpoint Management"]
STATUSES = ["Closed", "Resolved", "In Progress", "Open"]

rows = []
start = datetime(2026, 1, 1, 8, 0)

for i in range(1, ROWS + 1):
    category, subcategory, description, assignment, knowledge, action = random.choice(TEMPLATES)
    impact = random.choices([x[0] for x in IMPACT_WEIGHT], [x[1] for x in IMPACT_WEIGHT])[0]
    urgency = random.choices([x[0] for x in URGENCY_WEIGHT], [x[1] for x in URGENCY_WEIGHT])[0]
    priority = PRIORITY[(impact, urgency)]
    status = random.choices(STATUSES, [52, 28, 13, 7])[0]
    created = start + timedelta(
        days=random.randint(0, 280),
        hours=random.randint(0, 10),
        minutes=random.randint(0, 59),
    )

    base = {"P1": 3.5, "P2": 6.0, "P3": 14.0, "P4": 22.0}[priority]
    resolution = round(max(0.5, random.gauss(base, base * 0.35)), 1)
    if status in {"Open", "In Progress"}:
        resolution = round(random.uniform(0.5, 12), 1)

    category_confidence = round(random.uniform(0.80, 0.98), 2)
    priority_confidence = round(random.uniform(0.82, 0.97), 2)

    high_risk = action in {"privileged access change", "production change", "security control change"}
    human_approval = "Yes" if high_risk or priority == "P1" or min(category_confidence, priority_confidence) < 0.80 else "No"
    automation_eligible = "Yes" if human_approval == "No" and action in {
        "password reset", "account unlock", "ticket assignment",
        "knowledge article suggestion", "standard notification"
    } else "No"

    rows.append({
        "Ticket ID": f"INC-{i:05d}",
        "Created Date": created.strftime("%Y-%m-%d"),
        "Created Time": created.strftime("%H:%M"),
        "Department": random.choice(DEPARTMENTS),
        "Location": random.choice(LOCATIONS),
        "Service": random.choice(SERVICES),
        "Category": category,
        "Subcategory": subcategory,
        "Description": description,
        "Impact": impact,
        "Urgency": urgency,
        "Policy Priority": priority,
        "Assignment Group": assignment,
        "SLA Target Hours": SLA[priority],
        "Resolution Hours": resolution,
        "Status": status,
        "AI Category": category,
        "AI Category Confidence": category_confidence,
        "AI Priority": priority,
        "AI Priority Confidence": priority_confidence,
        "Knowledge Article ID": knowledge,
        "Human Approval Required": human_approval,
        "Automation Eligible": automation_eligible,
        "Automation Action": action,
        "Automation Result": "Approved - simulated" if automation_eligible == "Yes" else "Human review required",
        "Reopened": "Yes" if random.random() < 0.07 else "No",
        "User Satisfaction": random.choice([3, 4, 4, 4, 5]),
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {ROWS} synthetic tickets at {OUTPUT}")
