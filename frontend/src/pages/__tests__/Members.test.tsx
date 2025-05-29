import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MembersPage from '../MembersPage';
import * as userApi from '@api/users'; // To be mocked
import { UserRead, UserRole } from '@api/users';

// Mock the actual API module
vi.mock('@api/users');

// Mock the logger
// vi.mock('@utils/logger', () => ({ default: { info: vi.fn(), warn: vi.fn(), error: vi.fn() } }));
// Already mocked in vitest.setup.ts

const mockUsers: UserRead[] = [
  { id: '1', email: 'user1@example.com', full_name: 'User One', role: UserRole.resident },
  { id: '2', email: 'user2@example.com', full_name: 'User Two', role: UserRole.manager },
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

describe('MembersPage', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    queryClient.clear();

    // Default successful mock implementations
    (userApi.getUsers as vi.Mock).mockResolvedValue(mockUsers);
    (userApi.createUser as vi.Mock).mockImplementation(async (userData) => {
      const newId = (Math.random() * 1000).toString();
      return { ...userData, id: newId, full_name: userData.full_name || `New User ${newId}` };
    });
    (userApi.updateUser as vi.Mock).mockImplementation(async (userId, userData) => {
        const originalUser = mockUsers.find(u => u.id === userId) || { id: userId, email: 'unknown@example.com', role: UserRole.resident};
        return { ...originalUser, ...userData, full_name: userData.full_name || originalUser.full_name };
    });
    (userApi.deleteUser as vi.Mock).mockResolvedValue(undefined);
  });

  it('renders a list of members fetched from the API', async () => {
    render(<MembersPage />, { wrapper: AllTheProviders });

    expect(screen.getByRole('progressbar')).toBeInTheDocument(); // Initial loading state

    await waitFor(() => {
      expect(screen.getByText('User One')).toBeInTheDocument();
      expect(screen.getByText('user1@example.com')).toBeInTheDocument();
      expect(screen.getByText('User Two')).toBeInTheDocument();
      expect(screen.getByText('user2@example.com')).toBeInTheDocument();
    });
    expect(userApi.getUsers).toHaveBeenCalledTimes(1);
  });

  it('allows adding a new member', async () => {
    const user = userEvent.setup();
    render(<MembersPage />, { wrapper: AllTheProviders });

    await waitFor(() => expect(screen.getByText('User One')).toBeInTheDocument()); // Wait for initial load

    const emailInput = screen.getByLabelText(/email/i);
    const nameInput = screen.getByLabelText(/full name/i);
    const passwordInput = screen.getByLabelText(/password/i); // Password field is present in create mode
    const roleSelectButton = screen.getByLabelText(/role/i); // The button part of the Select
    const addButton = screen.getByRole('button', { name: /add member/i });

    await user.type(emailInput, 'newmember@example.com');
    await user.type(nameInput, 'New Member Name');
    await user.type(passwordInput, 'password123');
    
    // Open the Select dropdown for Role
    await user.click(roleSelectButton);
    // Select an item from the dropdown (assuming 'Manager' is an option)
    // The actual text might depend on how UserRole enum values are mapped to display names.
    // Here, UserRole.manager is 'manager', so 'Manager' with capital M.
    const managerOption = await screen.findByRole('option', { name: /manager/i });
    await user.click(managerOption);
    
    await user.click(addButton);

    await waitFor(() => {
      expect(userApi.createUser).toHaveBeenCalledTimes(1);
      expect(userApi.createUser).toHaveBeenCalledWith(
        expect.objectContaining({
          email: 'newmember@example.com',
          full_name: 'New Member Name',
          password: 'password123',
          role: UserRole.manager,
        })
      );
    });
    // Check for snackbar success message
    expect(await screen.findByText('Member created successfully!')).toBeInTheDocument();
    // Query cache should have been invalidated and getUsers called again
    await waitFor(() => expect(userApi.getUsers).toHaveBeenCalledTimes(2));
  });

  it('shows an error message if fetching members fails', async () => {
    const errorMessage = 'Failed to fetch members';
    (userApi.getUsers as vi.Mock).mockRejectedValue(new Error(errorMessage));
    render(<MembersPage />, { wrapper: AllTheProviders });

    await waitFor(() => {
      expect(screen.getByText(`Error fetching members: ${errorMessage}`)).toBeInTheDocument();
    });
  });

  it('shows an error message in snackbar if adding a member fails', async () => {
    const user = userEvent.setup();
    const addErrorMessage = 'Could not add member';
    (userApi.createUser as vi.Mock).mockRejectedValue({ response: { data: { detail: addErrorMessage } } });
    
    render(<MembersPage />, { wrapper: AllTheProviders });
    await waitFor(() => expect(screen.getByText('User One')).toBeInTheDocument());

    const emailInput = screen.getByLabelText(/email/i);
    await user.type(emailInput, 'fail@example.com');
    // Fill other required fields if necessary for the form to be submittable
    const passwordInput = screen.getByLabelText(/password/i);
    await user.type(passwordInput, 'password123');

    const addButton = screen.getByRole('button', { name: /add member/i });
    await user.click(addButton);

    await waitFor(() => {
      expect(screen.getByText(addErrorMessage)).toBeInTheDocument(); // Snackbar message
    });
  });

  it('allows editing a member (full name and role)', async () => {
    const user = userEvent.setup();
    render(<MembersPage />, { wrapper: AllTheProviders });
  
    await waitFor(() => expect(screen.getByText('User One')).toBeInTheDocument());
  
    // Find the edit button for the first user
    // The edit button is identified by aria-label="edit"
    const editButtons = screen.getAllByRole('button', { name: /edit/i });
    await user.click(editButtons[0]); // Click edit for "User One"
  
    await waitFor(() => {
      // Form should be populated for editing
      expect(screen.getByLabelText(/email/i)).toBeDisabled(); // Email not editable
      expect(screen.getByLabelText(/email/i)).toHaveValue('user1@example.com');
      expect(screen.getByLabelText(/full name/i)).toHaveValue('User One');
    });
  
    const nameInput = screen.getByLabelText(/full name/i);
    await user.clear(nameInput);
    await user.type(nameInput, 'User One Updated');
  
    const roleSelectButton = screen.getByLabelText(/role/i);
    await user.click(roleSelectButton);
    const adminOption = await screen.findByRole('option', { name: /admin/i });
    await user.click(adminOption);
  
    const saveButton = screen.getByRole('button', { name: /save changes/i });
    await user.click(saveButton);
  
    await waitFor(() => {
      expect(userApi.updateUser).toHaveBeenCalledTimes(1);
      expect(userApi.updateUser).toHaveBeenCalledWith(
        mockUsers[0].id, // user_id '1'
        expect.objectContaining({
          full_name: 'User One Updated',
          role: UserRole.admin,
        })
      );
    });
    expect(await screen.findByText('Member updated successfully!')).toBeInTheDocument();
    await waitFor(() => expect(userApi.getUsers).toHaveBeenCalledTimes(2)); // Refreshed
  });

  it('allows deleting a member', async () => {
    const user = userEvent.setup();
    render(<MembersPage />, { wrapper: AllTheProviders });

    await waitFor(() => expect(screen.getByText('User One')).toBeInTheDocument());

    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    await user.click(deleteButtons[0]); // Click delete for "User One"

    // Confirm dialog
    expect(await screen.findByText('Confirm Deletion')).toBeInTheDocument();
    const confirmDeleteButton = screen.getByRole('button', { name: 'Delete' }); // Inner text of button
    await user.click(confirmDeleteButton);

    await waitFor(() => {
        expect(userApi.deleteUser).toHaveBeenCalledTimes(1);
        expect(userApi.deleteUser).toHaveBeenCalledWith(mockUsers[0].id);
    });
    expect(await screen.findByText('Member deleted successfully!')).toBeInTheDocument();
    await waitFor(() => expect(userApi.getUsers).toHaveBeenCalledTimes(2)); // Refreshed
  });

});
