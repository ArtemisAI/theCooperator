# theCooperator – Software Architecture

This document provides a living overview of the system architecture used in the
reboot.  The aim is to capture key design decisions and outline where diagrams
will be placed.  Developers should keep this file updated as features evolve.

## 1. Component Overview

* **Frontend** – React SPA built with Vite and TypeScript.
  Responsible for all user interactions and real time updates via WebSockets.
* **Backend API** – FastAPI application exposing REST and WebSocket endpoints.
  Handles authentication, business rules and integrates with the database.
* **Celery Worker** – processes background jobs such as email notifications and
  periodic score calculations.
* **Database** – PostgreSQL with SQLAlchemy models and Alembic migrations.
* **Message Broker** – Redis used by Celery and for caching frequently accessed
  metrics.

## 2. Deployment Topology

```
Browser → Nginx → FastAPI → PostgreSQL
                        ↘ Celery → Redis
```

In local development Docker Compose spins up all services.  In production we
plan to deploy container images via GitHub Actions to a Kubernetes cluster or a
similar container orchestrator.

## 3. Diagrams

* **C4** container and component diagrams – TODO (`docs/diagrams/` will contain
  PlantUML sources).
* **Sequence diagram** for the voting workflow – TODO.
* **Entity Relationship Diagram** – generated from SQLAlchemy models using
  `eralchemy`.

## 4. Further Reading

See `ROADMAP_REBOOT.md` for the phased development plan and `README.md` for a
quick overview of the project goals.
