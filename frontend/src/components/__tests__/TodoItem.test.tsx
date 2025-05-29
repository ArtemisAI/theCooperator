import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import TodoItem from '../TodoItem';
import { TodoRead } from '@api/todos'; // Adjust path as necessary

// Mock the logger used in the component if it's directly imported and used
// vi.mock('@utils/logger', () => ({ default: { info: vi.fn(), warn: vi.fn(), error: vi.fn() } }));
// Already mocked in vitest.setup.ts

const mockTodo: TodoRead = {
  id: 1,
  title: 'Test Todo Item',
  completed: false,
};

const mockCompletedTodo: TodoRead = {
  id: 2,
  title: 'Completed Test Todo',
  completed: true,
};

describe('TodoItem', () => {
  it('renders the todo title', () => {
    render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={vi.fn()}
        onDelete={vi.fn()}
      />
    );
    expect(screen.getByText('Test Todo Item')).toBeInTheDocument();
  });

  it('checkbox reflects the completed status (unchecked)', () => {
    render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={vi.fn()}
        onDelete={vi.fn()}
      />
    );
    const checkbox = screen.getByRole('checkbox') as HTMLInputElement;
    expect(checkbox.checked).toBe(false);
  });

  it('checkbox reflects the completed status (checked)', () => {
    render(
      <TodoItem
        todo={mockCompletedTodo}
        onToggleComplete={vi.fn()}
        onDelete={vi.fn()}
      />
    );
    const checkbox = screen.getByRole('checkbox') as HTMLInputElement;
    expect(checkbox.checked).toBe(true);
  });

  it('calls onToggleComplete when the checkbox is clicked', async () => {
    const handleToggleComplete = vi.fn();
    render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={handleToggleComplete}
        onDelete={vi.fn()}
      />
    );
    const checkbox = screen.getByRole('checkbox');
    await userEvent.click(checkbox);
    expect(handleToggleComplete).toHaveBeenCalledTimes(1);
    expect(handleToggleComplete).toHaveBeenCalledWith(mockTodo.id, !mockTodo.completed);
  });

  it('calls onDelete when the delete button is clicked', async () => {
    const handleDelete = vi.fn();
    render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={vi.fn()}
        onDelete={handleDelete}
      />
    );
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await userEvent.click(deleteButton);
    expect(handleDelete).toHaveBeenCalledTimes(1);
    expect(handleDelete).toHaveBeenCalledWith(mockTodo.id);
  });

  it('applies line-through style to completed items', () => {
    render(
      <TodoItem
        todo={mockCompletedTodo}
        onToggleComplete={vi.fn()}
        onDelete={vi.fn()}
      />
    );
    const listItemText = screen.getByText(mockCompletedTodo.title);
    // Check for sx prop style or inline style
    // sx={{ textDecoration: todo.completed ? 'line-through' : 'none', ... }}
    // The style is applied via sx prop which results in a class usually.
    // A more robust way is to check computed style if MUI applies it directly or via a class.
    // However, MUI might use classes that are not easily predictable.
    // Let's check if the style attribute contains 'line-through'.
    // Note: sx prop might generate classes, so this check can be brittle.
    // A better way if using styled-components or emotion directly would be to check for the specific class.
    // For MUI with sx, it's often simpler to trust MUI applies styles correctly if props are right.
    // For this test, we'll assume the style attribute is directly affected or a specific class is known.
    // The component uses: sx={{ textDecoration: todo.completed ? 'line-through' : 'none', ... }}
    // This will result in an inline style or a generated class.
    // Let's inspect the element's style directly.
    expect(listItemText).toHaveStyle('text-decoration: line-through');
  });

  it('does not apply line-through style to incomplete items', () => {
    render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={vi.fn()}
        onDelete={vi.fn()}
      />
    );
    const listItemText = screen.getByText(mockTodo.title);
    expect(listItemText).not.toHaveStyle('text-decoration: line-through');
  });
});
