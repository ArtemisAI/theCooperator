# Reboot Roadmap for theCooperator

This roadmap outlines an incremental approach to rebuild *theCooperator*. It reflects lessons from the initial project and the findings in `OUT/POST_MORTEM.md`.

## Lessons Learned
- The original plan attempted to tackle multiple complex modules at once. Many features (e.g. file uploads) were never implemented, leaving gaps in the product.
- There was limited automation and CI. Tests exist for a few endpoints but large areas remain untested.

To avoid repeating these issues we will progress in clearly defined phases with required tests before moving on.

## Phase 0 – Foundation
**Goal:** Working development environment with CI.

**Tasks**
1. Docker Compose services for Postgres, backend, Redis and a Celery worker.
   Include volumes for persistent DB data and a shared `.env` file.
2. FastAPI skeleton with `/health` endpoint, basic configuration object and a
   minimal Alembic setup.  Provide a pytest suite that spins up the app with an
   in‑memory SQLite database.
3. React/Vite scaffold with a placeholder page and Vitest setup.  Add a
   `make dev` helper script to run the front‑end and back‑end together.
4. Pre‑commit hooks (Black/Flake8 for Python, ESLint/Prettier for TS) and
   a `.editorconfig` file to enforce spacing rules.
5. GitHub Actions workflow running lint and tests for backend and frontend on
   every pull request.
6. Document all environment variables in `docs/environment.md`.

**Checkpoint**
- `docker compose up` starts all services.
- `pytest` and `npm test` pass in CI.

## Phase 1 – Members & Units
**Goal:** Basic member database and unit mapping.

**Tasks**
1. SQLAlchemy models `Member` and `Unit`; create Alembic migrations and seed
   some demo data for local development.
2. CRUD API endpoints with FastAPI and input validation using Pydantic models.
3. React pages for listing and editing members/units with basic form validation
   and optimistic UI updates.
4. Integration tests covering all endpoints and React forms.
5. Update the README with database initialisation instructions and diagrams
   showing the data model.

**Checkpoint**
- API returns member and unit data.
- Frontend pages perform create/read/update/delete.
- Backend test coverage ≥80 % for these modules.

## Phase 2 – Task Management
**Goal:** Track tasks and responsibilities.

**Tasks**
1. Add `Task` model with lane_id and sort_index fields plus status, priority and due date.
   Create Alembic migration and seed default lanes.
2. CRUD API with business rules for assignment limits and permission checks.
   Expose `/lanes` endpoints and `/tasks/reorder` with WebSocket broadcast.
3. Celery task for due‑date email reminders and a background scheduler
   triggered via `beat`.
4. Kanban board UI built with **@dnd-kit** and optimistic updates via React Query.
5. End‑to‑end tests (vitest, Playwright) and contract fuzzing with schemathesis.
6. Extend pre‑commit config with mypy type checking.

**Checkpoint**
- Tasks can be created, updated, moved between states.
- Worker sends a test reminder email.
- All tests pass.

## Phase 3 – Voting & Polling
**Goal:** Allow proposals and secure voting.

**Tasks**
1. Models `Proposal` and `Vote` with relationships plus constraints for
   unique ballots and quorum tracking.
2. API endpoints to create proposals, cast votes, and fetch results. Include
   rate limiting and JWT based permissions.
3. WebSocket or Server‑Sent Events for live result updates and a fallback
   long‑polling route for older browsers.
4. React UI for proposals and ballot casting with validation and error states.
5. Tests for vote logic, permission checks and real‑time channels using
   WebSocket clients.
6. Update architecture diagrams to document the real‑time flow.

**Checkpoint**
- Users can create a proposal and vote on it via the UI.
- Real‑time results update correctly.
- Backend and frontend tests cover the flow.

## Phase 4 – Scorecards & Analytics
**Goal:** Visualise participation metrics.

**Tasks**
1. Metric/Score models and periodic computation jobs triggered via Celery.
   Store per‑member historical data for longitudinal charts.
2. API endpoints for dashboard metrics and personal scorecards with caching
   using Redis.
3. Charts on the React dashboard built with Recharts and friendly tooltips.
4. Accessibility and responsiveness audit for the new pages.
5. Tests verifying metric calculations, caching behaviour and UI rendering.
6. Update documentation with example screenshots of the dashboard.

**Checkpoint**
- Dashboard displays aggregated stats.
- Unit tests verify score computations.

## Phase 5 – File Uploads & Documents (Optional)
From the post‑mortem we learned that file uploads were entirely absent【F:OUT/POST_MORTEM.md†L198-L208】. If needed, implement them in this dedicated phase.

