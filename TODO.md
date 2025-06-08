 # theCooperator — To-Do List

## Current Focus: Phase 2 — Tasks & Duties

### Backend
 - [ ] Implement Task CRUD enhancements: due-date reminders and status transitions
 - [ ] Complete business logic in `task_service.py` and `vote_service.py` (assignment limits, quorum calculation)
 - [ ] Remove or integrate the `/api/v1/todo` placeholder endpoint
 - [ ] Implement Celery tasks: `send_notification_email` and `recompute_scores`; configure broker and workers
- [ ] Add Alembic migrations for current SQLAlchemy models
- [x] Implement global error handlers and structured logging (structlog + Uvicorn logs)
 - [ ] Finish 501 endpoints: `/metrics/dashboard`, `/metrics/scorecards`, and vote endpoints
- [x] Write tests for tasks endpoints and basic CRUD flow (metrics & votes pending)

 ### Frontend
 - [ ] Create API hooks for Units, Tasks, Votes, and Metrics using React Query
 - [ ] Implement Kanban board in `Tasks.tsx`: drag-and-drop, data fetching, status updates
 - [ ] Build voting UI in `Votes.tsx`: proposals list, voting form, live result charts
 - [ ] Integrate due-date reminders and notifications in the UI
 - [ ] Secure routes via `AuthContext` and provide JWT token to API client
 - [ ] Configure ESLint and Prettier; integrate with pre-commit hooks

 ### Infrastructure
 - [ ] Update `docker-compose.yml`: add Redis and Celery worker services; configure health-checks
 - [ ] Create `.env.example` with required environment variables
 - [ ] Set up GitHub Actions workflow for CI (lint, test, build)

 ### Documentation & DevOps
 - [ ] Expand `docs/architecture.md` with C4 diagrams and sequence diagrams for voting flow
 - [ ] Generate ERD from SQLAlchemy metadata and embed in docs
 - [ ] Update `README.md` quick-start instructions, including front-end proxy setup
 - [ ] Add changelog entry for completed Phase 1 items and update `DEVELOPMENT_ROADMAP.md` statuses
 - [ ] Finalize `TODO.md` and create GitHub issues for top-priority items
