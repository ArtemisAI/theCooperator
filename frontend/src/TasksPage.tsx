import { KanbanBoard } from './KanbanBoard';
import { useTasks } from './hooks';

export function TasksPage() {
  const { data: tasks = [] } = useTasks();
  return <KanbanBoard initialTasks={tasks} />;
}
