# theCooperator – Software Architecture (draft)

## 1. Overview
This document outlines the software architecture for theCooperator. It will be progressively updated with component diagrams, sequence diagrams, and deployment topology as the project evolves. For a high-level project introduction, please refer to the main README.md.

## 2. Canonical Tech-stack
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

## 3. Detailed Diagrams
Detailed architectural diagrams, including C4 models, sequence diagrams for key flows (like voting), and an auto-generated Entity-Relationship Diagram (ERD) from SQLAlchemy metadata, are planned. These will be added in future updates as per the tasks outlined in the `DEVELOPMENT_ROADMAP.md` (section 3.4 `docs/`).
