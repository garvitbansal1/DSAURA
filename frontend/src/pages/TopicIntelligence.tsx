import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Brain, ShieldCheck, AlertCircle, BarChart3,
  ChevronDown, ChevronUp, Layers, CheckCircle2,
  ArrowRight, BookOpen, Sparkles
} from 'lucide-react';
import { masteryAPI } from '../api/mastery';
import type { TopicMasteryDTO } from '../api/mastery';

const LEVEL_CONFIG: Record<string, { label: string; color: string }> = {
  advanced: { label: 'Advanced', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' },
  strong: { label: 'Strong', color: 'text-green-400 bg-green-500/10 border-green-500/30' },
  intermediate: { label: 'Intermediate', color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30' },
  developing: { label: 'Developing', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' },
  beginner: { label: 'Beginner', color: 'text-orange-400 bg-orange-500/10 border-orange-500/30' },
  insufficient_evidence: { label: 'Insufficient Evidence (<3 solved)', color: 'text-gray-400 bg-gray-500/10 border-gray-500/30' },
};

export function TopicIntelligence() {
  const [masteryData, setMasteryData] = useState<TopicMasteryDTO[]>([]);
  const [expandedTopic, setExpandedTopic] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'evaluated' | 'insufficient'>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMastery() {
      try {
        setLoading(true);
        const data = await masteryAPI.getTopicMastery();
        setMasteryData(data);
        if (data.length > 0) {
          const firstEvaluated = data.find((d) => d.has_sufficient_evidence) || data[0];
          setExpandedTopic(firstEvaluated.topic_slug);
        }
      } catch (err) {
        console.error('Failed to load topic mastery', err);
      } finally {
        setLoading(false);
      }
    }
    loadMastery();
  }, []);

  const toggleExpand = (slug: string) => {
    setExpandedTopic(expandedTopic === slug ? null : slug);
  };

  const filteredTopics = masteryData.filter((t) => {
    if (filter === 'evaluated') return t.has_sufficient_evidence;
    if (filter === 'insufficient') return !t.has_sufficient_evidence;
    return true;
  });

  const evaluatedCount = masteryData.filter((t) => t.has_sufficient_evidence).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Calculating 5-Dimension Mastery Metrics...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Brain className="w-6 h-6 text-[#6272f1]" />
            Topic-Wise Intelligence & Mastery Engine
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            Measurable mastery evaluated across 5 core dimensions: Pattern Coverage (30%), Independent Solving (25%),
            Difficulty Progression (20%), Diversity (15%), and Revision Retention (10%).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/recommendations"
            className="px-3.5 py-2 bg-[#6272f1] hover:bg-[#4f56e5] text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all shadow-md shadow-[#6272f1]/20"
          >
            <Sparkles className="w-3.5 h-3.5" /> Practice Weak Topics
          </Link>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-[#2a2a4a] pb-2 text-xs">
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1.5 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-[#6272f1] text-white'
              : 'text-gray-400 hover:text-white bg-[#1a1a2e]'
          }`}
        >
          All Topics ({masteryData.length})
        </button>
        <button
          onClick={() => setFilter('evaluated')}
          className={`px-3 py-1.5 rounded-lg font-medium transition-colors ${
            filter === 'evaluated'
              ? 'bg-[#6272f1] text-white'
              : 'text-gray-400 hover:text-white bg-[#1a1a2e]'
          }`}
        >
          Evaluated Topics ({evaluatedCount})
        </button>
        <button
          onClick={() => setFilter('insufficient')}
          className={`px-3 py-1.5 rounded-lg font-medium transition-colors ${
            filter === 'insufficient'
              ? 'bg-[#6272f1] text-white'
              : 'text-gray-400 hover:text-white bg-[#1a1a2e]'
          }`}
        >
          Need Practice (&lt;3) ({masteryData.length - evaluatedCount})
        </button>
      </div>

      {/* Topics List with Multi-Dimension Accordion */}
      <div className="space-y-3">
        {filteredTopics.map((topic) => {
          const isExpanded = expandedTopic === topic.topic_slug;
          const levelInfo = LEVEL_CONFIG[topic.mastery_level] || LEVEL_CONFIG.insufficient_evidence;

          return (
            <div
              key={topic.topic_slug}
              className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl overflow-hidden transition-all"
            >
              {/* Accordion Summary Row */}
              <div
                onClick={() => toggleExpand(topic.topic_slug)}
                className="p-5 flex items-center justify-between cursor-pointer hover:bg-[#252540]/50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-[#0f0f1a] border border-[#2a2a4a] flex items-center justify-center text-white font-bold text-sm">
                    {topic.topic_name.substring(0, 2).toUpperCase()}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-white font-semibold text-base">{topic.topic_name}</h3>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold border ${levelInfo.color}`}>
                        {levelInfo.label}
                      </span>
                    </div>
                    <p className="text-gray-400 text-xs mt-0.5 flex items-center gap-2">
                      <span>Evaluated Problems: <strong className="text-white">{topic.problems_recorded}</strong></span>
                      <span>•</span>
                      <span>Confidence: <strong className="text-cyan-400">{(topic.evidence_confidence * 100).toFixed(0)}%</strong></span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  {/* Mastery Score Progress Meter */}
                  <div className="text-right hidden sm:block">
                    <div className="text-xs text-gray-400 mb-1">Demonstrated Mastery</div>
                    <div className="flex items-center gap-2">
                      <div className="w-28 bg-[#0f0f1a] h-2 rounded-full overflow-hidden border border-[#2a2a4a]">
                        <div
                          className="bg-[#6272f1] h-full rounded-full transition-all"
                          style={{ width: `${Math.min(100, topic.mastery_score)}%` }}
                        />
                      </div>
                      <span className="text-white text-xs font-bold font-mono">
                        {topic.mastery_score.toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </div>
              </div>

              {/* Expanded Breakdown */}
              {isExpanded && (
                <div className="p-5 bg-[#0f0f1a] border-t border-[#2a2a4a] space-y-4">
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <div>
                      <strong className="text-white">Evidence Evaluation: </strong>
                      {!topic.has_sufficient_evidence
                        ? 'Fewer than 3 problems recorded. Solve problems in this topic to establish evidence-based mastery.'
                        : 'Comprehensive score computed from verified solving behavior and pattern diversity.'}
                    </div>

                    <Link
                      to={`/patterns?topic=${topic.topic_slug}`}
                      className="text-[#6272f1] hover:underline flex items-center gap-1 shrink-0 font-medium"
                    >
                      Browse Patterns <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>

                  {/* 5-Dimension Visual Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-3 pt-2">
                    {[
                      { name: 'Pattern Coverage', weight: '30%', score: topic.score_breakdown?.pattern_coverage ?? 0 },
                      { name: 'Independent Solving', weight: '25%', score: topic.score_breakdown?.independent_solving ?? 0 },
                      { name: 'Difficulty Progression', weight: '20%', score: topic.score_breakdown?.difficulty_progression ?? 0 },
                      { name: 'Problem Diversity', weight: '15%', score: topic.score_breakdown?.problem_diversity ?? 0 },
                      { name: 'Revision Retention', weight: '10%', score: topic.score_breakdown?.revision_retention ?? 0 },
                    ].map((dim) => (
                      <div
                        key={dim.name}
                        className="bg-[#1a1a2e] border border-[#2a2a4a] p-3 rounded-lg"
                      >
                        <div className="flex items-center justify-between text-[11px] text-gray-400 mb-1">
                          <span className="truncate pr-1">{dim.name}</span>
                          <span className="text-gray-500 font-mono">{dim.weight}</span>
                        </div>
                        <div className="text-sm font-bold text-white mb-2 font-mono">
                          {dim.score.toFixed(1)} / 100
                        </div>
                        <div className="w-full bg-[#0f0f1a] h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-[#6272f1] h-full rounded-full"
                            style={{ width: `${Math.min(100, dim.score)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
