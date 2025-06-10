import { render, screen, waitFor, cleanup } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { KanbanBoard, type Task } from '../src/KanbanBoard';

const mockTasks: Task[] = [
  { id: 1, title: 'Task A', status: 'todo', priority: 'high' },
  { id: 2, title: 'Task B', status: 'done', priority: 'low' },
];

describe('KanbanBoard', () => {
  beforeEach(() => {
    // Mock the global fetch function
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTasks),
      })
    ) as vi.Mock;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    cleanup();
  });

  it('fetches and renders lanes and tasks', async () => {
    render(<KanbanBoard />);

    // Verify fetch was called
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('/tasks/');

    // Wait for tasks to be rendered
    // Check for a lane
    expect(await screen.findByTestId('lane-todo')).toBeTruthy();

    // Check for a specific task
    const taskElement = await screen.findByTestId('task-1');
    expect(taskElement).toBeTruthy();
    expect(taskElement.textContent).toBe('Task A');

    // Optionally, check for another task in a different lane
    const taskElement2 = await screen.findByTestId('task-2');
    expect(taskElement2).toBeTruthy();
    expect(taskElement2.textContent).toBe('Task B');
    expect(screen.getByTestId('lane-done')).toBeTruthy();
  });

  it('displays an error message if fetching initial tasks fails', async () => {
    // Override the default fetch mock for this test
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ message: 'Internal Server Error' }),
      })
    ) as vi.Mock;

    render(<KanbanBoard />);

    // Verify fetch was called for initial tasks
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('/tasks/');

    // Check for the error message
    // The error message in KanbanBoard is `Failed to load tasks. Server responded with ${response.status}.`
    const errorMessage = await screen.findByText(/Failed to load tasks. Server responded with 500/i);
    expect(errorMessage).toBeTruthy();

    // Ensure no tasks are rendered
    expect(screen.queryByTestId('task-1')).toBeNull();
  });

  describe('handleDragEnd functionality', () => {
    const initialTestTasks: Task[] = [
      { id: 1, title: 'Task 1 (Todo)', status: 'todo', priority: 'P1' },
      { id: 2, title: 'Task 2 (In Progress)', status: 'in_progress', priority: 'P2' },
      { id: 3, title: 'Task 3 (Done)', status: 'done', priority: 'P3' },
    ];

    beforeEach(() => {
      // Default mock for GET /tasks/
      global.fetch = vi.fn((url) => {
        if (url === '/tasks/') {
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve([...initialTestTasks]), // Use a fresh copy
          });
        }
        // This will be overridden by specific PUT mocks in tests
        return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      }) as vi.Mock;
    });

    it('successfully updates task status and UI on drag to a new lane', async () => {
      // Mock PUT request to be successful
      global.fetch = vi.fn(async (url, options) => {
        if (url === '/tasks/') {
          return Promise.resolve({ ok: true, json: () => Promise.resolve([...initialTestTasks]) });
        }
        if (options?.method === 'PUT' && url === '/tasks/1') {
          // eslint-disable-next-line @typescript-eslint/no-unsafe-return
          const body = JSON.parse(options.body as string);
          // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
          expect(body.status).toBe('in_progress');
          return Promise.resolve({ ok: true, json: () => Promise.resolve(body) });
        }
        return Promise.resolve({ ok: false, status: 404 }); // Should not happen
      }) as vi.Mock;

      render(<KanbanBoard />);

      // Wait for initial tasks to load
      expect(await screen.findByText('Task 1 (Todo)')).toBeTruthy();
      // Ensure task 1 is initially in 'todo' lane
      let laneTodo = screen.getByTestId('lane-todo');
      expect(laneTodo.textContent).toContain('Task 1 (Todo)');

      // Trigger the drag end simulation via the test button
      const triggerButton = screen.getByTestId('test-drag-end-trigger');
      triggerButton.click(); // This simulates dragging task 1 to 'in_progress'

      // Verify PUT call
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          '/tasks/1',
          expect.objectContaining({ method: 'PUT' })
        );
      });

      const putCall = (fetch as vi.Mock).mock.calls.find(
        c => c[0] === '/tasks/1'
      ) as [string, RequestInit];
      expect(putCall).toBeTruthy();
      const options = putCall[1];
      expect(JSON.parse(options.body as string)).toEqual(
        expect.objectContaining({
          title: 'Task 1 (Todo)',
          status: 'in_progress',
          priority: 'P1',
        })
      );

      // Verify UI update (optimistic)
      // Task 1 should move to 'in_progress' lane
      const laneInProgress = await screen.findByTestId('lane-in_progress');
      await waitFor(() => {
        expect(laneInProgress.textContent).toContain('Task 1 (Todo)');
      });
      // And removed from 'todo'
      laneTodo = screen.getByTestId('lane-todo'); // re-fetch lane-todo
      await waitFor(() => {
         expect(laneTodo.textContent).not.toContain('Task 1 (Todo)');
      });

      // No error message should be shown
      expect(screen.queryByText(/Error:/i)).toBeNull();
    });

    it('rolls back UI and shows error if updating task status fails', async () => {
      // Mock PUT request to fail
       global.fetch = vi.fn(async (url, options) => {
        if (url === '/tasks/') {
          return Promise.resolve({ ok: true, json: () => Promise.resolve([...initialTestTasks]) });
        }
        if (options?.method === 'PUT' && url === '/tasks/1') {
          return Promise.resolve({ ok: false, status: 500, statusText: 'Server Error' });
        }
        return Promise.resolve({ ok: false, status: 404 });
      }) as vi.Mock;

      render(<KanbanBoard />);
      // Wait for initial tasks to load
      expect(await screen.findByText('Task 1 (Todo)')).toBeTruthy();
      let laneTodo = screen.getByTestId('lane-todo');
      expect(laneTodo.textContent).toContain('Task 1 (Todo)');

      // Trigger the drag end simulation
      const triggerButton = screen.getByTestId('test-drag-end-trigger');
      triggerButton.click();

      // Verify PUT call
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          '/tasks/1',
          expect.objectContaining({ method: 'PUT' })
        );
      });

      const putCall = (fetch as vi.Mock).mock.calls.find(
        c => c[0] === '/tasks/1'
      ) as [string, RequestInit];
      expect(putCall).toBeTruthy();
      const options = putCall[1];
      expect(JSON.parse(options.body as string)).toEqual(
        expect.objectContaining({ status: 'in_progress' })
      );

      // Verify UI rollback: Task 1 should still be in 'todo' lane
      laneTodo = screen.getByTestId('lane-todo'); // Re-fetch after potential optimistic update and rollback
      await waitFor(() => {
        expect(laneTodo.textContent).toContain('Task 1 (Todo)');
      });
      const laneInProgress = screen.getByTestId('lane-in_progress');
      expect(laneInProgress.textContent).not.toContain('Task 1 (Todo)');

      // Verify error message is shown
      // The component displays the error message returned from the API
      expect(await screen.findByText(/API error: 500/i)).toBeTruthy();
    });
  });
});
