import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ErrorBoundary from '../ErrorBoundary';
import logger from '@utils/logger'; // Actual logger to spy on

// Mock the logger that is imported by ErrorBoundary.tsx
// This allows us to spy on its methods.
vi.mock('@utils/logger');

// Test component that throws an error
const ProblemChild: React.FC<{ shouldThrow?: boolean }> = ({ shouldThrow }) => {
  if (shouldThrow) {
    throw new Error('Test error from ProblemChild');
  }
  return <div>Everything is fine</div>;
};

describe('ErrorBoundary', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.resetAllMocks();
    // Restore console.error if it was spied on and suppressed
    // vitest automatically mocks console.error when an error is thrown in a component
    // to prevent polluting test output, so we don't need to manually mock/restore it here
    // for the purpose of checking if ErrorBoundary logs the error.
  });

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <ProblemChild />
      </ErrorBoundary>
    );
    expect(screen.getByText('Everything is fine')).toBeInTheDocument();
  });

  it('renders fallback UI when a child component throws an error', () => {
    // Suppress console.error output for this specific test because we expect an error
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    render(
      <ErrorBoundary>
        <ProblemChild shouldThrow />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something went wrong.')).toBeInTheDocument();
    // Check if the error message from the thrown error is visible (optional, depends on your fallback UI)
    expect(screen.getByText(/Test error from ProblemChild/)).toBeInTheDocument();
    
    consoleErrorSpy.mockRestore();
  });

  it('logs the error when a child component throws an error', () => {
    // Suppress console.error output for this specific test
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(
      <ErrorBoundary>
        <ProblemChild shouldThrow />
      </ErrorBoundary>
    );

    // Verify that our mocked logger was called by ErrorBoundary's componentDidCatch
    expect(logger.error).toHaveBeenCalledTimes(1);
    expect(logger.error).toHaveBeenCalledWith(
      'Uncaught error:',
      expect.any(Error), // The error object
      expect.objectContaining({ componentStack: expect.any(String) }) // The errorInfo object
    );
    
    consoleErrorSpy.mockRestore();
  });

  it('does not render fallback UI if no error is thrown', () => {
    render(
      <ErrorBoundary>
        <ProblemChild />
      </ErrorBoundary>
    );
    expect(screen.queryByText('Something went wrong.')).not.toBeInTheDocument();
  });
});
