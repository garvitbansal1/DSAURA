import { apiClient } from './client';

export interface TopicMasteryDTO {
  topic_slug: string;
  topic_name: string;
  mastery_score: number;
  mastery_level: string;
  evidence_confidence: number;
  problems_recorded: number;
  has_sufficient_evidence: boolean;
  score_breakdown: Record<string, number>;
}

export interface RecommendationItem {
  problem_id: string;
  platform: string;
  name: string;
  url: string;
  difficulty: string;
  topics: string[];
  patterns: string[];
  reason: string;
  expected_outcome: string;
  priority: number;
}

export interface RealityCheckData {
  total_problems_solved: number;
  unique_patterns_practiced: number;
  total_patterns_available: number;
  pattern_coverage_pct: number;
  concentration_alert: boolean;
  summary_message: string;
  gaps: Array<{
    gap_type: string;
    severity: string;
    topic_slug: string;
    topic_name: string;
    title: string;
    description: string;
    recommendation: string;
    evidence: Record<string, any>;
  }>;
  overpracticed_patterns: Array<{
    pattern_name: string;
    topic: string;
    count: number;
    ideal_count: number;
    status: string;
  }>;
  blindspot_topics: string[];
}

export interface DashboardStatsData {
  total_solved: number;
  easy_solved: number;
  medium_solved: number;
  hard_solved: number;
  streak: number;
  max_streak: number;
  acceptance_rate: number;
  total_submissions: number;
  topic_distribution: Array<{ topic: string; count: number; mastery: number }>;
  difficulty_distribution: Array<{ name: string; value: number; color: string }>;
  heatmap: Array<{ date: string; count: number; level: number }>;
  recent_activity: Array<{
    problem: string;
    platform: string;
    difficulty: string;
    time: string;
    status: string;
  }>;
}

export interface RevisionItem {
  id: string;
  problem_id: string;
  problem_title: string;
  platform: string;
  difficulty: string;
  url?: string;
  repetition_count: number;
  ease_factor: number;
  interval_days: number;
  due_date: string;
  is_overdue: boolean;
  status: 'due_today' | 'overdue' | 'upcoming';
}

export const masteryAPI = {
  getTopicMastery: async (): Promise<TopicMasteryDTO[]> => {
    const res = await apiClient.get('/mastery/topics');
    return res.data;
  },
  getRecommendations: async (): Promise<RecommendationItem[]> => {
    const res = await apiClient.get('/recommendations');
    return res.data;
  },
  getRealityCheck: async (): Promise<RealityCheckData> => {
    const res = await apiClient.get('/gaps/reality-check');
    return res.data;
  },
  getDashboardStats: async (): Promise<DashboardStatsData> => {
    const res = await apiClient.get('/activity/dashboard-stats');
    return res.data;
  },
  getJourneyHistory: async () => {
    const res = await apiClient.get('/activity/journey-history');
    return res.data;
  },
  getRevisionQueue: async (): Promise<RevisionItem[]> => {
    const res = await apiClient.get('/revision');
    return res.data;
  },
  reviewItem: async (revisionId: string, quality: number) => {
    const res = await apiClient.post('/revision/review', {
      revision_id: revisionId,
      quality,
    });
    return res.data;
  },
  getAssessmentQuestions: async () => {
    const res = await apiClient.get('/assessments/questions');
    return res.data;
  },
  submitAssessment: async (answers: Record<string, string>) => {
    const res = await apiClient.post('/assessments/evaluate', { answers });
    return res.data;
  },
};
