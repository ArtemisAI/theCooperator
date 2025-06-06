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
1. Add `Task` model with status, priority and due date fields.
   Create migration scripts and populate enumerations.
2. CRUD API with business rules for assignment limits and permission checks.
3. Celery task for due‑date email reminders and a background scheduler
   triggered via `beat`.
4. Kanban board UI with drag‑and‑drop using a library such as
   `react-beautiful-dnd`.
5. End‑to‑end tests for API logic, Celery worker and React components.
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

---
By advancing through these phases sequentially and verifying each checkpoint, we ensure a stable foundation before tackling more complex features. This approach keeps the scope focused and allows visible progress after every milestone.
