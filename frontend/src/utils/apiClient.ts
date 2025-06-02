/**
 * Central API client.
 *
 * - Configures base URL for API requests.
 * - Automatically injects authentication token into headers.
 * - Handles response parsing and error handling.
 *
 * TODO:
 *  - Implement with fetch or axios instance.
 *  - Add request/response interceptors for auth.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function apiClient(input: RequestInfo, init?: RequestInit) {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init?.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const response = await fetch(`${API_BASE_URL}${input}`, {
    ...init,
    headers,
  });
  if (!response.ok) {
    // TODO: add unified error handling
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
