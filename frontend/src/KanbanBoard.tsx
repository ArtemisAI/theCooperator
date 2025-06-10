import { DndContext, closestCenter, type DragEndEvent, useDroppable } from '@dnd-kit/core';
import { SortableContext, useSortable, verticalListSortingStrategy, arrayMove } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useState, useEffect, useCallback } from 'react';

export interface Task {
  id: number;
  title: string;
  status: 'todo' | 'in_progress' | 'done';
  priority?: string;
  due_date?: string;
  assignee_id?: number;
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

export function KanbanBoard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [apiError, setApiError] = useState<string | null>(null);

  const clearError = useCallback(() => setApiError(null), []);

  // Function to display error and automatically clear it after some time
  const showError = useCallback((message: string, duration: number = 5000) => {
    setApiError(message);
    setTimeout(() => {
      clearError();
    }, duration);
  }, [clearError]);

  useEffect(() => {
    const fetchTasks = async () => {
      clearError(); // Clear previous errors
      try {
        const response = await fetch('/tasks/');
        if (!response.ok) {
          throw new Error(`Failed to load tasks. Server responded with ${response.status}.`);
        }
        const data = await response.json();
        setTasks(data as Task[]);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
        showError(error instanceof Error ? error.message : "An unknown error occurred while fetching tasks.");
      }
    };

    fetchTasks();
  }, [showError, clearError]); // Added showError and clearError to dependency array

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    const activeId = active.id;
    const overId = over.id;

    // Find the task being dragged
    const activeTask = tasks.find(t => t.id === activeId);
    if (!activeTask) return;

    // Determine the new status
    let newStatus: Task['status'] | undefined = undefined;
    const overIsLane = lanes.some(l => l.id === overId);

    if (overIsLane) {
      newStatus = overId as Task['status'];
    } else {
      // If dropped on another task, inherit that task's status
      const overTask = tasks.find(t => t.id === overId);
      if (overTask) {
        newStatus = overTask.status;
      }
    }

    if (!newStatus || newStatus === activeTask.status && activeId === overId) {
      // If status didn't change and not dropped on a different item in the same list (simple reorder)
      // For simple reordering within the same list when status doesn't change:
      if (activeId !== overId && !overIsLane) {
        setTasks(currentTasks => {
          const activeIndex = currentTasks.findIndex(t => t.id === activeId);
          const overIndex = currentTasks.findIndex(t => t.id === overId);
          if (activeIndex !== -1 && overIndex !== -1) {
            return arrayMove(currentTasks, activeIndex, overIndex);
          }
          return currentTasks;
        });
      }
      return; // No status change or API call needed, or only reorder
    }

    const previousTasks = [...tasks]; // Store for potential rollback

    // Optimistic UI update
    setTasks(currentTasks => {
      const activeIndex = currentTasks.findIndex(t => t.id === activeId);
      if (activeIndex === -1) return currentTasks; // Should not happen

      // If dropped on a lane
      if (overIsLane) {
        const updatedTasks = [...currentTasks];
        updatedTasks[activeIndex] = { ...updatedTasks[activeIndex], status: newStatus! };
        return updatedTasks;
      }

      // If dropped on another task (implies reorder and status change)
      const overIndex = currentTasks.findIndex(t => t.id === overId);
      if (overIndex === -1) return currentTasks; // Should not happen if overTask was found

      // Create the new version of the task
      const taskWithNewStatus = { ...currentTasks[activeIndex], status: newStatus! };

      // Remove the item from its old position
      const tempTasks = [...currentTasks];
      tempTasks.splice(activeIndex, 1);

      // Insert the item at the new position
      // Need to find the correct index in the potentially filtered list for arrayMove logic
      // For simplicity, let's just place it and let dnd-kit handle visual reordering if needed,
      // or adjust arrayMove logic if strict ordering is critical after status change and move.
      // The current arrayMove in the original code handles reordering within the full list.
      // We will apply status change first, then reorder.

      let reorderedTasks = currentTasks.map(t => t.id === activeId ? taskWithNewStatus : t);
      if (activeId !== overId) { // if it's not dropped on itself
        const updatedActiveIndex = reorderedTasks.findIndex(t => t.id === activeId);
        const updatedOverIndex = reorderedTasks.findIndex(t => t.id === overId);
         if (updatedActiveIndex !== -1 && updatedOverIndex !== -1) {
           // Ensure the task being moved inherits the target's status correctly
           // And other tasks in the list remain as they are or are reordered.
           reorderedTasks = arrayMove(reorderedTasks, updatedActiveIndex, updatedOverIndex);
         }
      }
      return reorderedTasks;
    });

    // Prepare task data for the API
    const taskPayloadForApi: Task = {
      ...activeTask, // Spread the original task
      status: newStatus!, // Apply the new status
      // Other fields like title, priority, due_date, assignee_id remain from activeTask
    };

    // Make the API call
    try {
      const response = await fetch(`/tasks/${taskPayloadForApi.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          // Send fields that can be updated, matching TaskBase or a specific TaskUpdate schema
          title: taskPayloadForApi.title,
          status: taskPayloadForApi.status,
          priority: taskPayloadForApi.priority,
          due_date: taskPayloadForApi.due_date,
          assignee_id: taskPayloadForApi.assignee_id,
        }),
      });

      if (!response.ok) {
        // If API fails, revert to previous state
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      // Optional: if the backend returns the updated task, you might want to setTasks(updatedTaskFromApi)
      // For now, optimistic update is assumed to be correct.
      console.log(`Task ${taskPayloadForApi.id} updated successfully.`);
      clearError(); // Clear any previous errors on successful update
    } catch (error) {
      console.error(`Failed to update task ${taskPayloadForApi.id}:`, error);
      setTasks(previousTasks); // Rollback
      showError(error instanceof Error ? error.message : `Failed to update task ${taskPayloadForApi.id}.`);
    }
  };

  return (
    <div>
      {apiError && (
        <div style={{ color: 'red', padding: '10px', border: '1px solid red', marginBottom: '10px' }}>
          <strong>Error:</strong> {apiError}
          <button onClick={clearError} style={{ marginLeft: '10px' }}>Dismiss</button>
        </div>
      )}
      {/* Test-only button to trigger handleDragEnd */}
      {process.env.NODE_ENV === 'test' && (
        <button
          data-testid="test-drag-end-trigger"
          onClick={() => {
            // Example: Simulate dragging task 1 to 'in_progress' lane
            const mockEvent = {
              active: { id: 1 }, // Assuming task with id 1 exists
              over: { id: 'in_progress' }, // Target lane id
            } as DragEndEvent;
            handleDragEnd(mockEvent);
          }}
        >
          Trigger Test Drag End
        </button>
      )}
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
