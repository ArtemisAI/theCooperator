/**
 * API service for Task endpoints (/api/v1/tasks).
 *
 * TODO:
 *  - listTasks(limit?, offset?): GET /api/v1/tasks
 *  - getTask(id): GET /api/v1/tasks/{id}
 *  - createTask(data): POST /api/v1/tasks
 *  - updateTask(id, data): PUT /api/v1/tasks/{id}
 *  - deleteTask(id): DELETE /api/v1/tasks/{id}
 */

import { apiClient } from '../utils/apiClient';
import type { TaskRead, TaskCreate, TaskUpdate } from '../types';

export async function listTasks(limit?: number, offset?: number): Promise<TaskRead[]> {
  // TODO: implement API call
  return [];
}

export async function getTask(id: string): Promise<TaskRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function createTask(data: TaskCreate): Promise<TaskRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function updateTask(id: string, data: TaskUpdate): Promise<TaskRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function deleteTask(id: string): Promise<void> {
  // TODO: implement API call
  throw new Error('Not implemented');
}
