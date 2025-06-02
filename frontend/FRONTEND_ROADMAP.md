# Frontend Roadmap

This document outlines the technical requirements, directory structure, and placeholder modules for the theCooperator frontend (React 18 + TypeScript + Vite + Material-UI).

## 1. Technical Requirements

- Node.js 20 LTS
- Vite (dev server & build)
- React 18
- TypeScript
- Material-UI (MUI) component library
- React Router v6 for routing
- React Query (@tanstack/react-query) for data fetching & caching
- OpenAPI codegen (openapi-typescript & react-query codegen) for type-safe API hooks
- ESLint + Prettier for linting & formatting
- Path aliases (e.g., @api, @components, @pages, @hooks, @utils) via tsconfig.json

## 2. Project Structure

frontend/
├── README.md
├── FRONTEND_ROADMAP.md
└── src/
    ├── api/            API service hooks (users, units, tasks, votes, metrics)
    ├── components/     Reusable UI components (DataTable, ConfirmDialog, KanbanBoard, VoteChart, etc.)
    ├── pages/          Route-level views (Dashboard, Members, Units, Tasks, Votes, Scorecards)
    ├── hooks/          Custom React hooks (useAuth, useDataQueries, etc.)
    ├── context/        React context providers (AuthContext, etc.)
    ├── utils/          Utility functions & API client
    ├── App.tsx         Root component & router
    └── main.tsx        Application entry point

## 3. Modules & Placeholders

### 3.1 API (src/api)
- users.ts: (implemented) basic fetch calls for /api/v1/users. TODO: replace with generated hooks (React Query + OpenAPI).
- units.ts: placeholder for CRUD hooks for /api/v1/units.
- tasks.ts: placeholder for CRUD hooks for /api/v1/tasks.
- votes.ts: placeholder for vote proposals, casting votes, and results.
- metrics.ts: placeholder for dashboard metrics and scorecards.

### 3.2 Components (src/components)
- DataTable.tsx: generic table wrapper using MUI DataGrid.
- ConfirmDialog.tsx: confirmation modal for destructive actions.
- KanbanBoard.tsx: drag-and-drop kanban board for tasks.
- VoteChart.tsx: chart component for vote results.
- (Future) ScorecardWidget.tsx: widget for displaying participation metrics.

### 3.3 Pages (src/pages)
- Dashboard.tsx: high-level metrics & snapshots.
- Members.tsx: member list & CRUD (basic UI implemented).
- Units.tsx: unit list & CRUD.
- Tasks.tsx: task management (kanban view).
- Votes.tsx: voting & proposal management.
- Scorecards.tsx: participation scorecards & analytics.

### 3.4 Hooks & Context
- useAuth (src/hooks/useAuth.ts): authentication state & methods (login, logout).
- AuthContext (src/context/AuthContext.tsx): provides auth context to App.
- (Future) useDataQueries: wrapper to combine React Query hooks.

### 3.5 Utilities
- apiClient.ts: central fetch/axios client with baseURL and auth token injection.
- index.ts: export utilities.

### 3.6 App & Entry Point
- App.tsx: configure React Router, global providers (QueryClientProvider, AuthContextProvider), and layout.
- main.tsx: bootstrap React application into the DOM.

## 4. Next Steps

1. Scaffold Vite project with TS template.
2. Install dependencies: react, react-dom, react-router-dom, @tanstack/react-query, @mui/material, @mui/icons-material, eslint, prettier, typescript.
3. Configure tsconfig.json for path aliases.
4. Set up OpenAPI codegen pipeline to generate API hooks and types.
5. Implement placeholder modules:
   - API methods in src/api (units, tasks, votes, metrics).
   - UI components in src/components.
   - Pages in src/pages.
   - Auth hook and context.
   - apiClient and utilities.
   - App routing and provider wrappers.
6. Add ESLint and Prettier configs and integrate with pre-commit.
7. Set up basic tests (React Testing Library) for components and pages.
