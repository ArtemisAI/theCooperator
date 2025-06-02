import React from 'react';
import TodoList from '@components/TodoList'; // Using path alias
import { Container } from '@mui/material';

const TodoPage: React.FC = () => {
  return (
    <Container maxWidth="md">
      <TodoList />
    </Container>
  );
};

export default TodoPage;
