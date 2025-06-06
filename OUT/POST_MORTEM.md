# Post-Mortem Document

## Incident Overview

**Incident Date:** [Date of Incident]
**Time of Incident:** [Time of Incident]
**Duration of Incident:** [Duration]
**Severity:** [Critical/High/Medium/Low]
**Affected Services:** [List of affected services/components]

## Summary

[A brief summary of the incident, its impact, and the resolution.]

### Project Overview

This section provides a general overview of the "theCooperator" project, extracted from project documentation. It's intended to give context rather than describe a specific incident.

#### Business Logic

"theCooperator" aims to provide small & medium-sized housing co-operatives with modern, data-driven tooling typically available only to large commercial property managers. The platform's vision is to be a single source of truth for members, units, and duties, enabling transparent task and responsibility tracking, democratic decision-making through secure online voting, visualization of participation and community health via scorecards, and real-time notifications with self-service dashboards for residents.

Core functionalities for the MVP include:
1.  Member & Unit Management (CRUD, unit ↔ member mapping).
2.  Task Tracking (Kanban flow, due-dates & reminders).
3.  Voting & Polling (proposals, ballots, quorum, live results).
4.  Scorecards & Analytics (participation metrics & co-op KPIs).
5.  Notifications (e-mail / in-app alerts, webhook outbox).
6.  Access Control (JWT auth, resident / admin / observer roles).

#### Technical Details

The project follows a monorepo structure and utilizes the following technology stack:
*   **Database:** PostgreSQL (≥14), Dockerised, with migrations via Alembic.
*   **Backend API:** Python 3.11 + FastAPI, using Pydantic v2 for data models and asynchronous I/O.
*   **Background Jobs:** Celery + Redis for tasks like notifications and score recomputation.
*   **Optional Server-side Pages:** Flask blueprints (to be used minimally).
*   **Scripting / Tooling:** Node.js 20 LTS for the front-end tool-chain and miscellaneous generators.
*   **Front-end SPA:** React 18 + TypeScript + Vite, with Material-UI (MUI) component library.
*   **DevOps:** Docker Compose for local development, GitHub Actions for CI (CI/CD to staging with Kubernetes is optional).

The backend is organized into modules for core functionalities (settings, logging, security), database interactions (SQLAlchemy), ORM models, Pydantic schemas (DTOs), CRUD operations, business logic services, API endpoints (FastAPI routers), and Celery jobs.
The frontend includes API hooks, components, pages, context management, and utility functions.
Infrastructure includes Docker Compose configurations and Dockerfiles.
The `docs/architecture.md` is currently a draft and refers to the README for a high-level overview.

#### Issues Encountered (Outstanding Tasks & Challenges)

Based on `DEVELOPMENT_ROADMAP.md` and `TODO.md`, several items are pending or represent challenges:

**Backend:**
*   Structured logging (structlog + UVicorn access logs) needs full implementation.
*   Global error-handling and standardized error responses design is pending.
*   Defining ORM `relationship()` attributes for bidirectional associations.
*   Writing initial Alembic revision for schema migrations.
*   Implementing placeholder API endpoints for votes and metrics (currently return 501).
*   Evaluating removal or integration of the in-memory `/api/v1/todo` example.
*   Implementing business rules for task assignment limits and quorum calculation in `task_service.py` and `vote_service.py`.
*   Implementing Celery worker discovery and integrating business logic for `send_notification_email` and `recompute_scores`.
*   Implementing tests for task, vote, and metrics endpoints (target ≥80% coverage).
*   Setting up a GitHub Actions CI pipeline for lint, test, and build.

**Frontend:**
*   Configuring ESLint + Prettier and integrating with pre-commit hooks.
*   Implementing CRUD hooks for units, tasks, votes, metrics and integrating React Query.
*   Configuring an OpenAPI codegen pipeline for type-safe hook generation.
*   Implementing data fetching and widgets for the Dashboard page.
*   Implementing list & form for unit management in `Units.tsx`.
*   Implementing drag-and-drop and API integration for the Kanban view in `Tasks.tsx`.
*   Implementing proposals list, voting form, and results in `Votes.tsx`.
*   Implementing charts and scorecard displays in `Scorecards.tsx`.
*   Implementing MUI and charting library for stubbed components (`DataTable`, `ConfirmDialog`, `KanbanBoard`, `VoteChart`).
*   Integrating authentication flows and protected routes using `AuthContext`.
*   Evaluating advanced state needs.

**Infrastructure:**
*   Updating `docker-compose.yml` to add Redis and Celery worker services and container health-checks.
*   Creating `.env.example` with required environment variables.
*   Creating `.github/workflows/ci.yml` for CI.
*   Considering CD to staging (DigitalOcean/Kubernetes).

**Documentation:**
*   Fleshing out `docs/architecture.md` with C4 component, container, and deployment diagrams.
*   Creating a sequence diagram for the voting flow.
*   Auto-generating an ERD from SQLAlchemy metadata.
*   Updating `README.md` quick-start instructions.

#### Changes Attempted (Rationale for Tech Choices)

