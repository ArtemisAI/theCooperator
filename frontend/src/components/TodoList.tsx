import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { List, TextField, Button, Box, Typography, CircularProgress, Alert } from '@mui/material';
import TodoItem from './TodoItem';
import * as todoApi from '@api/todos'; // Using path alias
import logger from '@utils/logger';

const TodoList: React.FC = () => {
  const queryClient = useQueryClient();
  const [newTodoTitle, setNewTodoTitle] = useState('');

  // Fetch Todos
  const { data: todos, isLoading, isError, error } = useQuery<todoApi.TodoRead[], Error>({
    queryKey: ['todos'],
    queryFn: todoApi.getTodos,
  });

  // Add Todo Mutation
  const addTodoMutation = useMutation({
    mutationFn: todoApi.addTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      setNewTodoTitle('');
      logger.info('Todo added successfully');
    },
    onError: (err) => {
      logger.error('Error adding todo:', err);
    },
  });

  // Update Todo Mutation
  const updateTodoMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: todoApi.TodoUpdate }) => todoApi.updateTodo(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      logger.info('Todo updated successfully');
    },
    onError: (err) => {
      logger.error('Error updating todo:', err);
    },
  });

  // Delete Todo Mutation
  const deleteTodoMutation = useMutation({
    mutationFn: todoApi.deleteTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      logger.info('Todo deleted successfully');
    },
    onError: (err) => {
      logger.error('Error deleting todo:', err);
    },
  });

  const handleAddTodo = () => {
    if (newTodoTitle.trim() === '') return;
    addTodoMutation.mutate({ title: newTodoTitle, completed: false });
  };

  const handleToggleComplete = (id: number, completed: boolean) => {
    updateTodoMutation.mutate({ id, data: { completed } });
  };

  const handleDelete = (id: number) => {
    deleteTodoMutation.mutate(id);
  };

  if (isLoading) return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 4 }} />;
  if (isError) return <Alert severity="error" sx={{ mt: 4 }}>Error fetching todos: {error?.message}</Alert>;

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Todo List (React Query)
      </Typography>
      <Box sx={{ display: 'flex', mb: 2 }}>
        <TextField
          label="New Todo"
          variant="outlined"
          fullWidth
          value={newTodoTitle}
          onChange={(e) => setNewTodoTitle(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAddTodo()}
          disabled={addTodoMutation.isLoading}
        />
        <Button
          variant="contained"
          onClick={handleAddTodo}
          sx={{ ml: 1, whiteSpace: 'nowrap' }}
          disabled={addTodoMutation.isLoading}
        >
          {addTodoMutation.isLoading ? <CircularProgress size={24} /> : 'Add Todo'}
        </Button>
      </Box>
      {addTodoMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Error adding todo: {addTodoMutation.error instanceof Error ? addTodoMutation.error.message : 'Unknown error'}
        </Alert>
      )}
      <List>
        {todos?.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggleComplete={handleToggleComplete}
            onDelete={handleDelete}
          />
        ))}
      </List>
    </Box>
  );
};

export default TodoList;
