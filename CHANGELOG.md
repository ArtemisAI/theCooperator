# Changelog

## [0.2.2] - Kanban update endpoint
### Added
- `/tasks/{id}` PUT endpoint and supporting schema to update tasks from the Kanban board.

## [0.2.0] - Begin Phase 2
- Marked Phase 1 as complete in documentation.
- Updated roadmaps and contributor instructions to focus on Task Management.
- Implemented Task model, CRUD API and tests.
- Added Celery skeleton for due-date reminders.

### Frontend
- Implemented Kanban board with drag-and-drop and React Query task fetching.

### Added
- `/demo/reset` endpoint for recreating demo fixtures
- Shared seeding logic for tests and local demo instances

## [0.2.1] - Fix Kanban integration tests
### Fixed
- Completed missing closing tag in `KanbanBoard.tsx` causing Vitest failures.
- Updated frontend tests to reflect API payloads and added cleanup hooks.
- Ensured backend requirements installed for pytest run.

## [0.1.0] - Initial Phase 1 Skeleton
- Added backend FastAPI application with Member and Unit CRUD endpoints.
- Added SQLite database setup with demo seed data.
- Added pytest integration test for basic Member flow.
- Updated README with backend start instructions.
