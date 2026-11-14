import { useEffect, useState } from 'react';
import {
  AlertTriangle, CheckCircle2, TrendingUp, ShieldAlert,
  HelpCircle, ArrowRight, Lightbulb, Compass
} from 'lucide-react';
import { masteryAPI } from '../api/mastery';
import type { RealityCheckData } from '../api/mastery';

export function RealityCheck() {
  const [data, setData] = useState<RealityCheckData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReality() {
      try {
        setLoading(true);
        const res = await masteryAPI.getRealityCheck();
        setData(res);
      } catch (err) {
        console.error('Failed to load reality check', err);
      } finally {
        setLoading(false);
      }
    }
    loadReality();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Running Algorithmic Reality Check...
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <ShieldAlert className="w-6 h-6 text-amber-400" />
          Knowledge Reality Check
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          "Solving more problems does not mean learning more." DSAURA measures demonstrated problem-solving breadth, not just problem counts.
        </p>
      </div>

      {/* Core Ratio Hero Box */}
      <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-[#0f0f1a] p-4 rounded-xl border border-[#2a2a4a]">
            <span className="text-gray-500 text-xs uppercase tracking-wider font-semibold">
              Total Problems Solved
            </span>
            <div className="text-3xl font-bold text-white mt-1 font-mono">
              {data.total_problems_solved}
            </div>
            <p className="text-gray-500 text-[11px] mt-1">Across synced profiles</p>
          </div>

          <div className="bg-[#0f0f1a] p-4 rounded-xl border border-[#2a2a4a]">
            <span className="text-gray-500 text-xs uppercase tracking-wider font-semibold">
              Unique Patterns Explored
            </span>
            <div className="text-3xl font-bold text-[#6272f1] mt-1 font-mono">
              {data.unique_patterns_practiced} / {data.total_patterns_available}
            </div>
            <p className="text-gray-500 text-[11px] mt-1">
              {data.pattern_coverage_pct}% taxonomy coverage
            </p>
          </div>

          <div className="bg-[#0f0f1a] p-4 rounded-xl border border-[#2a2a4a]">
            <span className="text-gray-500 text-xs uppercase tracking-wider font-semibold">
              Pattern Concentration Alert
            </span>
            <div
              className={`text-xl font-bold mt-2 flex items-center gap-2 ${
                data.concentration_alert ? 'text-amber-400' : 'text-emerald-400'
              }`}
            >
              {data.concentration_alert ? (
                <>
                  <AlertTriangle className="w-5 h-5" /> High Concentration
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-5 h-5" /> Balanced Coverage
                </>
              )}
            </div>
            <p className="text-gray-500 text-[11px] mt-1">
              {data.concentration_alert
                ? 'Repeatedly solving identical pattern types'
                : 'Broad exposure across diverse topics'}
            </p>
          </div>
        </div>

        {/* Summary Banner */}
        <div className="bg-[#0f0f1a] border border-[#2a2a4a] p-4 rounded-lg flex items-start gap-3 text-xs text-gray-300">
          <Compass className="w-5 h-5 text-[#6272f1] shrink-0 mt-0.5" />
          <p className="leading-relaxed">{data.summary_message}</p>
        </div>
      </div>

      {/* Identified Critical Gaps */}
      <div className="space-y-3">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Detected Algorithmic Blind Spots ({data.gaps.length})
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.gaps.map((gap, idx) => (
            <div
              key={idx}
              className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-5 space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded border text-amber-400 bg-amber-500/10 border-amber-500/20">
                  {gap.topic_name}
                </span>

                <span
                  className={`text-[10px] font-semibold px-2 py-0.5 rounded uppercase ${
                    gap.severity === 'high'
                      ? 'text-red-400 bg-red-500/10'
                      : 'text-amber-400 bg-amber-500/10'
                  }`}
                >
                  {gap.severity} Priority
                </span>
              </div>

              <h3 className="text-sm font-bold text-white">{gap.title}</h3>
              <p className="text-xs text-gray-300 leading-relaxed">{gap.description}</p>

              <div className="bg-[#0f0f1a] border border-[#2a2a4a] p-3 rounded-lg text-xs">
                <span className="text-emerald-400 font-semibold block mb-0.5 flex items-center gap-1">
                  <Lightbulb className="w-3.5 h-3.5" /> Recommended Remedy
                </span>
                <p className="text-gray-300">{gap.recommendation}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Over-Practiced vs Ideal Volume */}
      <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-6">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-[#6272f1]" />
          Pattern Repetition Breakdown
        </h3>

        <div className="space-y-3">
          {data.overpracticed_patterns.map((item, idx) => (
            <div
              key={idx}
              className="bg-[#0f0f1a] border border-[#2a2a4a] p-3.5 rounded-lg flex items-center justify-between text-xs"
            >
              <div>
                <span className="text-white font-semibold">{item.pattern_name}</span>
                <span className="text-gray-500 text-[11px] block">{item.topic}</span>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <span className="text-gray-400">Solved: </span>
                  <strong className="text-white font-mono">{item.count}</strong>
                  <span className="text-gray-600"> (Ideal: {item.ideal_count})</span>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30">
                  {item.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
