import React from 'react';
import { Box, Paper, Typography, Grid, Card, CardContent, CardActions, Button, IconButton } from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import type { Task, TaskStatus } from '@src/types'; // Assuming alias

interface KanbanBoardProps {
  tasks: Task[];
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: string) => void;
}

// Define the order of columns
const columnOrder: TaskStatus[] = ['todo', 'in_progress', 'done'];

// Helper to get a display name for status
const getStatusDisplayName = (status: TaskStatus): string => {
  switch (status) {
    case 'todo':
      return 'To Do';
    case 'in_progress':
      return 'In Progress';
    case 'done':
      return 'Done';
    default:
      return status;
  }
};

export function KanbanBoard({ tasks, onEditTask, onDeleteTask }: KanbanBoardProps) {
  // Group tasks by status
  const columns = tasks.reduce((acc, task) => {
    const statusKey = task.status as TaskStatus; // Ensure status is one of the keys
    if (!acc[statusKey]) {
      acc[statusKey] = [];
    }
    acc[statusKey].push(task);
    return acc;
  }, {} as Record<TaskStatus, Task[]>);

  // Ensure all defined columns appear, even if empty
  columnOrder.forEach(status => {
    if (!columns[status]) {
      columns[status] = [];
    }
  });


  return (
    <Grid container spacing={2} sx={{ p: 1 }}>
      {columnOrder.map((status) => (
        <Grid item xs={12} sm={6} md={4} key={status}>
          <Paper elevation={2} sx={{ p: 2, backgroundColor: 'grey.100', height: '100%' }}>
            <Typography variant="h6" component="div" sx={{ mb: 2, textAlign: 'center', color: 'primary.main' }}>
              {getStatusDisplayName(status)} ({columns[status]?.length || 0})
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {columns[status]?.length > 0 ? (
                columns[status].map((task) => (
                  <Card key={task.id} variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" component="div" sx={{ fontWeight: 'bold' }}>
                        {task.title}
                      </Typography>
                      {task.description && (
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1, whiteSpace: 'pre-line' }}>
                          {task.description}
                        </Typography>
                      )}
                       {task.assignee_id && (
                        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                          Assignee: {task.assignee_id.substring(0,8)}...
                        </Typography> // Displaying part of assignee_id
                      )}
                    </CardContent>
                    <CardActions sx={{ justifyContent: 'flex-end' }}>
                      <IconButton size="small" onClick={() => onEditTask(task)} color="primary">
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton size="small" onClick={() => onDeleteTask(task.id)} color="error">
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </CardActions>
                  </Card>
                ))
              ) : (
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
                  No tasks in this column.
                </Typography>
              )}
            </Box>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}
