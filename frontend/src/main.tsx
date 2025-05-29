import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

/**
 * Application entry point.
 *
 * - Mounts the App component into the DOM.
 * - Initializes React Query's QueryClient.
 * - Wraps App with necessary providers (QueryClientProvider, AuthContextProvider, ThemeProvider).
 *
 * TODO:
 *  - Create and configure QueryClient.
 *  - Import global styles and MUI theme.
 */

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Failed to find the root element');
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    {/* TODO: Wrap with QueryClientProvider, AuthContextProvider, ThemeProvider */}
    <App />
  </React.StrictMode>,
);
