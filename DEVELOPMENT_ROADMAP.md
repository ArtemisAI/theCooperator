# theCooperator — Development Road-map & Work-breakdown

This living document enumerates **everything that is still outstanding** for the
first public release (v0.1.0) of *theCooperator*.  It complements – but does
not duplicate – the high-level introduction found in `README.md`.

Anyone picking up a ticket should be able to open this file and immediately
understand  
• **what still needs to be built**,  
• **which technology / module** we expect to use, and  
• **where the corresponding source files live** in the repository.

--------------------------------------------------------------------------------

## 1 Canonical Tech-stack (agreed)

| Layer            | Selected Technology | Notes |
|------------------|---------------------|-------|
| **Database**     | PostgreSQL ≥14      | Dockerised; migrations via Alembic |
| **Backend API**  | Python 3.11 + FastAPI | Pydantic v2 data-models; asynchronous I/O |
| **Background jobs** | Celery + Redis     | Notifications, score recomputation |
| **Optional server-side pages** | Flask blueprints (small utilities) | use **only** if React UI cannot cover the use-case |
| **Scripting / Tooling** | Node.js 20 LTS | Front-end tool-chain & misc. generators |
| **Front-end SPA** | React 18 + TypeScript + Vite | Material-UI (MUI) component library |

The choices above follow the preference list provided by the product owner
(PostgreSQL, Python, Pydantic, Node.js **where needed**, Flask/Django for
server-rendered pages, TypeScript).  

*Rationale*: The core UI will be a client-side SPA.  Flask could therefore be
reserved for small, purely server-side admin pages or PDF exports (if ever
required).  Django is deemed too heavy for the limited server-rendered needs
and would introduce an overlapping ORM.

--------------------------------------------------------------------------------

## 2 Phase Overview & Status

Legend 🟢 done 🟡 in progress 🔴 not started

| Phase | Scope (2-week time-box) | Status |
|-------|-------------------------|--------|
| **0** | Project scaffolding, CI, Docker Compose, pre-commit, health-check endpoint | 🟢 completed |
| **1** | Member + Unit CRUD (API & UI); baseline auth (JWT) | 🟢 completed |
| **2** | Task / Responsibility module (Kanban), e-mail reminders | 🟡 in progress |
| **3** | Voting / Polling engine, live result feed (WebSockets) | 🔴 |
| **4** | Scorecards & KPI dashboards | 🔴 |
| **5** | Hardening, docs, 80 % test coverage, CI/CD to staging | 🟡 in progress |

--------------------------------------------------------------------------------

## 3 Detailed Work-breakdown

Below each major folder is listed with the **outstanding todo items**.  The
⚙️ emoji marks tasks that require a design decision or spike.

### 3.1 `backend/app/`

