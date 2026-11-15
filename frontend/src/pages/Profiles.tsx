import { useState, useEffect } from 'react';
import { Plus, RefreshCw, Trash2, ExternalLink, Loader2, AlertCircle, Layers, ShieldCheck } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';
import { profilesAPI } from '../api/profiles';
import type { CodingProfile, ProfileCreate } from '../types/profile';

const PLATFORMS = [
  { value: 'leetcode', label: 'LeetCode', url: 'https://leetcode.com/u/{username}', hint: 'Enter your LeetCode username' },
  { value: 'codeforces', label: 'Codeforces', url: 'https://codeforces.com/profile/{username}', hint: 'Enter your Codeforces handle' },
  { value: 'geeksforgeeks', label: 'GeeksforGeeks', url: 'https://www.geeksforgeeks.org/user/{username}', hint: 'Enter your GeeksforGeeks username' },
  { value: 'hackerrank', label: 'HackerRank', url: 'https://www.hackerrank.com/{username}', hint: 'Enter your HackerRank username' },
];

const PLATFORM_COLORS: Record<string, string> = {
  leetcode: 'text-yellow-400',
  codeforces: 'text-blue-400',
  geeksforgeeks: 'text-green-400',
  hackerrank: 'text-emerald-400',
};

const STATUS_STYLES: Record<string, string> = {
  success: 'text-green-400',
  failed: 'text-red-400',
  syncing: 'text-yellow-400',
  never: 'text-gray-500',
  pending: 'text-gray-400',
};

const STATUS_LABELS: Record<string, string> = {
  success: '✓ Synced',
  failed: '✗ Failed',
  syncing: '⟳ Syncing',
  never: '○ Never synced',
  pending: '◌ Pending',
};