The `DEVELOPMENT_ROADMAP.md` provides rationale for some technology choices:
*   The tech stack (PostgreSQL, Python, Pydantic, Node.js, Flask/Django, TypeScript) follows preferences from the product owner.
*   FastAPI was chosen for the backend API.
*   The core UI is a client-side SPA (React). Flask is reserved for small, server-side admin pages or specific exports, as Django was deemed too heavy and would introduce an overlapping ORM.

No major pivots or refactoring efforts are explicitly detailed as "changes attempted" in the provided documents, but the roadmap implies an iterative development process.

#### Objectives

The primary objective is the first public release (v0.1.0) of *theCooperator*.
Key objectives for the project include:
*   Providing a single source of truth for members, units, and duties.
*   Enabling transparent task & responsibility tracking.
*   Facilitating democratic decision-making through secure online voting.
*   Visualizing participation & community health through scorecards.
*   Delivering real-time notifications and self-service dashboards.
*   Achieving 80% test coverage.
*   Setting up CI/CD pipelines.

#### Roadmap

The project is divided into several phases:

*   **Phase 0:** Project scaffolding, CI, Docker Compose, pre-commit, health-check endpoint (🟢 completed).
*   **Phase 1:** Member + Unit CRUD (API & UI); baseline auth (JWT) (🟢 completed).
*   **Phase 2:** Task / Responsibility module (Kanban), e-mail reminders (🟡 in progress). This is the current focus.
*   **Phase 3:** Voting / Polling engine, live result feed (WebSockets) (🔴 not started).
*   **Phase 4:** Scorecards & KPI dashboards (🔴 not started).
*   **Phase 5:** Hardening, docs, 80 % test coverage, CI/CD to staging (🟡 in progress).

Details for each phase and outstanding tasks are enumerated in `DEVELOPMENT_ROADMAP.md`.

## Timeline of Events

[A detailed chronological account of the events leading up to the incident, during the incident, and during the recovery process. Include timestamps for each event.]

**Example:**
*   **YYYY-MM-DD HH:MM UTC:** [Event Description]
*   **YYYY-MM-DD HH:MM UTC:** [Event Description]

## Root Cause Analysis

[A detailed analysis of the root cause(s) of the incident. This section should explain not just what happened, but why it happened.]

## Impact Analysis

[A description of the impact of the incident on users, services, and the business.]

**User Impact:**
[Details of how users were affected]

**Service Impact:**
[Details of how services/components were affected]

**Business Impact:**
[Details of the impact on business operations, if any]

## Resolution and Recovery

[A description of the steps taken to resolve the incident and restore service.]

**Resolution Steps:**
[List of actions taken to fix the issue]

**Recovery Process:**
[Description of how services were restored and verified]

## Lessons Learned

[What went well, what didn’t go well, and what could be improved.]

**What Went Well:**
*   [Point 1]
*   [Point 2]

**What Didn’t Go Well:**
*   [Point 1]
*   [Point 2]

**Where We Got Lucky:**
*   [Point 1]
*   [Point 2]

## Action Items

[A list of actionable items to prevent similar incidents in the future or to improve the incident response process. Each item should have an owner and a due date.]

| Action Item                                  | Owner         | Due Date   | Status      |
| -------------------------------------------- | ------------- | ---------- | ----------- |
| [Description of action item]                 | [Team/Person] | YYYY-MM-DD | [To Do/In Progress/Done] |
| [Description of action item]                 | [Team/Person] | YYYY-MM-DD | [To Do/In Progress/Done] |

## Supporting Data/Links

[Links to relevant dashboards, logs, monitoring tools, or other documentation.]

*   [Link to relevant data]
*   [Link to relevant data]

## Participants

[List of individuals involved in the incident response and post-mortem analysis.]

*   [Name/Team]
*   [Name/Team]

## File Uploading System: Details and Issues

As of the last review of the project documentation (`DEVELOPMENT_ROADMAP.md`, `TODO.md`, `README.md`) and codebase inspection (core backend and frontend files, model definitions), no specific implementation, detailed plan, or explicit mention of a file uploading system (e.g., for attachments to tasks, proposals, or user profiles) was found.

**Overview of File Uploading Technology/Approach:**
*   Not defined or implemented. There are no dedicated services, API endpoints, or model fields that suggest a file uploading mechanism is in place or actively being developed.

**Identified Issues, Challenges, or Reasons for Problematic Nature:**
*   **Absence of Feature:** The primary "issue" is the apparent lack of file uploading functionality. If the ability to attach files (e.g., documents to proposals, images to tasks, user avatars) is a requirement for "theCooperator" platform, then this functionality is currently missing.
*   **No Documented Discussion:** The reviewed planning documents do not contain any discussion, requirements, or identified challenges related to implementing file storage, management, or uploading. This means that if such a system is needed, its design and potential complexities (e.g., storage solution, security considerations, file type restrictions, size limits) have not yet been formally addressed in these key documents.
*   **Potential Future Need:** Given the nature of a cooperative management platform, it's plausible that features requiring file uploads (e.g., sharing meeting minutes, proposal documents, invoices, or images related to maintenance tasks) could be valuable. The lack of current implementation or planning for this could be a future development hurdle or a gap in meeting user needs.

If a "problematic file uploading system" was reported or perceived, it likely refers to the complete absence of this capability rather than issues within an existing system. Further clarification on specific requirements or past discussions not captured in the central documents would be needed to elaborate more on this topic.
