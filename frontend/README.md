# Frontend (React - Vite - TypeScript)

This directory contains the frontend application for "TheCooperator" project, built with React, Vite, TypeScript, and Material-UI.

## Quick Start

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application should then be accessible at `http://localhost:5173` (or another port if 5173 is busy). Ensure the backend is running and reachable at `http://localhost:8000`.

## Features

### 1. Members Management
   - **Purpose:** Allows for the management of user accounts.
   - **Functionality:**
     - View a list of existing members (users).
     - Add new members by providing an email, full name, password, and role.
     - Edit existing members' full name and role.
     - Delete members from the system (with a confirmation dialog).
   - **Technical Implementation:**
     - Uses React Query for server state management, including fetching, creating, updating, and deleting members.
     - Provides user feedback through loading indicators, error messages, and success notifications (via Snackbars).

### 2. Todo List
   - **Purpose:** A simple task management feature to keep track of personal todos.
   - **Functionality:**
     - View a list of todo items.
     - Add new todos with a title.
     - Mark todos as completed or incomplete by toggling a checkbox.
     - Delete todos from the list.
   - **Technical Implementation:**
     - Uses React Query for managing the todo list state, interacting with the backend API.
     - UI built with Material-UI components.

## UI/UX Improvements

-   **Custom Material-UI Theme:** A custom theme (`src/theme.ts`) has been implemented to provide a consistent and modern look and feel across the application. This includes a defined color palette, typography settings, and some component style overrides.
-   **Enhanced User Feedback:**
    - **Loading States:** `CircularProgress` indicators are used during data fetching and mutation operations (e.g., adding, updating, deleting items).
    - **Error Messages:** `Alert` components and `Snackbar` notifications are used to inform users of errors during API interactions or other operations.
    - **Success Notifications:** `Snackbar` messages confirm successful operations like creating, updating, or deleting data.
-   **Improved Navigation:** The main application layout includes a sticky `AppBar` with clear navigation links that highlight the active page.
-   **Consistent Styling:** Material-UI components are used throughout for a cohesive user experience.

## Testing

-   **Frameworks:** The project uses [Vitest](https://vitest.dev/) as the test runner and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for writing unit and integration tests for React components.
-   **Setup:**
    - Test utilities and global mocks are configured in `src/vitest.setup.ts` (e.g., `jest-dom` matchers, browser API mocks).
    - Tests are co-located with components in `__tests__` subdirectories (e.g., `src/components/__tests__/MyComponent.test.tsx`).
-   **Running Tests:**
    ```bash
    npm test
    ```
    To run tests with the Vitest UI:
    ```bash
    npm test:ui
    ```

## Project Structure

The frontend application follows a standard Vite + React project structure:

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── api/                # API client and service functions (e.g., users.ts, todos.ts)
│   ├── assets/             # Static assets like images, fonts (if any, currently minimal)
│   ├── components/         # Reusable UI components (e.g., TodoItem.tsx, ErrorBoundary.tsx)
│   │   └── __tests__/      # Unit tests for components
│   ├── context/            # React context providers (e.g., AuthContext.tsx)
│   ├── hooks/              # Custom React hooks (e.g., useAuth.ts)
│   ├── pages/              # Route-level view components (e.g., Members.tsx, TodoPage.tsx)
│   │   └── __tests__/      # Unit tests for page components
│   ├── theme.ts            # Custom Material-UI theme definition
│   ├── types.ts            # Global TypeScript type definitions (can be extended by feature-specific types)
│   ├── utils/              # Utility functions (e.g., apiClient.ts, logger.ts)
│   ├── App.tsx             # Root application component, sets up routing
│   ├── main.tsx            # Main entry point, renders App and sets up providers (Theme, QueryClient)
│   └── vitest.setup.ts     # Vitest setup file for global test configurations
├── .eslintrc.js            # ESLint configuration
├── .gitignore              # Git ignore rules
├── .prettierrc.js          # Prettier configuration
├── index.html              # Main HTML entry point for Vite
├── package.json            # Project dependencies and scripts
├── tsconfig.json           # TypeScript configuration for the project
├── tsconfig.node.json      # TypeScript configuration for Node.js specific parts (e.g., Vite config)
└── vite.config.ts          # Vite configuration (build, dev server, aliases, Vitest)
```

## Key Technologies

-   **React:** JavaScript library for building user interfaces.
-   **Vite:** Fast build tool and development server.
-   **TypeScript:** Typed superset of JavaScript.
-   **Material-UI (MUI):** React UI component library.
-   **React Query:** Server state management library for fetching, caching, and updating data.
-   **React Router DOM:** For client-side routing.
-   **ESLint & Prettier:** For code linting and formatting.
-   **Vitest & React Testing Library:** For unit and component testing.
-   **Axios:** Promise-based HTTP client (used within `apiClient.ts`).

## Contributing

Please ensure your code adheres to the linting and formatting rules by running `npm run lint` and `npm run format` before committing. Write tests for new features and components.
