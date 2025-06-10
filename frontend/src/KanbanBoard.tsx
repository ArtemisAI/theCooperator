import { DndContext, closestCenter } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useState } from 'react';

export interface Task {
  id: number;
  title: string;
  status: 'todo' | 'in_progress' | 'done';
}

const lanes = [
  { id: 'todo', title: 'To Do' },
  { id: 'in_progress', title: 'In Progress' },
  { id: 'done', title: 'Done' }
];

export function KanbanBoard({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState(initialTasks);

  const handleDragEnd = () => {
    // TODO: reorder logic will go here
  };

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        {lanes.map(lane => {
          const items = tasks.filter(t => t.status === lane.id);
          return (
            <div key={lane.id} data-testid={`lane-${lane.id}`}
                 style={{ flex: 1, background: '#fafafa', padding: '0.5rem' }}>
              <h3>{lane.title}</h3>
              <SortableContext items={items.map(i => i.id.toString())}
                               strategy={verticalListSortingStrategy}>
                {items.map(task => (
                  <div key={task.id} data-testid={`task-${task.id}`} style={{ margin: '0.25rem', padding: '0.25rem', border: '1px solid #ccc' }}>
                    {task.title}
                  </div>
                ))}
              </SortableContext>
            </div>
          );
        })}
      </DndContext>
    </div>
  );
}
