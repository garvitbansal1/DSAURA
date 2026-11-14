import { useEffect, useState } from 'react';
import {
  TrendingUp, Calendar, Award, CheckCircle,
  Flag, ArrowUpRight, Zap
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
} from 'recharts';
import { masteryAPI } from '../api/mastery';

export function Journey() {
  const [journey, setJourney] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadJourney() {
      try {
        setLoading(true);
        const data = await masteryAPI.getJourneyHistory();
        setJourney(data);
      } catch (err) {
        console.error('Failed to load journey history', err);
      } finally {
        setLoading(false);
      }
    }
    loadJourney();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Synthesizing Historical Learning Journey...
      </div>
    );
  }

  const timeline = journey?.timeline || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <TrendingUp className="w-6 h-6 text-[#6272f1]" />
          Long-Term DSA Learning Journey
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Track demonstrated problem-solving development, pattern acquisition, and cognitive retention over time.
        </p>
      </div>

      {/* Main Mastery Progression Chart */}
      <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Mastery Score Evolution (0–100%)</h2>
            <p className="text-gray-400 text-xs mt-0.5">
              Weighted composite of pattern breadth, independence, and difficulty progression
            </p>
          </div>
          <span className="text-xs font-semibold text-[#6272f1] bg-[#6272f1]/10 px-2.5 py-1 rounded border border-[#6272f1]/20">
            Target Track: {journey?.user_goal?.toUpperCase() || 'PLACEMENT'}
          </span>
        </div>

        <div className="h-72 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeline}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" vertical={false} />
              <XAxis dataKey="date" stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
              <YAxis domain={[0, 100]} stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f0f1a',
                  border: '1px solid #2a2a4a',
                  borderRadius: '8px',
                  fontSize: '12px',
                }}
              />
              <Line
                type="monotone"
                dataKey="mastery_score"
                stroke="#6272f1"
                strokeWidth={3}
                dot={{ r: 4, fill: '#6272f1' }}
                name="Mastery Score (%)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Problems vs Patterns Dual Metric */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Problems Solved vs. Patterns Mastered
          </h3>
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" vertical={false} />
                <XAxis dataKey="week" stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f0f1a',
                    border: '1px solid #2a2a4a',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="problems_solved" fill="#3b82f6" name="Cumulative Problems" />
                <Bar dataKey="patterns_mastered" fill="#10b981" name="Patterns Mastered" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Learning Milestones Roadmap */}
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Flag className="w-4 h-4 text-emerald-400" />
            Milestones & Goals
          </h3>

          <div className="space-y-3">
            {(journey?.milestones || []).map((m: any, idx: number) => (
              <div
                key={idx}
                className="bg-[#0f0f1a] border border-[#2a2a4a] p-4 rounded-xl flex items-start gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-[#6272f1]/15 border border-[#6272f1]/30 flex items-center justify-center text-[#6272f1] shrink-0 mt-0.5">
                  <CheckCircle className="w-4 h-4" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">{m.title}</span>
                    <span className="text-[10px] text-gray-500 font-mono">({m.date})</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">{m.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
