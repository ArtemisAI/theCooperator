import React, { createContext, useContext } from 'react';
import { useAuth } from '../hooks/useAuth';

/**
 * AuthContext
 *
 * - Provides authentication context (user, login, logout) to the application.
 * - Wrap the App component with AuthContextProvider.
 *
 * TODO:
 *  - Implement context state and effects for token refresh.
 */

const AuthContext = createContext<ReturnType<typeof useAuth> | null>(null);

export function AuthContextProvider({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within AuthContextProvider');
  }
  return context;
}
