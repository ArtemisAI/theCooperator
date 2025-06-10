import { DndContext, closestCenter, type DragEndEvent, useDroppable } from '@dnd-kit/core';
import { SortableContext, useSortable, verticalListSortingStrategy, arrayMove } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
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

function KanbanCard({ task }: { task: Task }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: task.id });
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    margin: '0.25rem',
    padding: '0.25rem',
    border: '1px solid #ccc'
  } as const;
  return (
    <div ref={setNodeRef} style={style} data-testid={`task-${task.id}`} {...attributes} {...listeners}>
      {task.title}
    </div>
  );
}

function Lane({ laneId, title, children }: { laneId: string; title: string; children: React.ReactNode }) {
  const { setNodeRef } = useDroppable({ id: laneId });
  return (
    <div ref={setNodeRef} data-testid={`lane-${laneId}`} style={{ flex: 1, background: '#fafafa', padding: '0.5rem' }}>
      <h3>{title}</h3>
      {children}
    </div>
  );
}

export function KanbanBoard({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState(initialTasks);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    setTasks(current => {
      const activeIndex = current.findIndex(t => t.id === active.id);
      if (activeIndex === -1) return current;

      const overLane = lanes.find(l => l.id === over.id);
      if (overLane) {
        // dropped on empty lane
        const updated = [...current];
        updated[activeIndex] = { ...updated[activeIndex], status: over.id as Task['status'] };
        return updated;
      }

      const overIndex = current.findIndex(t => t.id === over.id);
      if (overIndex === -1) return current;

      const updated = arrayMove(current, activeIndex, overIndex).map(t =>
        t.id === active.id ? { ...t, status: current[overIndex].status } : t
      );
      return updated;
    });
  };

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        {lanes.map(lane => {
          const items = tasks.filter(t => t.status === lane.id);
          return (
            <Lane key={lane.id} laneId={lane.id} title={lane.title}>
              <SortableContext items={items.map(i => i.id)} strategy={verticalListSortingStrategy}>
                {items.map(task => (
                  <KanbanCard key={task.id} task={task} />
                ))}
              </SortableContext>
            </Lane>
          );
        })}
      </DndContext>
    </div>
  );
}
