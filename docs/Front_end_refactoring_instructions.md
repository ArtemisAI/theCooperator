0 | Starting point (June 2025 snapshot)
Phase status – repo roadmap shows you are in Phase 2 “Tasks & Duties”; Kanban UX is not yet implemented 
github.com

Monorepo layout – FastAPI backend (backend/app) + React 18 / Vite frontend (frontend/src) + Docker Compose infra 
github.com

No drag-and-drop code is present; tasks are exposed through early CRUD endpoints only.

1 | Target architecture for the Kanban board (with dnd-kit)
pgsql
Copy
 ┌─────────────┐    WebSocket      ┌────────────────────┐
 │ React GUI   │  ← live updates ─ │ FastAPI  /tasks WS │
 │  dnd-kit    │ ─ REST PATCH/GET →│  + SQLAlchemy ORM  │
 └─────────────┘                   └────────────────────┘
            ▲                                     │
            │ TanStack Query cache / optimistic   │
            ▼                                     ▼
       Zustand store                    PostgreSQL (Task, Lane tables)
Slice	Key design choices
Board engine	@dnd-kit/core + @dnd-kit/sortable with verticalListSortingStrategy; keyboard + pointer sensors registered for a11y.
State	Real-time order kept in React Query cache; global UI state (filters / preferences) in Zustand.
Persistence	New REST PATCH /tasks/reorder accepts {task_id, new_lane, before_id, after_id}; WebSocket topic tasks.updated broadcasts canonical order.
DB model	tasks gets lane_id (FK) and sort_index (float) so inserts are O(1). Separate lanes table to allow custom columns later.
Virtualisation	Each <Lane> body wrapped with @tanstack/react-virtual for 1 k+ cards. dnd-kit measuring API piggy-backs on virtual row heights.
Security	Authorise both REST and WS calls via your existing JWT middleware; server verifies membership in the same co-op before accepting reorder.

2 | What must change
Area	Replace / Add	Notes
Backend schema	➕ lane table, ➕ sort_index column on tasks, Alembic migration.	
API layer	➕ /lanes CRUD, /tasks/reorder, socket endpoints: subscribe_tasks, broadcast_task_order.	
Services	New reorder_task() domain service that re-indexes only the affected lane on large moves.	
Frontend	Replace temporary list rendering in pages/TasksPage.tsx with <KanbanBoard> composed of dnd-kit contexts; delete any MUI Table placeholder.	
CI pipeline	Add vitest + Playwright jobs; run backend contract tests with schemathesis on the Swagger diff.	
Docs	Extend docs/architecture.md with sequence diagram above and API payload examples.	

3 | Quality-gate matrix
Level	Tooling	Example test you must write
Unit (backend)	pytest-asyncio	Moving a task recalculates only that lane’s indexes (no gaps >1e6).
Unit (UI)	vitest + @testing-library/react + dnd-kit helpers	Card gains aria-grabbed="true" on Space key.
Service / contract	schemathesis fuzzes OpenAPI	PATCH /tasks/reorder rejects illegal before/after combos.
E2E	Playwright	Drag card from “To-Do” to “Done”, reload browser, order persists.
Performance	locust	100 concurrent reorder ops keep P95 < 200 ms.
A11y	axe-core CI check	Board passes WCAG 2.1 AA colour & role rules.

4 | Iterative roadmap (6 sprints → ±10 weeks)
Sprint (2 wks)	Deliverables you can demo	Code/infra tasks
S-0 : schema spike	Alembic migration merges; Swagger shows new fields.	Add lane & sort_index; seed default “Backlog / In-Progress / Done”.
S-1 : minimal board	Static <KanbanBoard> renders real task data; drag prints to console.	Install dnd-kit; build Lane, Card comps; hook sensors.
S-2 : optimistic reorder	Dragging updates UI immediately; POST saves order; manual refresh shows same order.	Implement /tasks/reorder; wire React Query mutation + optimistic cache.
S-3 : WebSocket sync	Open two browsers; drag in one, other updates live.	FastAPI WS endpoint; useTaskChannel hook with reconnection.
S-4 : virtual lanes & a11y	Scroll through 1 000 cards @ 60 fps; full keyboard drag; NVDA announces moves.	Integrate react-virtual; add KeyboardSensor; axe-core fixes.
S-5 : hardening & CI	Playwright suite green on GitHub Actions; Lighthouse a11y score ≥ 95.	Add all test tiers; Docker multi-stage build shrinks front-image < 120 MB.

5 | “Done” criteria for Phase 2 (Tasks & Duties)
Drag-and-drop board meets WCAG 2.1 AA.

