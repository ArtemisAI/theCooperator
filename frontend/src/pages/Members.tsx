import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Container,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Box,
  CircularProgress,
  Alert,
  Paper,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Snackbar,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import * as userApi from '@api/users'; // Using path alias
import logger from '@utils/logger';

const MembersPage: React.FC = () => {
  const queryClient = useQueryClient();

  // Form state for creating/editing
  const [formValues, setFormValues] = useState<userApi.UserCreate>({
    email: '',
    full_name: '',
    password_DO_NOT_SEND_BACK: '', // Special handling for password
    role: userApi.UserRole.resident,
  });
  const [isEditMode, setIsEditMode] = useState(false);
  const [editingUserId, setEditingUserId] = useState<string | null>(null);

  // Dialog state
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [userToDelete, setUserToDelete] = useState<userApi.UserRead | null>(null);
  
  // Snackbar state
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Fetch Users Query
  const { data: users, isLoading, isError, error: fetchError } = useQuery<userApi.UserRead[], Error>({
    queryKey: ['users'],
    queryFn: () => userApi.getUsers(),
  });

  // Create User Mutation
  const createUserMutation = useMutation({
    mutationFn: userApi.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      resetForm();
      setSnackbarMessage('Member created successfully!');
      setSnackbarOpen(true);
      logger.info('User created successfully');
    },
    onError: (err: any) => {
      logger.error('Error creating user:', err);
      setSnackbarMessage(err.response?.data?.detail || 'Error creating member.');
      setSnackbarOpen(true);
    },
  });

  // Update User Mutation
  const updateUserMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: userApi.UserUpdate }) => userApi.updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      resetForm();
      setSnackbarMessage('Member updated successfully!');
      setSnackbarOpen(true);
      logger.info('User updated successfully');
    },
    onError: (err: any) => {
      logger.error('Error updating user:', err);
      setSnackbarMessage(err.response?.data?.detail || 'Error updating member.');
      setSnackbarOpen(true);
    },
  });

  // Delete User Mutation
  const deleteUserMutation = useMutation({
    mutationFn: userApi.deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setOpenDeleteDialog(false);
      setUserToDelete(null);
      setSnackbarMessage('Member deleted successfully!');
      setSnackbarOpen(true);
      logger.info('User deleted successfully');
    },
    onError: (err: any) => {
      logger.error('Error deleting user:', err);
      setSnackbarMessage(err.response?.data?.detail || 'Error deleting member.');
      setSnackbarOpen(true);
      setOpenDeleteDialog(false);
    },
  });

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = event.target;
    setFormValues((prev) => ({ ...prev, [name as string]: value }));
  };
  
  const handleRoleChange = (event: React.ChangeEvent<{ name?: string; value: unknown }>) => {
    setFormValues((prev) => ({ ...prev, role: event.target.value as userApi.UserRole }));
  };


  const resetForm = () => {
    setFormValues({
      email: '',
      full_name: '',
      password_DO_NOT_SEND_BACK: '',
      role: userApi.UserRole.resident,
    });
    setIsEditMode(false);
    setEditingUserId(null);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (isEditMode && editingUserId) {
      const { email, password_DO_NOT_SEND_BACK, ...updateData } = formValues; // Exclude email and password from update payload
      updateUserMutation.mutate({ id: editingUserId, data: updateData });
    } else {
      // Ensure password is set from password_DO_NOT_SEND_BACK for creation
      const createPayload: userApi.UserCreate = {
        ...formValues,
        password: formValues.password_DO_NOT_SEND_BACK
      };
      // delete createPayload.password_DO_NOT_SEND_BACK; // Not strictly necessary as API should ignore it
      createUserMutation.mutate(createPayload);
    }
  };

  const handleEdit = (user: userApi.UserRead) => {
    setIsEditMode(true);
    setEditingUserId(user.id);
    setFormValues({
      email: user.email, // Email is not editable on backend via UserUpdate, but shown for context
      full_name: user.full_name || '',
      password_DO_NOT_SEND_BACK: '', // Password field cleared for editing
      role: user.role || userApi.UserRole.resident,
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDeleteClick = (user: userApi.UserRead) => {
    setUserToDelete(user);
    setOpenDeleteDialog(true);
  };

  const handleDeleteConfirm = () => {
    if (userToDelete) {
      deleteUserMutation.mutate(userToDelete.id);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
    setSnackbarMessage('');
  };


  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 3, mt: 2 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {isEditMode ? 'Edit Member' : 'Manage Members'}
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }} noValidate autoComplete="off">
          <TextField
            label="Email"
            name="email"
            type="email"
            variant="outlined"
            fullWidth
            value={formValues.email}
            onChange={handleInputChange}
            disabled={isEditMode} // Email not editable for existing users
            required={!isEditMode}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Full Name"
            name="full_name"
            variant="outlined"
            fullWidth
            value={formValues.full_name || ''}
            onChange={handleInputChange}
            sx={{ mb: 2 }}
          />
          {!isEditMode && ( // Only show password field when creating a new user
            <TextField
              label="Password"
              name="password_DO_NOT_SEND_BACK"
              type="password"
              variant="outlined"
              fullWidth
              value={formValues.password_DO_NOT_SEND_BACK}
              onChange={handleInputChange}
              required
              sx={{ mb: 2 }}
            />
          )}
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel id="role-select-label">Role</InputLabel>
            <Select
              labelId="role-select-label"
              id="role-select"
              name="role"
              value={formValues.role}
              label="Role"
              onChange={handleRoleChange as any} // MUI Select type issue with custom event handler
            >
              {Object.values(userApi.UserRole).map((role) => (
                <MenuItem key={role} value={role}>
                  {role.charAt(0).toUpperCase() + role.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={createUserMutation.isLoading || updateUserMutation.isLoading}
              sx={{ whiteSpace: 'nowrap' }}
            >
              {(createUserMutation.isLoading || updateUserMutation.isLoading) ? (
                <CircularProgress size={24} />
              ) : isEditMode ? (
                'Save Changes'
              ) : (
                'Add Member'
              )}
            </Button>
            {isEditMode && (
              <Button variant="outlined" onClick={resetForm} disabled={updateUserMutation.isLoading}>
                Cancel Edit
              </Button>
            )}
          </Box>
        </Box>

        {isLoading && <CircularProgress sx={{ display: 'block', margin: 'auto', my: 2 }} />}
        {fetchError && <Alert severity="error" sx={{ my: 2 }}>Error fetching members: {fetchError.message}</Alert>}
        
        {!isLoading && !fetchError && users?.length === 0 && (
          <Typography variant="body1" sx={{ my: 2 }}>
            No members found. Add one above!
          </Typography>
        )}

        {!isLoading && !fetchError && users && users.length > 0 && (
          <List>
            {users.map((user) => (
              <ListItem 
                key={user.id} 
                divider 
                sx={{ 
                  backgroundColor: 'background.paper', 
                  mb: 1, 
                  borderRadius: 1,
                  '&:hover': { boxShadow: 3 } 
                }}
              >
                <ListItemText 
                  primary={user.full_name || 'N/A'} 
                  secondary={<>{user.email}<br/>Role: {user.role} - ID: {user.id}</>}
                />
                <ListItemSecondaryAction>
                  <IconButton edge="end" aria-label="edit" onClick={() => handleEdit(user)} color="primary">
                    <EditIcon />
                  </IconButton>
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteClick(user)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={() => setOpenDeleteDialog(false)}
      >
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete member "{userToDelete?.full_name || userToDelete?.email}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)} color="primary" disabled={deleteUserMutation.isLoading}>
            Cancel
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" disabled={deleteUserMutation.isLoading}>
            {deleteUserMutation.isLoading ? <CircularProgress size={24} /> : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for feedback */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
    </Container>
  );
};

export default MembersPage;
