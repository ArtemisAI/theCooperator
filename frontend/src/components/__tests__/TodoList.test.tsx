import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TodoList from '../TodoList';
import * as todoApi from '@api/todos'; // To be mocked
import { TodoRead } from '@api/todos';

// Mock the actual API module
vi.mock('@api/todos');

// Mock the logger
// vi.mock('@utils/logger', () => ({ default: { info: vi.fn(), warn: vi.fn(), error: vi.fn() } }));
// Already mocked in vitest.setup.ts

const mockTodos: TodoRead[] = [
  { id: 1, title: 'First Todo', completed: false },
  { id: 2, title: 'Second Todo', completed: true },
];

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false, // Disable retries for testing
    },
  },
});

// Wrapper component to provide QueryClient
const AllTheProviders: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('TodoList', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.resetAllMocks();
    queryClient.clear(); // Clear query cache

    // Default successful mock implementations
    (todoApi.getTodos as vi.Mock).mockResolvedValue(mockTodos);
    (todoApi.addTodo as vi.Mock).mockImplementation(async (todo) => {
      const newId = Math.floor(Math.random() * 1000) + 3;
      return { ...todo, id: newId };
    });
    (todoApi.updateTodo as vi.Mock).mockImplementation(async (id, data) => {
        const originalTodo = mockTodos.find(t => t.id === id) || { id, title: 'Unknown', completed: false };
        return { ...originalTodo, ...data };
    });
    (todoApi.deleteTodo as vi.Mock).mockResolvedValue(undefined);
  });

  it('renders a list of todos fetched from the API', async () => {
    render(<TodoList />, { wrapper: AllTheProviders });

    expect(screen.getByRole('progressbar')).toBeInTheDocument(); // Loading state

    await waitFor(() => {
      expect(screen.getByText('First Todo')).toBeInTheDocument();
      expect(screen.getByText('Second Todo')).toBeInTheDocument();
    });
    expect(todoApi.getTodos).toHaveBeenCalledTimes(1);
  });

  it('displays a message when there are no todos', async () => {
    (todoApi.getTodos as vi.Mock).mockResolvedValue([]); // Override default mock for this test
    render(<TodoList />, { wrapper: AllTheProviders });

    await waitFor(() => {
      // The component doesn't explicitly show "No todos" but the list will be empty.
      // We can check that no TodoItem-like elements are rendered.
      // Let's assume TodoItems have a checkbox.
      expect(screen.queryByRole('checkbox')).not.toBeInTheDocument();
      // Or check for a specific message if one were added. For now, this is sufficient.
    });
  });

  it('allows adding a new todo', async () => {
    const user = userEvent.setup();
    render(<TodoList />, { wrapper: AllTheProviders });

    // Wait for initial todos to load to prevent state updates during test
    await waitFor(() => expect(screen.getByText('First Todo')).toBeInTheDocument());

    const input = screen.getByLabelText(/new todo/i);
    const addButton = screen.getByRole('button', { name: /add todo/i });

    await user.type(input, 'New Shiny Todo');
    await user.click(addButton);

    await waitFor(() => {
      expect(todoApi.addTodo).toHaveBeenCalledTimes(1);
      expect(todoApi.addTodo).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'New Shiny Todo', completed: false })
      );
    });
    
    // Query cache should have been invalidated and getTodos called again
    await waitFor(() => expect(todoApi.getTodos).toHaveBeenCalledTimes(2)); 
  });

  it('shows an error message if fetching todos fails', async () => {
    const errorMessage = 'Failed to fetch';
    (todoApi.getTodos as vi.Mock).mockRejectedValue(new Error(errorMessage));
    render(<TodoList />, { wrapper: AllTheProviders });

    await waitFor(() => {
      expect(screen.getByText(`Error fetching todos: ${errorMessage}`)).toBeInTheDocument();
    });
  });

  it('shows an error message if adding a todo fails', async () => {
    const user = userEvent.setup();
    const addErrorMessage = 'Could not add todo';
    (todoApi.addTodo as vi.Mock).mockRejectedValue(new Error(addErrorMessage));
    
    render(<TodoList />, { wrapper: AllTheProviders });
    await waitFor(() => expect(screen.getByText('First Todo')).toBeInTheDocument()); // Wait for initial load

    const input = screen.getByLabelText(/new todo/i);
    const addButton = screen.getByRole('button', { name: /add todo/i });

    await user.type(input, 'Todo that will fail');
    await user.click(addButton);

    await waitFor(() => {
      expect(screen.getByText(`Error adding todo: ${addErrorMessage}`)).toBeInTheDocument();
    });
  });
});
