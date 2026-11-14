import { useEffect, useState } from 'react';
import {
  Sparkles, ExternalLink, ArrowRight, Target,
  CheckCircle, BookOpen, AlertCircle
} from 'lucide-react';
import { masteryAPI } from '../api/mastery';
import type { RecommendationItem } from '../api/mastery';

export function Recommendations() {
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRecs() {
      try {
        setLoading(true);
        const data = await masteryAPI.getRecommendations();
        setRecommendations(data);
      } catch (err) {
        console.error('Failed to load recommendations', err);
      } finally {
        setLoading(false);
      }
    }
    loadRecs();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Generating Targeted Algorithmic Recommendations...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-[#6272f1]" />
          Personalized Problem Recommendations
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Algorithmic problems prioritized by identified knowledge gaps, prerequisite readiness, and demonstrated pattern coverage.
        </p>
      </div>

      {recommendations.length === 0 ? (
        <div className="p-12 text-center text-gray-500 bg-[#1a1a2e] rounded-xl border border-[#2a2a4a]">
          No new recommendations at this moment. You are up to date!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((rec) => (
            <div
              key={rec.problem_id}
              className="bg-[#1a1a2e] border border-[#2a2a4a] hover:border-[#6272f1]/50 rounded-xl p-5 flex flex-col justify-between transition-all group"
            >
              <div>
                {/* Top Badges */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase border ${
                        rec.difficulty === 'easy'
                          ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                          : rec.difficulty === 'hard'
                          ? 'text-red-400 bg-red-500/10 border-red-500/20'
                          : 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                      }`}
                    >
                      {rec.difficulty}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded font-medium text-gray-400 bg-[#0f0f1a] border border-[#2a2a4a] uppercase">
                      {rec.platform}
                    </span>
                  </div>

                  <span className="text-xs font-semibold text-[#6272f1] bg-[#6272f1]/10 px-2 py-0.5 rounded border border-[#6272f1]/20">
                    Priority {rec.priority}/10
                  </span>
                </div>

                {/* Problem Name */}
                <h3 className="text-base font-bold text-white group-hover:text-[#6272f1] transition-colors mb-2">
                  {rec.name}
                </h3>

                {/* Reason & Outcome */}
                <div className="space-y-2 text-xs bg-[#0f0f1a] p-3 rounded-lg border border-[#2a2a4a] mb-4">
                  <div>
                    <span className="text-gray-500 block text-[10px] uppercase tracking-wider font-semibold">
                      Why This Problem
                    </span>
                    <p className="text-gray-300 mt-0.5">{rec.reason}</p>
                  </div>

                  <div>
                    <span className="text-gray-500 block text-[10px] uppercase tracking-wider font-semibold">
                      Target Outcome
                    </span>
                    <p className="text-emerald-400/90 mt-0.5">{rec.expected_outcome}</p>
                  </div>
                </div>

                {/* Topics / Patterns Pills */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {rec.topics.map((t) => (
                    <span
                      key={t}
                      className="text-[10px] bg-[#252540] text-gray-300 px-2 py-0.5 rounded border border-[#353555]"
                    >
                      {t}
                    </span>
                  ))}
                  {rec.patterns.map((p) => (
                    <span
                      key={p}
                      className="text-[10px] bg-[#6272f1]/10 text-[#6272f1] px-2 py-0.5 rounded border border-[#6272f1]/20"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              </div>

              {/* Action Button */}
              <a
                href={rec.url}
                target="_blank"
                rel="noreferrer"
                className="w-full py-2 bg-[#6272f1] hover:bg-[#4f56e5] text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all shadow-md shadow-[#6272f1]/20"
              >
                Solve on {rec.platform.toUpperCase()}
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
