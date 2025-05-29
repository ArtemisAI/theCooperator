import apiClient from '@utils/apiClient'; // Using path alias

// Define the Todo types based on backend schemas
// These should ideally be in a shared types directory or generated from OpenAPI spec
export interface TodoRead {
  id: number;
  title: string;
  completed: boolean;
}

export interface TodoCreate {
  title: string;
  completed?: boolean;
}

export interface TodoUpdate {
  title?: string;
  completed?: boolean;
}

const API_BASE_URL = '/api/v1/todos'; // Matches the backend router prefix

export const getTodos = async (): Promise<TodoRead[]> => {
  const response = await apiClient.get<TodoRead[]>(API_BASE_URL);
  return response.data;
};

export const addTodo = async (todo: TodoCreate): Promise<TodoRead> => {
  const response = await apiClient.post<TodoRead>(API_BASE_URL, todo);
  return response.data;
};

export const updateTodo = async (id: number, todoUpdate: TodoUpdate): Promise<TodoRead> => {
  const response = await apiClient.put<TodoRead>(`${API_BASE_URL}/${id}`, todoUpdate);
  return response.data;
};

export const deleteTodo = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_BASE_URL}/${id}`);
};
