import { useEffect, useState } from 'react';
import { KanbanBoard, Task } from './KanbanBoard';

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    fetch('/tasks/')
      .then(r => r.json())
      .then(data => setTasks(data));
  }, []);

  return <KanbanBoard initialTasks={tasks} />;
}
