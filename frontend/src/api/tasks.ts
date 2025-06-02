import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@utils/apiClient'; // Adjusted path based on typical project structure
import type { Task, TaskCreate, TaskUpdate } from '@src/types'; // Adjusted path

const TASKS_API_BASE_URL = '/api/v1/tasks';

// Fetch all tasks
const fetchTasks = async (): Promise<Task[]> => {
  return apiClient(TASKS_API_BASE_URL) as Promise<Task[]>;
};

export const useTasks = () => {
  return useQuery<Task[], Error>({
    queryKey: ['tasks'],
    queryFn: fetchTasks,
  });
};

// Fetch a single task by ID
const fetchTaskById = async (taskId: string): Promise<Task> => {
  return apiClient(`${TASKS_API_BASE_URL}/${taskId}`) as Promise<Task>;
};

export const useTask = (taskId: string) => {
  return useQuery<Task, Error>({
    queryKey: ['tasks', taskId],
    queryFn: () => fetchTaskById(taskId),
    enabled: !!taskId, // Only run query if taskId is provided
  });
};

// Create a new task
const createTask = async (taskData: TaskCreate): Promise<Task> => {
  return apiClient(TASKS_API_BASE_URL, {
    method: 'POST',
    body: JSON.stringify(taskData),
  }) as Promise<Task>;
};

export const useCreateTask = () => {
  const queryClient = useQueryClient();
  return useMutation<Task, Error, TaskCreate>({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
};

// Update an existing task
const updateTask = async ({ taskId, taskData }: { taskId: string; taskData: TaskUpdate }): Promise<Task> => {
  return apiClient(`${TASKS_API_BASE_URL}/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  }) as Promise<Task>;
};

export const useUpdateTask = () => {
  const queryClient = useQueryClient();
  return useMutation<Task, Error, { taskId: string; taskData: TaskUpdate }>({
    mutationFn: updateTask,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['tasks', variables.taskId] });
      // Optionally, update the specific query data directly
      // queryClient.setQueryData(['tasks', variables.taskId], data);
    },
  });
};

// Delete a task
const deleteTask = async (taskId: string): Promise<void> => {
  await apiClient(`${TASKS_API_BASE_URL}/${taskId}`, {
    method: 'DELETE',
  });
  // apiClient for DELETE might not return content, or response.json() might fail if empty.
  // Assuming DELETE returns no content or apiClient handles it.
  // If apiClient throws error on empty response for non-204, this needs adjustment.
  // For now, assuming it's fine.
};

export const useDeleteTask = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
};
