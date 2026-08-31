# ClientFlow CRM — Workflow Automation Engine

## 1. Trigger-Condition-Action Architecture
The Automation Engine allows organizations to define event-driven business rules:

```
Domain Event (e.g. `deal.stage_changed`, `lead.created`)
        │
        ▼
Trigger Matching Filter
        │
        ▼
Conditional Evaluation Engine (eq, gt, gte, lt, lte, contains)
        │
        ▼
Sequential Action Dispatch (Task Creation, Email Notification, Webhook, Status Update)
        │
        ▼
Execution Log & Audit Ledger
```

## 2. Supported Conditions & Operators
- `gt`, `gte`, `lt`, `lte`: Numeric evaluations (e.g., deal value > $50,000).
- `eq`: Exact string or numeric equality.
- `contains`: Substring matching on text attributes.