Task re-ordering latency < 200 ms (95ᵗʰ).

All new code ≥ 85 % line coverage; zero P1–P2 Snyk findings.

Product demo: Admin signs in → drags three tasks → resident’s dashboard reflects change live.

6 | Risk watch-list & mitigations
Risk	Mitigation
Sort-index overflow / drift	Use floating “fractional indexing”; rebuild lane indexes nightly with Celery task.
dnd-kit future maintenance	Encapsulate board in ui/kanban package; adapter layer > 200 LOC makes vendor swap feasible.
WebSocket scaling	Keep per-tenant NATS subject naming; if you adopt multi-coop (Phase 9) use NATS JetStream instead of Redis-pubsub.

TL;DR
Implementing dnd-kit requires one DB tweak, two new endpoints, a React board composed from dnd-kit Sortable contexts, and a disciplined test pyramid. Six well-scoped sprints will land a production-ready, accessible Kanban that aligns with theCooperator’s Phase 2 goals and is robust enough to survive the later multi-tenant push.

<KanbanBoard>
  <DndContext sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}>
    {columns.map(col => (
      <SortableContext id={col.id}
                       items={col.cardIds}
                       strategy={verticalListSortingStrategy}>
        <Column>
          {cardsInCol.map(card => <Card key={card.id} id={card.id} />)}
        </Column>
      </SortableContext>
    ))}
  </DndContext>
</KanbanBoard>
--------

Optimistic Flow
handleDragEnd → mutate React Query cache.

PATCH /tasks/reorder with {task_id, new_lane, before_id, after_id}.

FastAPI broadcasts tasks.updated WS event → tabs reconcile canonical order.

Virtualisation
Wrap each <Column> body in useVirtual(); feed measured row heights back to dnd-kit for smooth auto-scroll.

Accessibility Quick-wins
Keep focus outline; expose aria-grabbed, aria-dropeffect.

Announce “{task} moved to {lane} position {index}”.

Provide lane-cycle shortcuts ([ and ]).

4. Incremental Delivery & Tests
Sprint	Goal & Key Tests	Expected Demo Output
S-0 (schema spike)	Alembic migration; Swagger shows lane_id, sort_index	DB tables seeded with Backlog/In-Progress/Done
S-1 (minimal board)	Vitest: renders lane + 1 k fake tasks; drag prints coords	Browser shows static board @ 60 fps
S-2 (optimistic reorder)	Unit: cache mutates instantly; API patch mocked	Reload keeps new order
S-3 (WebSocket sync)	Playwright: drag in tab A → tab B updates	Live multi-tab sync < 200 ms
S-4 (virtual & a11y)	Axe-core CI green; NVDA announces moves	Scroll 10 k cards stutter-free
S-5 (hardening & CI)	Coverage ≥ 85 %; Lighthouse a11y ≥ 95	GH Actions badge green

Test Pyramid
Unit – jest/vitest + dnd-kit helpers (KeyboardSensor events).

Service/contract – schemathesis fuzz PATCH.

E2E – Playwright dragAndDrop() asserts API order.

Perf – locust: 100 concurrent reorders P95 < 200 ms.

A11y – axe-linter in CI; manual NVDA/VoiceOver spot-checks.

5. Quality Gates (Definition of “Done” – Phase 2)
Area	Metric
UX & A11y	WCAG 2.1 AA; keyboard-only drag reachable
Latency	Reorder round-trip < 200 ms (p95)
Coverage	≥ 85 % lines; 0 P1-P2 Snyk vulns
Demo	Admin drags 3 tasks → resident dashboard updates live

6. Risk Log & Mitigations
Risk	Response
Sort-index drift	Fractional indexing; nightly Celery re-index.
dnd-kit abandoned	Wrap board in /ui/kanban; adapter ≤ 200 LOC → switch to Pragmatic in < 1 week.
WS fan-out scaling	Move per-coop channels to NATS JetStream when Phase 9 multi-tenant lands.

7. Immediate Actions (Week 1)
Bootstrap PoC – single lane, 1 k tasks, measure FPS.

Define /tasks/reorder payload – include sibling IDs.

Set CI guard – fail build on React 19 peer-dep conflicts.

Draft a11y test plan – NVDA + keyboard matrix.

TL;DR
Adopt dnd-kit + @tanstack/react-virtual today for a fast, accessible Kanban board that plugs into your React 19 stack. Keep the board isolated so a future switch to Atlassian’s Pragmatic engine is a small refactor, not a rewrite.
