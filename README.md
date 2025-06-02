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


4 Development Roadmap (condensed)  ↗ Full details in `DEVELOPMENT_ROADMAP.md`
-------------------------------------------------------------------------

Phase 0   Scaffolding             🟢 done  
Phase 1   Members & Units CRUD    🟡 in progress  
Phase 2   Task Management         🔴  
Phase 3   Voting / Polling        🔴  
Phase 4   Dashboards & Scores     🔴  
Phase 5   Hardening & Deployment  🔴


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


6 Quick-start (dev)
-------------------
Prerequisites: Docker + Docker Compose.

```bash
git clone https://github.com/<you>/theCooperator.git
cd theCooperator/infrastructure
docker compose up --build
```

The API is now on `http://localhost:8000` – open
`http://localhost:8000/docs` for the Swagger UI. A minimal *Members* screen is
available in the React front-end (`frontend/`); run `npm i && npm run dev` to
see it in action (proxy config still pending).

--------------------------------------------------------------------------------

© 2024 theCooperator — MIT licence.
