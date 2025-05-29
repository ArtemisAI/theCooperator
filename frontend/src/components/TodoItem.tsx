import React from 'react';
import { ListItem, ListItemText, Checkbox, IconButton, Paper } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { TodoRead } from '@api/todos'; // Assuming TodoRead will be defined in todos.ts or a types file

interface TodoItemProps {
  todo: TodoRead;
  onToggleComplete: (id: number, completed: boolean) => void;
  onDelete: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggleComplete, onDelete }) => {
  return (
    <Paper elevation={1} sx={{ mb: 1, '&:last-child': { mb: 0 } }}>
      <ListItem
        secondaryAction={
          <IconButton edge="end" aria-label="delete" onClick={() => onDelete(todo.id)} color="error">
            <DeleteIcon />
          </IconButton>
        }
        sx={{
          p: 1.5, // Add some padding inside the Paper
          transition: 'background-color 0.3s',
          '&:hover': {
            backgroundColor: 'action.hover',
          },
        }}
      >
        <Checkbox
          edge="start"
          checked={todo.completed}
          tabIndex={-1}
          disableRipple
          inputProps={{ 'aria-labelledby': `checkbox-list-label-${todo.id}` }}
          onClick={() => onToggleComplete(todo.id, !todo.completed)}
          color={todo.completed ? "success" : "primary"}
        />
        <ListItemText
          id={`checkbox-list-label-${todo.id}`}
          primary={todo.title}
          sx={{ 
            textDecoration: todo.completed ? 'line-through' : 'none',
            color: todo.completed ? 'text.secondary' : 'text.primary',
            wordBreak: 'break-word', // Ensure long titles wrap
          }}
        />
      </ListItem>
    </Paper>
  );
};

export default TodoItem;
