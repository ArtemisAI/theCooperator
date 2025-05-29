/**
 * Custom hook: useAuth
 *
 * - Manages authentication state (JWT token, current user).
 * - Exposes login, logout, and auth status.
 * - Stores token in localStorage or cookies.
 *
 * TODO:
 *  - Implement login (call /api/v1/auth/login).
 *  - Store and refresh JWT tokens.
 *  - Expose user data and auth methods.
 */

export function useAuth() {
  // Placeholder implementation
  return {
    user: null,
    login: async (email: string, password: string) => {
      // TODO: call auth API and store token
    },
    logout: () => {
      // TODO: clear token and user data
    },
  };
}
