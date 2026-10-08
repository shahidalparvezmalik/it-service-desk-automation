# Governance Model

## Risk Tiers

### Tier 1 — Low Risk
Examples:
- Ticket categorization
- Knowledge-article suggestion
- Assignment recommendation
- Draft response

These can normally be automated or auto-applied under approved policy.

### Tier 2 — Controlled
Examples:
- Password reset
- Account unlock
- Standard software request
- Routine non-production service action

Require policy checks and, where appropriate, human approval.

### Tier 3 — High Risk
Examples:
- Privileged access changes
- Production changes
- Security-control changes
- Destructive actions
- Business-critical service intervention

Require explicit human authorization and stronger audit controls.

## Guardrails

- Approved action allow-list
- Confidence threshold
- Role-based approval
- Audit logging
- Human override
- Rollback where practical
- Monitoring and alerting
- Periodic control review

## Core Principle

> **Automate the decision support before automating the decision itself.**

As confidence, controls, and operational evidence improve, selected low-risk actions may move toward higher levels of autonomy.
