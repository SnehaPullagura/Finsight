# ClientFlow CRM — REST API Documentation

## Base URL
`/api/v1`

## Authentication
Bearer JWT Token passed in `Authorization: Bearer <token>` header, accompanied by `X-Tenant-ID: <tenant_id>`.

## Endpoint Matrix

| Domain | Route | Method | Description |
|---|---|---|---|
| **Health** | `/health` | GET | System health & subsystem diagnostics |
| **Auth** | `/auth/register` | POST | Register new tenant & administrator |
| | `/auth/login` | POST | Authenticate & retrieve JWT tokens |
| | `/auth/refresh` | POST | Refresh expired access token |
| | `/auth/me` | GET | Current user profile |
| | `/auth/mfa/setup` | POST | Generate TOTP secret and QR URI |
| | `/auth/mfa/verify` | POST | Validate TOTP 6-digit code |
| **Organizations** | `/organizations` | POST/GET | Organization management |
| | `/organizations/members` | GET/POST | Team membership |
| **Contacts** | `/contacts` | GET/POST | Contact CRUD |
| | `/contacts/{id}` | GET/PUT/DELETE | Single contact operations |
| | `/contacts/deduplicate` | GET | Fuzzy deduplication search |
| **Companies** | `/companies` | GET/POST | Company CRUD |
| | `/companies/{id}` | GET/PUT/DELETE | Company profile & hierarchies |
| **Leads** | `/leads` | GET/POST | Lead management |
| | `/leads/{id}/qualify` | POST | Trigger rule-based qualification |
| | `/leads/{id}/convert` | POST | 1-Click convert to Contact+Company+Deal |
| **Pipelines & Deals** | `/pipelines` | GET/POST | Pipeline & stage configuration |
| | `/deals` | GET/POST | Deal records |
| | `/deals/kanban` | GET | Board grouped by pipeline stages |
| | `/deals/{id}/stage` | POST | Transition deal stage with SLA validation |
| **Activities** | `/activities/timeline/{type}/{id}` | GET | Polymorphic event timeline |
| | `/activities` | POST | Log call, email, meeting, note |
| **Tasks & Calendar** | `/tasks` | GET/POST | Task queue |
| | `/calendar/events` | GET/POST | Meeting schedule |
| **Quote to Cash** | `/products` | GET/POST | Product catalog |
| | `/proposals` | GET/POST | Proposal generator |
| | `/proposals/{id}/accept` | POST | Proposal customer acceptance |
| | `/quotes` | GET/POST | Quotation management |
| | `/invoices` | GET/POST | Invoices & billing |
| | `/invoices/{id}/payments` | POST | Record invoice payment |
| **Customer Support** | `/support/tickets` | GET/POST | Support tickets |
| | `/support/tickets/{id}/resolve` | POST | Ticket resolution |
| **Customer Success** | `/customer-success/plans` | GET/POST | Success plans & health tracking |
| | `/customer-success/plans/{id}/recalculate-health` | POST | Trigger health score formula |
| **Marketing & Automations** | `/campaigns` | GET/POST | Campaign broadcasts |
| | `/automations` | GET/POST | Workflow rules |
| **Search & Analytics** | `/search?q=...` | GET | Global search engine across CRM |
| | `/analytics/dashboard` | GET | Real-time executive KPIs & funnel |
| **AI Assistant** | `/ai/summarize/lead/{id}` | POST | AI lead synthesis & fit score |
| | `/ai/analyze/deal/{id}` | POST | Deal risk analysis & win probability |
| | `/ai/draft/email` | POST | Contextual email generator |
| | `/ai/query` | POST | Natural language query translator |
