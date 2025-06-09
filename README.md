# theCooperator

Unified Member Management & Participation Platform for Housing Cooperatives

--------------------------------------------------------------------------------

Table of Contents
1. Vision
2. Core Functionalities
3. Technical Architecture (high-level)
4. Development Roadmap (summary)
5. Module Layout
6. Quick-start for Local Dev


1 Vision
-----------
theCooperator gives small & medium-sized housing co-operatives the modern,
data-driven tooling usually reserved for large commercial property managers:

• a single source of truth for members, units and duties  
• transparent task & responsibility tracking  
• democratic decision-making through secure online voting  
• personal and aggregate scorecards that visualise participation & community
  health  
• real-time notifications and self-service dashboards for every resident


2 Core Functionalities (MVP)
---------------------------
1. Member & Unit Management – CRUD, unit ↔ member mapping.
2. Task Tracking – Kanban flow, due-dates & reminders.
3. Voting & Polling – proposals, ballots, quorum, live results.
4. Scorecards & Analytics – participation metrics & co-op KPIs.
5. Notifications – e-mail / in-app alerts, webhook outbox.
6. Access Control – JWT auth, resident / admin / observer roles.


3 Technical Architecture (bird’s-eye)
------------------------------------

Backend   FastAPI (Python 3.11, async)  + SQLAlchemy ORM + PostgreSQL + Alembic

             │—— Celery + Redis for background jobs (notifications, scores)  
             │—— Native FastAPI WebSockets for live updates

Frontend  React 18 + TypeScript + Vite + MUI component library

DevOps    Docker Compose for local, GitHub Actions CI → optional Kubernetes



4 Development Roadmap (condensed)  ↗ Full details in `ROADMAP_REBOOT.md`
-------------------------------------------------------------------------

Phase 0   Foundation              🟢 done
Phase 1   Members & Units         🟢 done
Phase 2   Tasks & Duties          🟡 in progress
Phase 3   Voting                  🔴
Phase 4   Analytics               🔴
Phase 5   File Uploads            🔴
Phase 6   Notifications           🔴
Phase 7   Hardening & Deployment  🔴
Phase 8   Beta Feedback & Polish  🔴
Phase 9   Multi-Co-op Tenancy     🔴
Phase 10  Maintenance & Assets    🔴
Phase 11  Finance Integration     🔴
Phase 12  Extensions & Community  🔴

5 Module Layout (monorepo)
--------------------------

backend/
  app/
    core/      settings, logging, security helpers
    db/        SQLAlchemy engine & session factory (async)
    models/    ORM models (Member, Unit, Task, …)
    schemas/   Pydantic schemas / DTOs
    crud/      thin persistence helpers
    services/  business logic (e.g. score calculation)
    api/       versioned FastAPI routers
    jobs/      Celery tasks

frontend/
  src/ api/ components/ pages/ …

infrastructure/
  docker-compose.yml    local dev stack  
  Dockerfile.backend    backend image

docs/ architecture.md, business PDFs, etc.


6 Quick-start (dev)
-------------------
Prerequisites: Docker + Docker Compose.

```bash
git clone https://github.com/<you>/theCooperator.git
cd theCooperator/infrastructure
docker compose up --build
```

The API is now on `http://localhost:8000` – open
`http://localhost:8000/docs` for the Swagger UI. On first run the
SQLite database will be created automatically with demo data.
Run the React app from `frontend/` with:

```bash
npm install
npm run dev
```

Alternatively run the backend directly during early phases:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.api:app --reload
celery -A app.celery_app.celery_app worker --loglevel=info  # optional

=======
```

To initialise the local database using Alembic migrations run:

```bash
alembic upgrade head
```

## Data Model (Phase 1)


 +------------+        +-------------+
 | Unit       |        | Member      |
 +------------+        +-------------+
 | id   PK    |<--+  +-| id     PK   |
 | name       |    |  | name        |
 +------------+    |  | email       |
                  +--| unit_id  FK |
                     +-------------+

Developer Setup

If you prefer to run the backend without Docker:

```bash
cd backend
pip install -r requirements.txt
pre-commit install   # optional linting hooks
```

© 2024 theCooperator — MIT licence.
