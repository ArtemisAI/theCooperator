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

## 3. Kanban Board Architecture

```
┌─────────────┐    WebSocket      ┌────────────────────┐
│ React GUI   │  ← live updates ─ │ FastAPI  /tasks WS │
│  dnd-kit    │ ─ REST PATCH/GET →│  + SQLAlchemy ORM  │
└─────────────┘                   └────────────────────┘
           ▲                                     │
           │ TanStack Query cache / optimistic   │
           ▼                                     ▼
      Zustand store                    PostgreSQL (Task, Lane tables)
```

The board is composed using **@dnd-kit** with `SortableContext` and
`verticalListSortingStrategy`. Task order is kept in React Query cache and
persisted via `PATCH /tasks/reorder`. Clients subscribe to the
`tasks.updated` WebSocket topic to synchronise across tabs.

## 4. Diagrams

* **C4** container and component diagrams – TODO (`docs/diagrams/` will contain
  PlantUML sources).
* **Sequence diagrams** – voting workflow and Kanban drag‑and‑drop.
* **Entity Relationship Diagram** – generated from SQLAlchemy models using
  `eralchemy`.

## 5. Further Reading

See `ROADMAP_REBOOT.md` for the phased development plan and `README.md` for a
quick overview of the project goals.

## 6. Database Schema

The backend currently uses **SQLAlchemy** models with **Alembic** migrations to
manage schema updates.  During development an SQLite database is created
automatically; production deployments target PostgreSQL.  Administrators can add
or remove columns via new migration scripts.

### Tables

| Table       | Key | Fields & Notes                                                                |
|-------------|-----|-------------------------------------------------------------------------------|
| `units`     | `id` PK | `name` (unique)                                                            |
| `members`   | `id` PK | `name`, `email` (unique), `unit_id` → `units.id`                           |
| `tasks`     | `id` PK | `title`, `status` enum, `priority` enum, `due_date`, `assignee_id` → `members.id`, `lane_id` → `lanes.id`, `sort_index` float |
| `lanes`     | `id` PK | `name`, `sort_index` float |
| `committees` *(planned)* | `id` PK | `name`, `description`                                         |

### Relationships

* **Unit → Member** – one unit may have many members. Members reference their
  unit via `unit_id`.
* **Member → Task** – tasks may optionally be assigned to a member via
  `assignee_id`.
* **Lane → Task** – every task is ordered within a lane via `lane_id` and
  `sort_index`.
* **Committee → Task** – future work will allow tasks to be linked to
  committees, enabling group ownership.

### Administration

CRUD endpoints expose these tables so data can be created, updated or deleted
through the API or a future admin UI.  When schema changes are required,
administrators create Alembic migrations to alter the tables safely and keep
environments in sync.
For local demos and tests a helper endpoint `POST /demo/reset` drops all
tables and re-inserts the default fixtures.
