import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { KanbanBoard } from '../src/KanbanBoard';

const tasks = [
  { id: 1, title: 'A', status: 'todo' },
  { id: 2, title: 'B', status: 'done' }
] as const;

describe('KanbanBoard', () => {
  it('renders lanes and tasks', () => {
    render(<KanbanBoard initialTasks={[...tasks]} />);
    expect(screen.getByTestId('lane-todo')).toBeTruthy();
    expect(screen.getByTestId('task-1').textContent).toBe('A');
  });
});
