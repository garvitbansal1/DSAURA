export interface CodingProfile {
  id: string;
  user_id: string;
  platform: 'leetcode' | 'codeforces' | 'geeksforgeeks' | 'hackerrank';
  username: string;
  profile_url?: string;
  is_verified: boolean;
  last_synced_at?: string;
  sync_status: 'never' | 'pending' | 'syncing' | 'success' | 'failed';
  raw_stats?: Record<string, unknown>;
  created_at: string;
}

export interface ProfileCreate {
  platform: string;
  username: string;
  profile_url?: string;
}
