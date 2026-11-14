export interface User {
  id: string;
  name: string;
  email: string;
  avatar_url?: string;
  experience_level?: 'beginner' | 'intermediate' | 'advanced';
  preferred_language?: 'java' | 'python';
  learning_goal?: 'placement' | 'competitive' | 'interview' | 'fundamentals' | 'advanced';
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  experience_level?: string;
  learning_goal?: string;
  preferred_language?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}
