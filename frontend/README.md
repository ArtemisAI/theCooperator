# Front-end (React) – placeholder

Run `npm install` followed by `npm run dev` once the backend is reachable at
`http://localhost:8000`. The first implemented screen is *Members* and can be
found in `src/pages/Members.tsx`.


The React project will be initialised with Vite + TypeScript once Phase 0 is
underway. Expected high-level structure:

src/
├── api/            – auto-generated hooks (e.g. React Query + OpenAPI)
├── components/     – reusable UI widgets
├── pages/          – route-level views (Dashboard, Members, Tasks, Votes…)
└── App.tsx         – root component / router

Until then this directory remains empty to keep the git tree tidy.
