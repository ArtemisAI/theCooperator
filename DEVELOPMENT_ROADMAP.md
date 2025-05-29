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
| **1** | Member + Unit CRUD (API & UI); baseline auth (JWT) | 🟡 15 % |
| **2** | Task / Responsibility module (Kanban), e-mail reminders | 🔴 |
| **3** | Voting / Polling engine, live result feed (WebSockets) | 🔴 |
| **4** | Scorecards & KPI dashboards | 🔴 |
| **5** | Hardening, docs, 80 % test coverage, CI/CD to staging | 🔴 |

--------------------------------------------------------------------------------

## 3 Detailed Work-breakdown

Below each major folder is listed with the **outstanding todo items**.  The
⚙️ emoji marks tasks that require a design decision or spike.

### 3.1 `backend/app/`

1. **core/**
   • `config.py`: move from ad-hoc env parsing to *Pydantic-Settings* model.  
   • add structured logging (structlog + UVicorn access logs).  
   • ⚙️ decide on global error-handling & response format.

2. **models/**
   • complete SQLAlchemy models & relations for `Member`, `Unit`, `Task`,
     `Proposal`, `Vote`, `ScoreEntry`.  
   • write initial Alembic revision.

3. **schemas/**
   • Generate matching Pydantic v2 models (DTOs) for every SQL model.  
   • Introduce `BaseSchema` with JSON-serialisation helpers.

4. **api/**
   • `api.v1.endpoints.auth`: JWT login/refresh + password hashing (passlib).
   • `api.v1.endpoints.members`: list/create/update/delete + pagination.
   • `api.v1.endpoints.units`: idem.
   • After Phase 2: `tasks/`, Phase 3: `votes/`, Phase 4: `metrics/`.

5. **services/**
   • business rules (e.g. task assignment limits, quorum calculation).

6. **jobs/**
   • Celery worker configuration.  
   • tasks: send notification e-mails, recompute scorecards nightly.

7. **tests/**
   • bring coverage to ≥80 %; integrate with GitHub Actions.

### 3.2 `frontend/`

1. **Tool-chain**
   • Vite + React 18 + TS baseline already bootstrapped.  
   • configure ESLint + Prettier rules (pre-commit).  
   • add absolute path aliases (`@components/*`, `@api/*`).

2. **api/**
   • auto-generate type-safe hooks (React Query) from OpenAPI spec ⚙️.

3. **pages/**
   • Dashboard ➜ statistics widgets placeholder.  
   • Members ➜ data-grid CRUD form.  
   • Units ➜ as above.  
   • Tasks, Votes & Scorecards ﹣ to be scaffolded in Phases 2 – 4.

4. **components/**
   • generic `DataTable`, `ConfirmDialog`, `KanbanBoard`, `VoteChart`.

5. **State management**
   • keep it minimal: React Query cache + `useContext`.  
   • ⚙️ re-evaluate once complex cross-page state emerges.

### 3.3 `infrastructure/`

1. **docker-compose.yml**
   • add Redis and Celery worker services.  
   • mount a dedicated Docker volume for Postgres data.  
   • health-checks for each container.

2. **GitHub Actions**
   • CI: lint → test → build → push image.  
   • CD (optional): deploy to staging DigitalOcean droplet.

### 3.4 `docs/`

• Complete architecture diagrams (C4 model).  
• Sequence diagram: voting flow.  
• ERD auto-generated from SQLAlchemy metadata.

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
2. Pick an open issue from **Phase 1** – labels `good-first-issue` recommended.  
3. Make sure you read the *Developer Setup* section inside `README.md` (will be
   expanded as part of Phase 1).

Happy hacking! 💜