export function Profiles() {
  const user = useAuthStore((s) => s.user);
  const cacheKey = `dsaura_profiles_${user?.id || 'default'}`;

  const [profiles, setProfiles] = useState<CodingProfile[]>([]);
  const [crossStats, setCrossStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [syncing, setSyncing] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [form, setForm] = useState<ProfileCreate>({ platform: 'leetcode', username: '', profile_url: '' });
  const [submitting, setSubmitting] = useState(false);

  const updateProfiles = (newProfs: CodingProfile[]) => {
    setProfiles(newProfs);
    try {
      localStorage.setItem(cacheKey, JSON.stringify(newProfs));
    } catch {}
  };

  const loadProfiles = async () => {
    setLoading(true);
    try {
      const cachedStr = localStorage.getItem(cacheKey);
      let cached: CodingProfile[] = [];
      if (cachedStr) {
        try {
          cached = JSON.parse(cachedStr);
          if (cached.length > 0) {
            setProfiles(cached);
          }
        } catch {}
      }

      const [r, cross] = await Promise.all([
        profilesAPI.list().catch(() => ({ data: [] })),
        profilesAPI.getCrossPlatformStats().catch(() => ({ data: null })),
      ]);

      if (r.data && r.data.length > 0) {
        updateProfiles(r.data);
      } else if (cached.length > 0) {
        try {
          const rehydrated = await profilesAPI.rehydrate(cached);
          if (rehydrated.data && rehydrated.data.length > 0) {
            updateProfiles(rehydrated.data);
          }
        } catch {}
      }

      setCrossStats(cross.data);
    } catch {
      toast.error('Failed to load profiles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadProfiles(); }, [cacheKey]);

  const handleConnect = async () => {
    if (!form.username.trim()) { toast.error('Username is required'); return; }
    setSubmitting(true);
    try {
      const { data } = await profilesAPI.create(form);
      const nextProfs = [...profiles.filter((p) => p.id !== data.id), data];
      updateProfiles(nextProfs);
      setShowForm(false);
      setForm({ platform: 'leetcode', username: '', profile_url: '' });
      toast.success(`${form.platform} profile connected! Synchronizing...`);
      try {
        const syncRes = await profilesAPI.sync(data.id);
        if (syncRes.data) {
          const syncedList = nextProfs.map((pr) => pr.id === data.id ? { ...pr, ...syncRes.data } : pr);
          updateProfiles(syncedList);
        }
        await loadProfiles();
        toast.success(`${form.platform} profile synchronized!`);
      } catch {
        // sync non-blocking during connect
      }
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to connect profile');
    } finally {
      setSubmitting(false);
    }
  };

  const handleSync = async (id: string) => {
    setSyncing(id);
    try {
      const syncRes = await profilesAPI.sync(id);
      if (syncRes.data) {
        const updated = profiles.map((pr) => pr.id === id ? { ...pr, ...syncRes.data } : pr);
        updateProfiles(updated);
      }
      await loadProfiles();
      toast.success('Profile synced successfully!');
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Sync failed');
    } finally {
      setSyncing(null);
    }
  };

  const handleDelete = async (id: string, platform: string) => {
    if (!confirm(`Remove ${platform} profile?`)) return;
    setDeleting(id);
    try {
      await profilesAPI.delete(id);
      const filtered = profiles.filter((pr) => pr.id !== id);
      updateProfiles(filtered);
      toast.success('Profile removed');
    } catch {
      toast.error('Failed to remove profile');
    } finally {
      setDeleting(null);
    }
  };

  const selectedPlatform = PLATFORMS.find((p) => p.value === form.platform);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">My Profiles</h1>
          <p className="text-gray-400 mt-1 text-sm">Connect your coding profiles to sync your problem history.</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary text-sm py-2">
          <Plus className="w-4 h-4" /> Connect Profile
        </button>
      </div>

      {/* Add Profile Form */}
      {showForm && (
        <div className="bg-[#1a1a2e] border border-[#6272f1]/30 rounded-xl p-5 animate-slide-up">
          <h2 className="font-semibold text-white mb-4">Connect a New Profile</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Platform</label>
              <select
                value={form.platform}
                onChange={(e) => setForm((f) => ({ ...f, platform: e.target.value }))}
                className="input"
              >
                {PLATFORMS.map(({ value, label }) => <option key={value} value={value}>{label}</option>)}
              </select>
            </div>
            <div>
              <label className="label">Username</label>
              <input
                type="text"
                value={form.username}
                onChange={(e) => setForm((f) => ({ ...f, username: e.target.value }))}
                placeholder={selectedPlatform?.hint || 'Enter username'}
                className="input"
              />
            </div>
          </div>
          {selectedPlatform?.value === 'geeksforgeeks' && (
            <div className="mt-3 flex items-start gap-2 bg-yellow-500/5 border border-yellow-500/20 rounded-lg p-3 text-sm">
              <AlertCircle className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5" />
              <div className="text-yellow-300/80">
                GeeksforGeeks does not provide a public API. Profile will be connected but automatic sync is not available. Use CSV import when available.
              </div>
            </div>
          )}
          <div className="flex items-center gap-3 mt-4">
            <button onClick={handleConnect} disabled={submitting} className="btn-primary text-sm py-2">
              {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
              {submitting ? 'Connecting…' : 'Connect Profile'}
            </button>
            <button onClick={() => setShowForm(false)} className="btn-outline text-sm py-2">Cancel</button>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center py-16 text-gray-500">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-[#6272f1]" />
          <p>Loading profiles…</p>
        </div>
      )}

      {/* Empty */}
      {!loading && profiles.length === 0 && (
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-12 text-center">
          <div className="text-5xl mb-4">🔗</div>
          <h2 className="text-lg font-semibold text-white mb-2">No profiles connected yet</h2>
          <p className="text-gray-400 text-sm mb-6">Connect LeetCode, Codeforces, or other platforms to start tracking your DSA journey.</p>
          <button onClick={() => setShowForm(true)} className="btn-primary">
            <Plus className="w-4 h-4" /> Connect Your First Profile
          </button>
        </div>
      )}

      {/* Profile Cards */}
      {!loading && profiles.length > 0 && (
        <div className="grid gap-4">
          {profiles.map((p) => {
            const stats = p.raw_stats || {};
            const platformLabel = PLATFORMS.find((pl) => pl.value === p.platform)?.label || p.platform;
            const colorClass = PLATFORM_COLORS[p.platform] || 'text-gray-400';

            return (
              <div key={p.id} className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-5 hover:border-[#6272f1]/20 transition-all">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-[#0f0f1a] rounded-lg flex items-center justify-center border border-[#2a2a4a]">
                      <span className={`font-bold text-sm ${colorClass}`}>{platformLabel[0]}</span>
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-white font-semibold">{platformLabel}</span>
                        <span className="text-gray-400 text-sm">·</span>
                        <span className="text-gray-300 text-sm font-mono">{p.username}</span>
                        <a
                          href={PLATFORMS.find(pl => pl.value === p.platform)?.url.replace('{username}', p.username)}
                          target="_blank"
                          rel="noreferrer"
                          className="text-gray-600 hover:text-gray-400"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                      <div className="flex items-center gap-3 mt-1">
                        <span className={`text-xs ${STATUS_STYLES[p.sync_status] || 'text-gray-500'}`}>
                          {STATUS_LABELS[p.sync_status] || p.sync_status}
                        </span>
                        {p.last_synced_at && (
                          <span className="text-gray-600 text-xs">
                            {new Date(p.last_synced_at).toLocaleString()}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleSync(p.id)}
                      disabled={syncing === p.id || p.sync_status === 'syncing'}
                      className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-white border border-[#2a2a4a] hover:border-[#6272f1]/30 px-3 py-1.5 rounded-lg transition-all disabled:opacity-50"
                    >
                      <RefreshCw className={`w-3.5 h-3.5 ${syncing === p.id ? 'animate-spin' : ''}`} />
                      {syncing === p.id ? 'Syncing…' : 'Sync Now'}
                    </button>
                    <button
                      onClick={() => handleDelete(p.id, platformLabel)}
                      disabled={deleting === p.id}
                      className="p-1.5 text-gray-600 hover:text-red-400 hover:bg-red-500/5 rounded-lg transition-colors"
                    >
                      {deleting === p.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Stats summary */}
                {Object.keys(stats).length > 0 && stats.available !== false && (
                  <div className="mt-4 pt-4 border-t border-[#2a2a4a] grid grid-cols-2 md:grid-cols-4 gap-3">
                    {p.platform === 'leetcode' && [
                      { label: 'Total Solved', val: String(stats.total_solved ?? '') },
                      { label: 'Easy', val: String(stats.easy_solved ?? '') },
                      { label: 'Medium', val: String(stats.medium_solved ?? '') },
                      { label: 'Hard', val: String(stats.hard_solved ?? '') },
                    ].filter(x => x.val !== '').map(({ label, val }) => (
                      <div key={label} className="bg-[#0f0f1a] rounded-lg px-3 py-2">
                        <div className="text-white font-semibold text-sm">{val}</div>
                        <div className="text-gray-500 text-xs">{label}</div>
                      </div>
                    ))}
                    {p.platform === 'codeforces' && [
                      { label: 'Total Solved', val: String(stats.total_solved ?? '') },
                      { label: 'Rating', val: String(stats.rating ?? '') },
                      { label: 'Max Rating', val: String(stats.max_rating ?? '') },
                      { label: 'Rank', val: String(stats.rank ?? '') },
                    ].filter(x => x.val !== '').map(({ label, val }) => (
                      <div key={label} className="bg-[#0f0f1a] rounded-lg px-3 py-2">
                        <div className="text-white font-semibold text-sm">{val}</div>
                        <div className="text-gray-500 text-xs">{label}</div>
                      </div>
                    ))}
                    {p.platform === 'geeksforgeeks' && [
                      { label: 'Total Solved', val: String(stats.total_solved ?? '') },
                      { label: 'Easy', val: String(stats.easy_solved ?? '') },
                      { label: 'Medium', val: String(stats.medium_solved ?? '') },
                      { label: 'Score', val: String(stats.coding_score ?? '') },
                    ].filter(x => x.val !== '').map(({ label, val }) => (
                      <div key={label} className="bg-[#0f0f1a] rounded-lg px-3 py-2">
                        <div className="text-white font-semibold text-sm">{val}</div>
                        <div className="text-gray-500 text-xs">{label}</div>
                      </div>
                    ))}
                    {p.platform === 'hackerrank' && [
                      { label: 'Total Solved', val: String(stats.total_solved ?? '') },
                      { label: 'Easy', val: String(stats.easy_solved ?? '') },
                      { label: 'Medium', val: String(stats.medium_solved ?? '') },
                      { label: 'Badges', val: String(stats.badges_count ?? '') },
                    ].filter(x => x.val !== '').map(({ label, val }) => (
                      <div key={label} className="bg-[#0f0f1a] rounded-lg px-3 py-2">
                        <div className="text-white font-semibold text-sm">{val}</div>
                        <div className="text-gray-500 text-xs">{label}</div>
                      </div>
                    ))}
                  </div>
                )}

                {stats.available === false && (
                  <div className="mt-3 flex items-center gap-2 text-xs text-yellow-400/80">
                    <AlertCircle className="w-3.5 h-3.5" />
                    {String(stats.reason || stats.error || 'Limited data available for this platform.')}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Cross-Platform Deduplication & Intelligence (Phase 15) */}
      {crossStats && (
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#6272f1]" />
              Cross-Platform Deduplication & Synergy Engine
            </h3>
            <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/20 font-semibold uppercase">
              Phase 15 Active
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a]">
              <span className="text-gray-500 text-xs block">Raw Total Solved</span>
              <span className="text-lg font-bold text-white font-mono">{crossStats.total_raw_solved}</span>
              <span className="text-[10px] text-gray-500 block">Sum across all platforms</span>
            </div>

            <div className="bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a]">
              <span className="text-gray-500 text-xs block">Deduplicated Unique</span>
              <span className="text-lg font-bold text-[#6272f1] font-mono">{crossStats.deduplicated_solved}</span>
              <span className="text-[10px] text-emerald-400 block">True problem count</span>
            </div>

            <div className="bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a]">
              <span className="text-gray-500 text-xs block">Cross-Platform Overlap</span>
              <span className="text-lg font-bold text-amber-400 font-mono">
                {crossStats.duplicates_detected} duplicates
              </span>
              <span className="text-[10px] text-gray-500 block">Identical problem titles filtered</span>
            </div>
          </div>

          {crossStats.synergy_insights && crossStats.synergy_insights.length > 0 && (
            <div className="bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a] text-xs">
              <div className="flex items-center gap-1.5 text-[#6272f1] font-semibold mb-1">
                <ShieldCheck className="w-4 h-4" />
                {crossStats.synergy_insights[0].synergy_title}
              </div>
              <p className="text-gray-300 leading-relaxed">
                {crossStats.synergy_insights[0].description}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Platform notes */}
      <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-5">
        <h3 className="text-sm font-semibold text-white mb-3">Platform Integration Notes</h3>
        <div className="grid md:grid-cols-2 gap-2">
          {[
            { platform: 'LeetCode', status: '✓ Full sync', desc: 'Problems, difficulty, streak, contest rating', ok: true },
            { platform: 'Codeforces', status: '✓ Full sync', desc: 'Rating, contests, submission history', ok: true },
            { platform: 'GeeksforGeeks', status: '◌ CSV import', desc: 'No public API — manual import only', ok: false },
            { platform: 'HackerRank', status: '~ Limited', desc: 'Profile data only, no submission history', ok: false },
          ].map(({ platform, status, desc, ok }) => (
            <div key={platform} className="flex items-start gap-2 text-xs">
              <span className={ok ? 'text-green-400' : 'text-yellow-400'}>{status}</span>
              <span className="text-gray-600">·</span>
              <div>
                <span className="text-gray-300 font-medium">{platform}</span>
                <span className="text-gray-500 ml-1">{desc}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
