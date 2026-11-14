import { apiClient } from './client';
import type { CodingProfile, ProfileCreate } from '../types/profile';

export const profilesAPI = {
  list: () => apiClient.get<CodingProfile[]>('/profiles'),
  create: (data: ProfileCreate) => apiClient.post<CodingProfile>('/profiles', data),
  delete: (id: string) => apiClient.delete(`/profiles/${id}`),
  sync: (id: string) => apiClient.post(`/profiles/${id}/sync`),
  syncHistory: (id: string) => apiClient.get(`/profiles/${id}/sync-history`),
  getCrossPlatformStats: () => apiClient.get('/profiles/cross-platform-stats'),
};
