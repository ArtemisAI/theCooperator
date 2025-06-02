import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, CssBaseline } from '@mui/material';
import App from './App';
import ErrorBoundary from '@components/ErrorBoundary'; // Using path alias
import logger from '@utils/logger'; // Using path alias
import theme from './theme'; // Import the custom theme

/**
 * Application entry point.
 *
 * - Mounts the App component into the DOM.
 * - Initializes React Query's QueryClient.
 * - Wraps App with necessary providers (QueryClientProvider, AuthContextProvider, ThemeProvider, ErrorBoundary).
 *
 * TODO:
 *  - Configure AuthContextProvider.
 */

logger.info('Application starting...'); // Demonstrate logger usage

const queryClient = new QueryClient();

const rootElement = document.getElementById('root');
if (!rootElement) {
  logger.error('Failed to find the root element'); // Demonstrate logger usage
  throw new Error('Failed to find the root element');
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Adds normalize.css type of behavior */}
      <ErrorBoundary>
        <QueryClientProvider client={queryClient}>
          {/* TODO: Wrap with AuthContextProvider */}
          <App />
        </QueryClientProvider>
      </ErrorBoundary>
    </ThemeProvider>
  </React.StrictMode>,
);
