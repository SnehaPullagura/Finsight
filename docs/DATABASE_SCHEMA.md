# ClientFlow CRM — Database Schema Reference

## 1. Overview
ClientFlow utilizes PostgreSQL 16 with UUID primary keys (RFC 4122 v4) across all tables, ensuring distributed generation and zero sequential enumeration vulnerability.

## 2. Core Entities & Relationship Graph

### Identity & Access
- `users`: Core user accounts (Argon2id passwords, TOTP MFA, roles).
- `roles` & `permissions`: Granular RBAC definitions with junction table mappings.
- `user_sessions`: Active JWT sessions with IP and user-agent tracing.

### Tenancy & Organizations
- `organizations`: Root tenant entity with plan tiers and custom settings.
- `organization_members`: User-organization membership with owner flags.
- `teams` & `team_members`: Organizational sub-units and team hierarchies.

### CRM Core
- `contacts`: Individual person profiles with lifecycle stages and custom fields.
- `companies`: Corporate organizations with annual revenue, industry, employee scale.
- `leads`: Inbound/outbound prospects with dynamic scores and qualification grades (A-F).
- `lead_scoring_rules`: Multi-criteria heuristic rules.

### Sales & Revenue
- `pipelines` & `pipeline_stages`: Configurable sales pipelines with stage probabilities and SLAs.
- `deals`: Revenue opportunities moving across pipeline stages.
- `products`: Catalog items, service offerings, SKU tracking.
- `proposals` & `proposal_line_items`: Formal customer proposals with acceptance tracking.
- `quotes` & `quote_line_items`: Price quotations with revision control.
- `invoices` & `invoice_payments`: Invoicing engine with payment reconciliation.

### Customer Operations
- `activities`: Polymorphic timeline events across any entity type.
- `tasks`: Action queues with recurring scheduling.
- `calendar_events`: Meeting coordination and attendee status.
- `support_tickets`: SLA-governed customer support tickets.
- `customer_success_plans` & `onboarding_milestones`: Health scoring engine.
- `communication_messages` & `communication_templates`: Multi-channel dispatch.
- `documents` & `document_versions`: File vault with SHA-256 integrity.

### Growth & Engine
- `campaigns` & `campaign_segments`: Targeted marketing broadcasts.
- `automation_workflows`: Trigger-condition-action workflow automation.
- `custom_field_definitions`: Dynamic entity field schema extensibility.
- `audit_logs`: Centralized immutable compliance audit ledger.
