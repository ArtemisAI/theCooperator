import React, { useState, useEffect } from 'react';
import { Box, Button, CircularProgress, Alert, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Typography, Container, Paper, Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

import { KanbanBoard } from '@components/KanbanBoard';
import { useTasks, useCreateTask, useUpdateTask, useDeleteTask } from '@api/tasks';
import type { Task, TaskCreate, TaskUpdate, TaskStatus } from '@src/types';
import { UserRead } from '@src/types'; // Assuming UserRead might be useful for assignee selection later
import { getUsers } from '@api/users'; // For assignee dropdown

export default function TasksPage() {
  const { data: tasks, isLoading: isLoadingTasks, isError: isErrorTasks, error: errorTasks } = useTasks();
  const createTaskMutation = useCreateTask();
  const updateTaskMutation = useUpdateTask();
  const deleteTaskMutation = useDeleteTask();

  // Users for assignee dropdown
  const [users, setUsers] = useState<UserRead[]>([]);
  useEffect(() => {
    getUsers().then(setUsers).catch(console.error);
  }, []);


  // Create Task Dialog
  const [createTaskDialogOpen, setCreateTaskDialogOpen] = useState(false);
  const [newTask, setNewTask] = useState<Partial<TaskCreate>>({ title: '', description: '', status: 'todo', assignee_id: '' });

  // Edit Task Dialog
  const [editTaskDialogOpen, setEditTaskDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [updatedTaskData, setUpdatedTaskData] = useState<Partial<TaskUpdate>>({});

  // Delete Task Dialog
  const [deleteTaskConfirmOpen, setDeleteTaskConfirmOpen] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);


  // --- Create Task Handlers ---
  const handleOpenCreateTaskDialog = () => {
    setNewTask({ title: '', description: '', status: 'todo', assignee_id: '' });
    setCreateTaskDialogOpen(true);
  };
  const handleCloseCreateTaskDialog = () => setCreateTaskDialogOpen(false);
  const handleNewTaskChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setNewTask(prev => ({ ...prev, [name]: value }));
  };
   const handleNewTaskStatusChange = (event: SelectChangeEvent<TaskStatus>) => {
    setNewTask(prev => ({ ...prev, status: event.target.value as TaskStatus }));
  };
  const handleNewTaskAssigneeChange = (event: SelectChangeEvent<string | null>) => {
    setNewTask(prev => ({ ...prev, assignee_id: event.target.value === '' ? null : event.target.value }));
  };
  const handleCreateTaskSubmit = async () => {
    if (!newTask.title) {
      alert("Title is required."); return;
    }
    createTaskMutation.mutate(
      {
        title: newTask.title,
        description: newTask.description || undefined,
        status: newTask.status || 'todo',
        assignee_id: newTask.assignee_id || undefined,
      },
      { onSuccess: handleCloseCreateTaskDialog }
    );
  };

  // --- Edit Task Handlers ---
  const handleOpenEditTaskDialog = (task: Task) => {
    setEditingTask(task);
    setUpdatedTaskData({
      title: task.title,
      description: task.description || '',
      status: task.status,
      assignee_id: task.assignee_id || ''
    });
    setEditTaskDialogOpen(true);
  };
  const handleCloseEditTaskDialog = () => setEditTaskDialogOpen(false);
  const handleUpdatedTaskDataChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setUpdatedTaskData(prev => ({ ...prev, [name]: value }));
  };
  const handleUpdatedTaskStatusChange = (event: SelectChangeEvent<TaskStatus>) => {
    setUpdatedTaskData(prev => ({ ...prev, status: event.target.value as TaskStatus }));
  };
  const handleUpdatedTaskAssigneeChange = (event: SelectChangeEvent<string | null>) => {
    setUpdatedTaskData(prev => ({ ...prev, assignee_id: event.target.value === '' ? null : event.target.value }));
  };
  const handleUpdateTaskSubmit = async () => {
    if (!editingTask || !updatedTaskData.title) {
      alert("Title is required."); return;
    }
    // Construct only changed fields for TaskUpdate
    const payload: TaskUpdate = {};
    if (updatedTaskData.title !== editingTask.title) payload.title = updatedTaskData.title;
    if (updatedTaskData.description !== (editingTask.description || '')) payload.description = updatedTaskData.description;
    if (updatedTaskData.status !== editingTask.status) payload.status = updatedTaskData.status;
    if (updatedTaskData.assignee_id !== (editingTask.assignee_id || '')) {
        payload.assignee_id = updatedTaskData.assignee_id === '' ? null : updatedTaskData.assignee_id;
    }

    // Only mutate if there are actual changes
    if (Object.keys(payload).length > 0) {
        updateTaskMutation.mutate(
          { taskId: editingTask.id, taskData: payload },
          { onSuccess: handleCloseEditTaskDialog }
        );
    } else {
        handleCloseEditTaskDialog(); // No changes, just close
    }
  };

  // --- Delete Task Handlers ---
  const handleOpenDeleteConfirmDialog = (taskId: string) => {
    setDeletingTaskId(taskId);
    setDeleteTaskConfirmOpen(true);
  };
  const handleCloseDeleteConfirmDialog = () => setDeleteTaskConfirmOpen(false);
  const handleDeleteTaskConfirm = () => {
    if (deletingTaskId) {
      deleteTaskMutation.mutate(deletingTaskId, {
        onSuccess: handleCloseDeleteConfirmDialog,
        onError: handleCloseDeleteConfirmDialog, // Also close on error for now
      });
    }
  };


  if (isLoadingTasks) return <Container sx={{display: 'flex', justifyContent: 'center', mt: 5}}><CircularProgress /></Container>;
  if (isErrorTasks && errorTasks) return <Container><Alert severity="error">Error fetching tasks: {errorTasks.message}</Alert></Container>;

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}> {/* Changed to xl for wider Kanban */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">Tasks Kanban</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleOpenCreateTaskDialog}>Create Task</Button>
      </Box>

      <Paper elevation={0} sx={{ p: 0, backgroundColor: 'transparent' }}> {/* Changed elevation and padding */}
        <KanbanBoard
          tasks={tasks || []}
          onEditTask={handleOpenEditTaskDialog}
          onDeleteTask={handleOpenDeleteConfirmDialog}
        />
      </Paper>

      {/* Create Task Dialog */}
      <Dialog open={createTaskDialogOpen} onClose={handleCloseCreateTaskDialog} fullWidth maxWidth="sm">
        <DialogTitle>Create New Task</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" name="title" label="Task Title" type="text" fullWidth variant="outlined" value={newTask.title} onChange={handleNewTaskChange} required sx={{ mb: 2, mt:1 }} />
          <TextField margin="dense" name="description" label="Description" type="text" fullWidth multiline rows={3} variant="outlined" value={newTask.description} onChange={handleNewTaskChange} sx={{ mb: 2 }} />
          <FormControl fullWidth margin="dense" sx={{ mb: 2 }}>
            <InputLabel id="create-task-status-label">Status</InputLabel>
            <Select labelId="create-task-status-label" name="status" value={newTask.status || 'todo'} onChange={handleNewTaskStatusChange} label="Status">
              <MenuItem value="todo">To Do</MenuItem><MenuItem value="in_progress">In Progress</MenuItem><MenuItem value="done">Done</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel id="create-task-assignee-label">Assignee</InputLabel>
            <Select labelId="create-task-assignee-label" name="assignee_id" value={newTask.assignee_id || ''} onChange={handleNewTaskAssigneeChange} label="Assignee">
              <MenuItem value=""><em>Unassigned</em></MenuItem>
              {users.map(user => <MenuItem key={user.id} value={user.id}>{user.full_name || user.email}</MenuItem>)}
            </Select>
          </FormControl>
          {createTaskMutation.isError && <Alert severity="error" sx={{ mt: 2 }}>{createTaskMutation.error?.message || "Failed to create task."}</Alert>}
        </DialogContent>
        <DialogActions><Button onClick={handleCloseCreateTaskDialog} disabled={createTaskMutation.isLoading}>Cancel</Button><Button onClick={handleCreateTaskSubmit} variant="contained" disabled={createTaskMutation.isLoading}>{createTaskMutation.isLoading ? <CircularProgress size={24} /> : "Create"}</Button></DialogActions>
      </Dialog>

      {/* Edit Task Dialog */}
      {editingTask && (
      <Dialog open={editTaskDialogOpen} onClose={handleCloseEditTaskDialog} fullWidth maxWidth="sm">
        <DialogTitle>Edit Task: {editingTask.title}</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" name="title" label="Task Title" type="text" fullWidth variant="outlined" value={updatedTaskData.title} onChange={handleUpdatedTaskDataChange} required sx={{ mb: 2, mt:1 }} />
          <TextField margin="dense" name="description" label="Description" type="text" fullWidth multiline rows={3} variant="outlined" value={updatedTaskData.description} onChange={handleUpdatedTaskDataChange} sx={{ mb: 2 }}/>
          <FormControl fullWidth margin="dense" sx={{ mb: 2 }}>
            <InputLabel id="edit-task-status-label">Status</InputLabel>
            <Select labelId="edit-task-status-label" name="status" value={updatedTaskData.status || 'todo'} onChange={handleUpdatedTaskStatusChange} label="Status">
              <MenuItem value="todo">To Do</MenuItem><MenuItem value="in_progress">In Progress</MenuItem><MenuItem value="done">Done</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel id="edit-task-assignee-label">Assignee</InputLabel>
            <Select labelId="edit-task-assignee-label" name="assignee_id" value={updatedTaskData.assignee_id || ''} onChange={handleUpdatedTaskAssigneeChange} label="Assignee">
              <MenuItem value=""><em>Unassigned</em></MenuItem>
              {users.map(user => <MenuItem key={user.id} value={user.id}>{user.full_name || user.email}</MenuItem>)}
            </Select>
          </FormControl>
          {updateTaskMutation.isError && <Alert severity="error" sx={{ mt: 2 }}>{updateTaskMutation.error?.message || "Failed to update task."}</Alert>}
        </DialogContent>
        <DialogActions><Button onClick={handleCloseEditTaskDialog} disabled={updateTaskMutation.isLoading}>Cancel</Button><Button onClick={handleUpdateTaskSubmit} variant="contained" disabled={updateTaskMutation.isLoading}>{updateTaskMutation.isLoading ? <CircularProgress size={24} /> : "Save Changes"}</Button></DialogActions>
      </Dialog>
      )}

      {/* Delete Task Confirmation Dialog */}
      <Dialog open={deleteTaskConfirmOpen} onClose={handleCloseDeleteConfirmDialog}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent><Typography>Are you sure you want to delete this task? This action cannot be undone.</Typography></DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteConfirmDialog} disabled={deleteTaskMutation.isLoading}>Cancel</Button>
          <Button onClick={handleDeleteTaskConfirm} color="error" variant="contained" disabled={deleteTaskMutation.isLoading}>
            {deleteTaskMutation.isLoading ? <CircularProgress size={24} color="inherit"/> : "Delete"}
          </Button>
        </DialogActions>
        {deleteTaskMutation.isError && <Alert severity="error" sx={{m:2}}>{deleteTaskMutation.error?.message || "Failed to delete task."}</Alert>}
      </Dialog>
    </Container>
  );
}
