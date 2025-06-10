import React from 'react';
import ReactDOM from 'react-dom/client';
import { TasksPage } from './TasksPage';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <TasksPage />
  </React.StrictMode>
);
