import apiClient from '@utils/apiClient';

// Based on backend/app/schemas/user.py
export enum UserRole {
  resident = 'resident',
  manager = 'manager',
  admin = 'admin',
}

export interface UserBase {
  email: string;
  full_name?: string | null;
  role?: UserRole;
}

export interface UserCreate extends UserBase {
  password_DO_NOT_SEND_BACK?: string; // For form handling, ensure this is not sent if empty
  password?: string; // Actual field for creation
}

export interface UserUpdate {
  full_name?: string | null;
  role?: UserRole;
  // Add other updatable fields if any, e.g., email, password - but current backend UserUpdate is limited
}

export interface UserRead extends UserBase {
  id: string;
  // email: string; // Already in UserBase
  // full_name?: string | null; // Already in UserBase
  // role: UserRole; // Already in UserBase
}

const API_BASE_URL = '/api/v1/users';

export const getUsers = async (limit: number = 100, offset: int = 0): Promise<UserRead[]> => {
  const response = await apiClient.get<UserRead[]>(`${API_BASE_URL}/?limit=${limit}&offset=${offset}`);
  return response.data;
};

export const getUserById = async (userId: string): Promise<UserRead> => {
  const response = await apiClient.get<UserRead>(`${API_BASE_URL}/${userId}`);
  return response.data;
};

export const createUser = async (userData: UserCreate): Promise<UserRead> => {
  // Ensure only 'password' is sent, not 'password_DO_NOT_SEND_BACK'
  const { password_DO_NOT_SEND_BACK, ...payload } = userData;
  if (payload.password === undefined && password_DO_NOT_SEND_BACK) {
      payload.password = password_DO_NOT_SEND_BACK;
  }
  const response = await apiClient.post<UserRead>(API_BASE_URL, payload);
  return response.data;
};

export const updateUser = async (userId: string, userData: UserUpdate): Promise<UserRead> => {
  const response = await apiClient.put<UserRead>(`${API_BASE_URL}/${userId}`, userData);
  return response.data;
};

export const deleteUser = async (userId: string): Promise<void> => {
  await apiClient.delete(`${API_BASE_URL}/${userId}`);
};