**Tasks**
1. Decide on storage backend (local filesystem or S3 compatible) and update
   infrastructure scripts accordingly.
2. Endpoints for uploading attachments to tasks or proposals with checksum
   validation and background virus scanning.
3. React components for file inputs and preview with drag‑and‑drop support.
4. Security checks (size limits, allowed types) and rate limiting.
5. Tests for upload API and frontend interactions with mock storage adapters.
6. Update privacy policy and documentation if user data is stored externally.

**Checkpoint**
- Files can be attached to a task and retrieved.

## Phase 6 – Notifications & Integrations
**Goal:** Keep members informed and integrate external services.

**Tasks**
1. Expand Celery tasks to handle notifications for tasks and votes, including
   templated emails and digest summaries.
2. Outgoing webhook endpoints for automation tools such as n8n with signed
   payloads.
3. Optional integration tests with n8n workflows running in Docker.
4. Provide a mock notification channel for local development and tests.
5. Document how to connect the platform to common communication tools
   (e.g. Slack or Mattermost).

**Checkpoint**
- Notification tasks trigger from the app and tests confirm delivery via a mocked channel.

## Phase 7 – Hardening & Deployment
**Goal:** Production readiness.

**Tasks**
1. Structured logging (`structlog`) and global error handling including
   custom exception types.
2. Container health checks and `.env.example` for required variables plus a
   helper script for generating development secrets.
3. GitHub Actions deploying Docker images to staging on every main branch push
   and running security scans with `trivy`.
4. Documentation updates: C4 diagrams, ERD, and a CHANGELOG.  Create release
   notes for each tagged version.
5. Ensure overall test coverage ≥80 % with coverage reports uploaded to CI.
6. Final user acceptance checklist and manual test plan before tagging v1.0.

**Checkpoint**
- CI pipeline builds, tests, and deploys automatically.
- Documentation complete and reviewed.

## Phase 8 – Beta Feedback & Polish
**Goal:** Release a minimal beta to select co-ops and gather feedback.

**Tasks**
1. Deploy a staging environment for early adopters with seed data.
2. Enable error tracking (e.g. Sentry) and usage analytics.
3. Collect feedback via in-app forms and track issues in GitHub.
4. Prioritise bug fixes and usability improvements.
5. Document onboarding steps and update README with known issues.

**Checkpoint**
- Beta testers actively use the system and submit feedback.
- Major blockers addressed before wider launch.

## Phase 9 – Multi-Co-op Tenancy
**Goal:** Host multiple cooperatives on the same platform.

**Tasks**
1. Add a `Coop` tenant model and reference it from all entities.
2. Update authentication and permissions to enforce tenant isolation.
3. Extend API and UI to switch between co-ops.
4. Migrate data and include fixtures for multi-coop demos.
5. Provide a tenant-aware admin dashboard.

**Checkpoint**
- Data from different co-ops remains isolated and accessible only to authorised members.

## Phase 10 – Maintenance & Asset Tracking
**Goal:** Manage building assets and scheduled maintenance.

**Tasks**
1. Introduce `Asset` and `MaintenanceEvent` models with optional attachments.
2. Calendar UI showing upcoming maintenance events.
3. Reminder emails sent via Celery tasks.
4. Reports summarising maintenance costs and history.
5. Update documentation with examples and screenshots.

**Checkpoint**
- Maintenance events appear on the dashboard and reminders work in tests.

## Phase 11 – Finance Integration
**Goal:** Provide basic accounting and payment capabilities.

**Tasks**
1. Implement invoice and expense models with CRUD APIs.
2. Integrate with a payment gateway for dues collection.
3. Export financial reports to CSV or PDF.
4. Add roles and permissions for treasurers.
5. Document security considerations around financial data.

**Checkpoint**
- Dues payments recorded successfully and financial exports available.

## Phase 12 – Extensions & Community
**Goal:** Encourage community contributions and third-party integrations.

**Tasks**
1. Publish stable REST API endpoints with versioning.
2. Define a plugin architecture and example extension repository.
3. Provide contributor guide, code of conduct and governance policy.
4. Automate dependency updates and set release cadence.
5. Showcase at least one community-created plugin.

**Checkpoint**
- First external extension installed and documentation updated.

---
By advancing through these phases sequentially and verifying each checkpoint, we ensure a stable foundation before tackling more complex features. This approach keeps the scope focused and allows visible progress after every milestone.
