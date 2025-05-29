import React from 'react';
import { KanbanBoard } from '../components/KanbanBoard';

/**
 * Tasks page
 *
 * - Displays tasks in a Kanban board layout.
 * - Fetches tasks data from src/api/tasks.
 *
 * TODO:
 *  - Implement drag-and-drop interactions.
 *  - Connect with API via React Query.
 */

export default function TasksPage() {
  return (
    <div>
      <h1>Tasks</h1>
      <KanbanBoard />
    </div>
  );
}
