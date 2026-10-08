# Architecture

## Workflow

1. Receive ticket
2. Extract text and context
3. Recommend category
4. Recommend priority
5. Recommend SLA
6. Suggest assignment group
7. Suggest approved knowledge article
8. Apply policy and risk rules
9. Require human approval when necessary
10. Execute only eligible actions
11. Record result and audit information
12. Measure operational outcomes

## Separation of Responsibilities

### Intelligence layer
Produces recommendations and confidence scores.

### Control layer
Determines whether the recommendation can be applied.

### Execution layer
Runs an approved automation playbook.

### Verification layer
Confirms the result and updates the ITSM record.

This separation prevents a recommendation engine from becoming an ungoverned privileged automation mechanism.
