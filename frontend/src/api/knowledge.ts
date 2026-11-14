import { apiClient } from './client';

export interface DSATopicItem {
  id: string;
  name: string;
  slug: string;
  parent_id?: string;
  description?: string;
  sort_order: number;
  patterns: Array<{
    id: string;
    name: string;
    slug: string;
    difficulty_level?: string;
  }>;
}

export interface DSAPatternItem {
  id: string;
  topic_id: string;
  name: string;
  slug: string;
  explanation?: string;
  when_to_use?: string;
  recognition_clues?: string;
  common_keywords?: string[];
  pseudocode?: string;
  java_template?: string;
  python_template?: string;
  time_complexity?: string;
  space_complexity?: string;
  common_mistakes?: string[];
  difficulty_level?: string;
}

export interface ProblemSummaryItem {
  id: string;
  title: string;
  slug: string;
  platform: string;
  difficulty: string;
  url?: string;
}

export const knowledgeAPI = {
  getTopics: async (): Promise<DSATopicItem[]> => {
    const res = await apiClient.get('/topics');
    return res.data;
  },
  getPatterns: async (topicSlug?: string): Promise<DSAPatternItem[]> => {
    const res = await apiClient.get('/patterns', {
      params: topicSlug ? { topic_slug: topicSlug } : {},
    });
    return res.data;
  },
  getPatternDetail: async (idOrSlug: string): Promise<DSAPatternItem> => {
    const res = await apiClient.get(`/patterns/${idOrSlug}`);
    return res.data;
  },
  getPatternProblems: async (idOrSlug: string): Promise<ProblemSummaryItem[]> => {
    const res = await apiClient.get(`/patterns/${idOrSlug}/problems`);
    return res.data;
  },
  getKnowledgeGraph: async () => {
    const res = await apiClient.get('/knowledge-graph');
    return res.data;
  },
};
