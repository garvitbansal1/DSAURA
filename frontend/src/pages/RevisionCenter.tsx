import { useEffect, useState } from 'react';
import {
  RotateCcw, Calendar, CheckCircle2, Clock,
  ExternalLink, Sparkles, AlertCircle, ArrowUpRight
} from 'lucide-react';
import toast from 'react-hot-toast';
import { masteryAPI } from '../api/mastery';
import type { RevisionItem } from '../api/mastery';

export function RevisionCenter() {
  const [queue, setQueue] = useState<RevisionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [reviewingItem, setReviewingItem] = useState<RevisionItem | null>(null);

  useEffect(() => {
    loadQueue();
  }, []);

  async function loadQueue() {
    try {
      setLoading(true);
      const data = await masteryAPI.getRevisionQueue();
      setQueue(data);
    } catch (err) {
      console.error('Failed to load revision queue', err);
    } finally {
      setLoading(false);
    }
  }

  const handleReview = async (quality: number) => {
    if (!reviewingItem) return;
    try {
      const res = await masteryAPI.reviewItem(reviewingItem.id, quality);
      toast.success(res.message || 'Review recorded successfully');
      setReviewingItem(null);
      loadQueue();
    } catch {
      toast.error('Failed to record review');
    }
  };

  const dueItems = queue.filter((i) => i.status === 'due_today' || i.status === 'overdue');
  const upcomingItems = queue.filter((i) => i.status === 'upcoming');

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Calculating Spaced Repetition (SM-2) Queue...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <RotateCcw className="w-6 h-6 text-[#6272f1]" />
          Spaced Repetition & Revision Center
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Optimized with the SuperMemo SM-2 algorithm to combat the forgetting curve. Rate recall quality to automatically calculate the next optimal review interval.
        </p>
      </div>

      {/* Review Dialog Banner if active */}
      {reviewingItem && (
        <div className="bg-[#1a1a2e] border-2 border-[#6272f1] p-6 rounded-xl space-y-4 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6272f1] uppercase tracking-wider bg-[#6272f1]/10 px-2.5 py-1 rounded">
              Active Recall Review
            </span>
            <button
              onClick={() => setReviewingItem(null)}
              className="text-gray-400 hover:text-white text-xs"
            >
              Cancel
            </button>
          </div>

          <div>
            <h2 className="text-xl font-bold text-white">{reviewingItem.problem_title}</h2>
            <p className="text-gray-400 text-xs mt-1">
              Platform: {reviewingItem.platform.toUpperCase()} • Current Interval: {reviewingItem.interval_days} day(s) • Ease Factor: {reviewingItem.ease_factor}
            </p>
          </div>

          <div className="flex gap-2">
            <a
              href={reviewingItem.url || '#'}
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2 bg-[#0f0f1a] hover:bg-[#252540] border border-[#2a2a4a] text-xs font-semibold text-white rounded-lg flex items-center gap-1.5 transition-colors"
            >
              Open Problem Code <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          <div className="border-t border-[#2a2a4a] pt-4">
            <span className="text-xs font-semibold text-gray-300 block mb-2.5">
              How well did you recall the pattern & approach?
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              <button
                onClick={() => handleReview(0)}
                className="p-3 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold text-center transition-all"
              >
                Again (0)
                <span className="block text-[10px] text-gray-400 font-normal mt-0.5">Forgot approach</span>
              </button>

              <button
                onClick={() => handleReview(3)}
                className="p-3 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-400 rounded-lg text-xs font-semibold text-center transition-all"
              >
                Hard (3)
                <span className="block text-[10px] text-gray-400 font-normal mt-0.5">Recalled with effort</span>
              </button>

              <button
                onClick={() => handleReview(4)}
                className="p-3 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 rounded-lg text-xs font-semibold text-center transition-all"
              >
                Good (4)
                <span className="block text-[10px] text-gray-400 font-normal mt-0.5">Optimal recall</span>
              </button>

              <button
                onClick={() => handleReview(5)}
                className="p-3 bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-400 rounded-lg text-xs font-semibold text-center transition-all"
              >
                Easy (5)
                <span className="block text-[10px] text-gray-400 font-normal mt-0.5">Instant intuition</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Due Today Queue */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-amber-400" />
            Due for Revision Today ({dueItems.length})
          </h2>
        </div>

        {dueItems.length === 0 ? (
          <div className="p-8 text-center text-gray-500 bg-[#1a1a2e] rounded-xl border border-[#2a2a4a] text-sm">
            🎉 All set! No problems are due for revision today.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {dueItems.map((item) => (
              <div
                key={item.id}
                className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                        item.is_overdue
                          ? 'text-red-400 bg-red-500/15'
                          : 'text-amber-400 bg-amber-500/15'
                      }`}
                    >
                      {item.is_overdue ? 'Overdue' : 'Due Today'}
                    </span>
                    <span className="text-[10px] text-gray-500">
                      Reps: {item.repetition_count}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-white">{item.problem_title}</h3>
                  <span className="text-xs text-gray-400">
                    Ease: {item.ease_factor} • Interval: {item.interval_days}d
                  </span>
                </div>

                <button
                  onClick={() => setReviewingItem(item)}
                  className="px-3.5 py-2 bg-[#6272f1] hover:bg-[#4f56e5] text-white rounded-lg text-xs font-semibold transition-all shadow-md shadow-[#6272f1]/20"
                >
                  Review
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upcoming Queue */}
      <div className="space-y-3 pt-4 border-t border-[#2a2a4a]">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Calendar className="w-5 h-5 text-gray-400" />
          Scheduled Upcoming Reviews ({upcomingItems.length})
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {upcomingItems.map((item) => (
            <div
              key={item.id}
              className="bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl flex flex-col justify-between"
            >
              <div>
                <span className="text-[10px] text-gray-400 font-semibold block mb-1">
                  Due: {item.due_date}
                </span>
                <h4 className="text-xs font-semibold text-white">{item.problem_title}</h4>
              </div>
              <div className="mt-3 text-[11px] text-gray-500 flex items-center justify-between">
                <span>Reps: {item.repetition_count}</span>
                <span>Interval: {item.interval_days}d</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
