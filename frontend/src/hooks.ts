import { useQuery } from '@tanstack/react-query';
import { Task } from './KanbanBoard';

export function useTasks() {
  return useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      const res = await fetch('/tasks/');
      if (!res.ok) throw new Error('Failed to fetch tasks');
      return res.json();
    }
  });
}
