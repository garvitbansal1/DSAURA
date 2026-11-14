import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Zap, Target, CheckCircle, Link2, ArrowRight,
  BookOpen, Sparkles, ShieldAlert, RotateCcw, Brain, Activity
} from 'lucide-react';
import {
  ResponsiveContainer, PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import { useAuthStore } from '../store/authStore';
import { profilesAPI } from '../api/profiles';
import { masteryAPI } from '../api/mastery';
import type { CodingProfile } from '../types/profile';
import type { DashboardStatsData } from '../api/mastery';

const PLATFORM_COLORS: Record<string, string> = {
  leetcode: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
  codeforces: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  geeksforgeeks: 'text-green-400 bg-green-500/10 border-green-500/20',
  hackerrank: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
};

const PLATFORM_LABELS: Record<string, string> = {
  leetcode: 'LeetCode',
  codeforces: 'Codeforces',
  geeksforgeeks: 'GeeksforGeeks',
  hackerrank: 'HackerRank',
};

export function Dashboard() {
  const user = useAuthStore((s) => s.user);
  const [profiles, setProfiles] = useState<CodingProfile[]>([]);
  const [statsData, setStatsData] = useState<DashboardStatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAll() {
      try {
        setLoading(true);
        const [profRes, statsRes] = await Promise.all([
          profilesAPI.list().then((r) => r.data).catch(() => []),
          masteryAPI.getDashboardStats().catch(() => null),
        ]);
        setProfiles(profRes);
        setStatsData(statsRes);
      } finally {
        setLoading(false);
      }
    }
    loadAll();
  }, []);

  const totalSolved = statsData?.total_solved || 0;
  const streak = statsData?.streak || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">
            Welcome back, {user?.name || 'Developer'}! 👋
          </h1>
          <p className="text-gray-400 text-sm mt-0.5">
            Target Track:{' '}
            <span className="text-[#6272f1] font-semibold uppercase">
              {user?.learning_goal || 'Placement Preparation'}
            </span>{' '}
            • Tracking pattern mastery across your coding profiles
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/reality-check"
            className="px-3.5 py-2 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/30 text-amber-400 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors"
          >
            <ShieldAlert className="w-3.5 h-3.5" /> Reality Check
          </Link>
          <Link
            to="/recommendations"
            className="px-3.5 py-2 bg-[#6272f1] hover:bg-[#4f56e5] text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all shadow-md shadow-[#6272f1]/20"
          >
            <Sparkles className="w-3.5 h-3.5" /> Next Problems
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Problems Solved</span>
            <Target className="w-4 h-4 text-[#6272f1]" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">{totalSolved}</div>
          <span className="text-[11px] text-gray-500 mt-0.5 block">Across connected platforms</span>
        </div>

        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Current Streak</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">{streak} days</div>
          <span className="text-[11px] text-gray-500 mt-0.5 block">
            Best: {statsData?.max_streak || 14} days
          </span>
        </div>

        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Acceptance Rate</span>
            <CheckCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">
            {statsData?.acceptance_rate?.toFixed(1) || '62.4'}%
          </div>
          <span className="text-[11px] text-gray-500 mt-0.5 block">
            {statsData?.total_submissions || 76} total submissions
          </span>
        </div>

        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Connected Profiles</span>
            <Link2 className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono">{profiles.length}</div>
          <Link to="/profiles" className="text-[11px] text-[#6272f1] hover:underline mt-0.5 block">
            Manage integrations →
          </Link>
        </div>
      </div>

      {/* Visual Charts: Difficulty Donut & Topic Mastery */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Difficulty Donut */}
        <div className="lg:col-span-4 bg-[#1a1a2e] border border-[#2a2a4a] p-5 rounded-xl flex flex-col justify-between">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-2">
            Difficulty Distribution
          </h2>

          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statsData?.difficulty_distribution || []}
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {(statsData?.difficulty_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f0f1a',
                    border: '1px solid #2a2a4a',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#2a2a4a]">
            <div>
              <span className="text-[10px] text-emerald-400 font-semibold block">Easy</span>
              <span className="text-sm font-bold text-white font-mono">
                {statsData?.easy_solved || 0}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-amber-400 font-semibold block">Medium</span>
              <span className="text-sm font-bold text-white font-mono">
                {statsData?.medium_solved || 0}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-red-400 font-semibold block">Hard</span>
              <span className="text-sm font-bold text-white font-mono">
                {statsData?.hard_solved || 0}
              </span>
            </div>
          </div>
        </div>

        {/* Topic Mastery Distribution */}
        <div className="lg:col-span-8 bg-[#1a1a2e] border border-[#2a2a4a] p-5 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Topic Practice vs Demonstrated Mastery
            </h2>
            <Link to="/topics" className="text-xs text-[#6272f1] hover:underline flex items-center gap-1">
              Deep Dive <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={statsData?.topic_distribution || []} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" horizontal={false} />
                <XAxis type="number" stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis
                  dataKey="topic"
                  type="category"
                  stroke="#6b7280"
                  tick={{ fill: '#9ca3af', fontSize: 11 }}
                  width={110}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f0f1a',
                    border: '1px solid #2a2a4a',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="count" fill="#3b82f6" name="Problems Solved" />
                <Bar dataKey="mastery" fill="#6272f1" name="Mastery Score (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 60-Day Activity Heatmap */}
      <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-5 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              60-Day Problem-Solving Activity
            </h2>
          </div>
          <div className="flex items-center gap-1.5 text-[10px] text-gray-500">
            <span>Less</span>
            <span className="w-2.5 h-2.5 rounded-sm bg-[#0f0f1a] border border-[#2a2a4a]" />
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-900/60" />
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-700" />
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-400" />
            <span>More</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-1.5 pt-1">
          {(statsData?.heatmap || []).map((day, idx) => {
            const colors = [
              'bg-[#0f0f1a] border border-[#2a2a4a]',
              'bg-emerald-900/60',
              'bg-emerald-700',
              'bg-emerald-500',
              'bg-emerald-400',
            ];
            return (
              <div
                key={idx}
                title={`${day.date}: ${day.count} problem(s)`}
                className={`w-3.5 h-3.5 rounded-sm cursor-pointer transition-transform hover:scale-125 ${
                  colors[day.level] || colors[0]
                }`}
              />
            );
          })}
        </div>
      </div>

      {/* Recent Activity & Connected Profiles */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Connected Profiles Card */}
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-5 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Connected Platforms ({profiles.length})
            </h2>
            <Link to="/profiles" className="text-xs text-[#6272f1] hover:underline">
              Manage →
            </Link>
          </div>

          {profiles.length === 0 ? (
            <div className="text-center py-6 text-gray-500 text-xs">
              No profile connected yet. Connect your LeetCode or Codeforces profile!
            </div>
          ) : (
            <div className="space-y-2">
              {profiles.map((p) => {
                const color = PLATFORM_COLORS[p.platform] || 'text-gray-400 bg-gray-500/10 border-gray-500/20';
                return (
                  <div
                    key={p.id}
                    className="p-3 bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg flex items-center justify-between text-xs"
                  >
                    <div className="flex items-center gap-2.5">
                      <span className={`px-2 py-0.5 rounded font-bold border ${color}`}>
                        {PLATFORM_LABELS[p.platform] || p.platform}
                      </span>
                      <span className="text-white font-medium">{p.username}</span>
                    </div>

                    <span
                      className={`text-[11px] ${
                        p.sync_status === 'success'
                          ? 'text-emerald-400'
                          : p.sync_status === 'failed'
                          ? 'text-red-400'
                          : 'text-gray-500'
                      }`}
                    >
                      {p.sync_status === 'success' ? '● Synced' : '○ Pending'}
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Recent Solved Activity */}
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-5 rounded-xl space-y-3">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Recent Solving Log
          </h2>

          <div className="space-y-2">
            {(statsData?.recent_activity || []).map((act, idx) => (
              <div
                key={idx}
                className="p-3 bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg flex items-center justify-between text-xs"
              >
                <div>
                  <h4 className="text-white font-medium">{act.problem}</h4>
                  <span className="text-gray-500 text-[11px]">{act.status}</span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                    {act.difficulty}
                  </span>
                  <span className="text-gray-500 text-[10px] block mt-1">{act.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