1. **core/**
   • `config.py`: move from ad-hoc env parsing to *Pydantic-Settings* model. ✅ implemented via Pydantic BaseSettings.
   • add structured logging (structlog + UVicorn access logs). ⚙️ pending implementation.
   • implement global error-handling & standardized error responses. ⚙️ pending design.

2. **models/**
   • complete SQLAlchemy model stubs for `Member`, `Unit`, `Task`, `Proposal`, `Vote`, `ScoreEntry` (columns & FKs). ✅ model definitions in place.
   • define ORM `relationship()` attributes for bidirectional associations. ⚙️ pending implementation.
   • write initial Alembic revision for schema migrations. ⚙️ pending.

3. **schemas/**
   • Generate matching Pydantic v2 models (DTOs) for every SQL model. ✅ schemas implemented for all domain types.
   • Introduce `BaseSchema` with JSON-serialization helpers. ⚙️ consider adding base class for shared config.

4. **api/**
   • `api.v1.endpoints.auth`: JWT login endpoint with token generation. ✅ implemented.
   • `api.v1.endpoints.members`: list/create/update/delete + pagination. ✅ implemented.
   • `api.v1.endpoints.units`: list/create/update/delete. ✅ implemented.
   • `api.v1.endpoints.tasks`: CRUD for Task objects. ✅ implemented.
   • `api.v1.endpoints.votes`, `metrics`: placeholder endpoints returning 501. ⚙️ implement in Phases 3 & 4.
   • `api.v1.endpoints.todo`: in-memory todo example. ⚙️ evaluate removal or integration.

5. **services/**
   • business rules for task assignment limits and quorum calculation. ⚙️ pending implementation in `task_service.py` and `vote_service.py`.

6. **jobs/**
   • Celery app configuration (`celery_app` broker setup). ✅ defined in `jobs/celery.py`.
   • Celery tasks `send_notification_email` and `recompute_scores` exist as placeholders. ⚙️ implement worker discovery and integrate business logic.

7. **tests/**
   • tests for user & unit endpoints via in-memory SQLite. ✅ passing.
   • tests for task, vote, metrics endpoints are currently skipped. ⚙️ implement and enable pytest tests; target ≥80% coverage.
   • GitHub Actions CI pipeline for lint, test, and build. ⚙️ pending workflow setup.

### 3.2 `frontend/`

1. **Tool-chain**
   • Vite + React 18 + TypeScript baseline bootstrapped. ✅ implemented via Vite template.
   • ESLint + Prettier dependencies installed. ✅ .eslintrc & .prettierrc configured; pre-commit integration pending.
   • absolute path aliases configured (`@api`, `@components`, etc.). ✅ implemented in `vite.config.ts`.

2. **api/**
   • manual API hooks for users implemented (`src/api/users.ts`). ✅ functional for user CRUD.
   • placeholder hooks for units, tasks, votes, metrics in `src/api/`. ⚙️ implement CRUD hooks and integrate React Query.
   • configure OpenAPI codegen pipeline for type-safe hook generation. ⚙️ pending.

3. **pages/**
   • Dashboard: scaffold exists in `Dashboard.tsx`. ⚙️ implement data fetching and widgets.
   • Members: full CRUD UI implemented in `Members.tsx`. ✅ supports list, create, update, delete.
   • Units: scaffolded in `Units.tsx`. ⚙️ implement list & form for unit management.
   • Tasks: scaffolded Kanban view in `Tasks.tsx`. ⚙️ implement drag-and-drop and API integration.
   • Votes: scaffolded in `Votes.tsx`. ⚙️ implement proposals list, voting form, and results.
   • Scorecards: scaffolded in `Scorecards.tsx`. ⚙️ implement charts and scorecard displays.

4. **components/**
   • `DataTable`, `ConfirmDialog`, `KanbanBoard`, `VoteChart` components exist as stubs. ⚙️ implement using MUI and charting library (e.g., Recharts).

5. **State management**
   • React Query used for user data; ⚙️ ensure global `QueryClientProvider` in `App.tsx`.
   • `AuthContext` scaffolded in `src/context/AuthContext.tsx`. ⚙️ integrate authentication flows and protected routes.
   • evaluate advanced state needs once multi-entity interactions scale.

### 3.3 `infrastructure/`

1. **docker-compose.yml**
   • add Redis and Celery worker services for background jobs. ⚙️ update compose file.
   • mount a dedicated Docker volume for Postgres data. ✅ configured.
   • add container health-checks (db, backend, redis). ⚙️ pending.

2. **GitHub Actions**
   • CI: lint → test → build → push Docker image. ⚙️ create `.github/workflows/ci.yml`.
   • CD (optional): deploy to staging DigitalOcean/Kubernetes. ⚙️ consider using GitHub Actions or other CI/CD tool.

### 3.4 `docs/`

• `architecture.md` draft exists. ⚙️ flesh out C4 component, container, and deployment diagrams.
• Sequence diagram for voting flow. ⚙️ create UML/PlantUML and include in docs.
• Auto-generate ERD from SQLAlchemy metadata. ⚙️ integrate ERAlchemy or similar and embed ERD.
• Business requirements & action plan PDFs present. ✅ reference in `docs/`.

--------------------------------------------------------------------------------

## 4 Issue Tracking & Contribution Workflow

1. Every bullet point above should become a **GitHub issue** with labels:  
   • `phase:X` • `backend` / `frontend` / `infra` • `good-first-issue` (if easy).

2. Small PRs › easier review.  Include unit tests & documentation where
   relevant.

3. **Definition of Done (DoD)**  
   • all automated tests pass  
   • code-coverage does not regress  
   • lints (`pre-commit run --all-files`) are clean  
   • documentation is updated (OpenAPI, this file, READMEs).

--------------------------------------------------------------------------------

## 5 Environment Variables (summary)

| Name | Example | Purpose |
|------|---------|---------|
| `POSTGRES_HOST` | `postgres` | hostname of DB container |
| `POSTGRES_DB`   | `thecooperator` | database name |
| `POSTGRES_USER` | `tc_app` | DB user |
| `POSTGRES_PASSWORD` | `super-secret` | DB password |
| `JWT_SECRET`    | `change-me-pls` | HMAC secret for auth tokens |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Celery / Redis |

--------------------------------------------------------------------------------

## 6 Next Step for New Contributors

1. Clone the repo and run `docker compose up --build`.  
2. Pick an open issue from the **current 'in progress' phases (refer to Phase Overview & Status)** or a `good-first-issue` from any phase.
3. Make sure you read the *Developer Setup* section inside `README.md` (will be
   expanded as part of Phase 1).

Happy hacking! 💜
