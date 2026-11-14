import { apiClient } from './client';
import type { TokenResponse, RegisterRequest, LoginRequest } from '../types/auth';

export const authAPI = {
  register: (data: RegisterRequest) => apiClient.post<TokenResponse>('/auth/register', data),
  login: (data: LoginRequest) => apiClient.post<TokenResponse>('/auth/login', data),
  logout: () => apiClient.post('/auth/logout'),
  getMe: () => apiClient.get('/users/me'),
  updateMe: (data: Partial<{ name: string; avatar_url: string; experience_level: string; preferred_language: string; learning_goal: string }>) =>
    apiClient.patch('/users/me', data),
};
