import { Link } from 'react-router-dom';
import {
  Network, Brain, Sparkles, RotateCcw,
  ArrowRight, Zap, Target,
} from 'lucide-react';

const FEATURES = [
  {
    icon: Network,
    title: 'Interactive Knowledge Graph',
    desc: 'Visualize your DSA mastery as a live graph. See which topics you have mastered, which are partial, and what you have never explored.',
    color: 'text-[#6272f1]',
    bg: 'bg-[#6272f1]/10',
  },
  {
    icon: Brain,
    title: 'Evidence-Based Mastery Engine',
    desc: 'Five-dimensional mastery scoring: pattern coverage, independent solving, difficulty progression, diversity, and revision retention.',
    color: 'text-purple-400',
    bg: 'bg-purple-500/10',
  },
  {
    icon: Zap,
    title: 'Knowledge Gap Analysis',
    desc: 'Detect when you are stuck repeating the same pattern. Identifies what you are missing, not just what you have done.',
    color: 'text-yellow-400',
    bg: 'bg-yellow-500/10',
  },
  {
    icon: BookOpen2,
    title: 'Pattern Library',
    desc: '60+ DSA patterns with pseudocode, Java and Python templates, complexity analysis, and recognition clues.',
    color: 'text-green-400',
    bg: 'bg-green-500/10',
  },
  {
    icon: Sparkles,
    title: 'Smart Recommendations',
    desc: 'Context-aware problem recommendations based on your current mastery gaps, not random popular problems.',
    color: 'text-blue-400',
    bg: 'bg-blue-500/10',
  },
  {
    icon: RotateCcw,
    title: 'Spaced Repetition',
    desc: 'SM-2 based revision scheduling to maximize long-term retention of solved patterns.',
    color: 'text-orange-400',
    bg: 'bg-orange-500/10',
  },
];

const HOW_IT_WORKS = [
  { step: '01', title: 'Connect Your Profiles', desc: 'Link LeetCode, Codeforces, GeeksforGeeks, and HackerRank.' },
  { step: '02', title: 'Analyze Your History', desc: 'DSAURA classifies every problem by DSA topic and pattern.' },
  { step: '03', title: 'Measure Real Mastery', desc: 'Evidence-based scoring across 5 dimensions — not just problem counts.' },
  { step: '04', title: 'Learn What Matters', desc: 'Targeted recommendations, gap analysis, and spaced revision.' },
];

function BookOpen2(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} {...props}>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </svg>
  );
}

export function Landing() {
  return (
    <div className="min-h-screen bg-[#0f0f1a] text-white">
      {/* Navbar */}
      <header className="border-b border-[#2a2a4a] sticky top-0 bg-[#0f0f1a]/90 backdrop-blur z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-[#6272f1] to-[#4044cb] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">D</span>
            </div>
            <span className="text-white font-bold text-xl">DSAURA</span>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm text-gray-400">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#how" className="hover:text-white transition-colors">How it works</a>
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/login" className="text-sm text-gray-300 hover:text-white px-4 py-2 rounded-lg hover:bg-[#1a1a2e] transition-colors">
              Sign In
            </Link>
            <Link to="/register" className="btn-primary text-sm py-2">
              Get Started <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-24 pb-20 px-6 text-center relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[#6272f1]/5 rounded-full blur-3xl pointer-events-none" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-[#6272f1]/10 border border-[#6272f1]/20 text-[#6272f1] text-xs font-medium px-3 py-1.5 rounded-full mb-6">
            <Zap className="w-3 h-3" />
            Evidence-Based DSA Learning Intelligence
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold leading-tight mb-6">
            Don&apos;t just solve problems.{' '}
            <span className="bg-gradient-to-r from-[#6272f1] to-[#8197f8] bg-clip-text text-transparent">
              Understand what you&apos;ve mastered.
            </span>
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            DSAURA connects your coding profiles, analyzes your DSA problem-solving history,
            identifies real knowledge gaps, and tells you exactly what to learn next.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/register" className="btn-primary text-base px-6 py-3">
              Start for Free <ArrowRight className="w-5 h-5" />
            </Link>
            <Link to="/login" className="btn-outline text-base px-6 py-3 rounded-lg">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <section className="border-y border-[#2a2a4a] py-8 px-6 bg-[#0d0d1f]">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {[
            { val: '28+', label: 'DSA Topics' },
            { val: '60+', label: 'Problem Patterns' },
            { val: '5', label: 'Mastery Dimensions' },
            { val: '4', label: 'Platform Integrations' },
          ].map(({ val, label }) => (
            <div key={label}>
              <div className="text-3xl font-bold text-[#6272f1]">{val}</div>
              <div className="text-gray-400 text-sm mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* The Problem section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-2xl p-8 md:p-12">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-10 h-10 rounded-lg bg-yellow-500/10 flex items-center justify-center flex-shrink-0">
                <Target className="w-5 h-5 text-yellow-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-3">The Problem With Traditional Practice</h2>
                <p className="text-gray-400 leading-relaxed">
                  Most developers track their progress by <span className="text-white font-medium">problem count</span> alone.
                  But solving 200 LeetCode problems does not mean you understand 200 concepts — it often means you have
                  practiced the same 10 patterns 20 times each.
                </p>
              </div>
            </div>
            <div className="grid md:grid-cols-3 gap-4 mt-8">
              {[
                { label: 'What you think', val: '200 problems solved', color: 'text-green-400', bg: 'bg-green-500/10' },
                { label: 'What actually happened', val: 'Same 5 patterns, 40x each', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
                { label: 'What DSAURA shows', val: 'Real pattern gaps & mastery', color: 'text-[#6272f1]', bg: 'bg-[#6272f1]/10' },
              ].map(({ label, val, color, bg }) => (
                <div key={label} className={`${bg} border border-[#2a2a4a] rounded-xl p-4`}>
                  <div className="text-gray-500 text-xs mb-1">{label}</div>
                  <div className={`font-semibold ${color}`}>{val}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6 bg-[#0d0d1f]">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold mb-4">Everything you need to learn DSA intelligently</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Built for developers who want to actually understand what they know — not just count how many problems they have attempted.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map(({ icon: Icon, title, desc, color, bg }) => (
              <div key={title} className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-6 hover:border-[#6272f1]/30 transition-all">
                <div className={`w-10 h-10 ${bg} rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className={`w-5 h-5 ${color}`} />
                </div>
                <h3 className="font-semibold text-white mb-2">{title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold mb-4">How DSAURA Works</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            {HOW_IT_WORKS.map(({ step, title, desc }) => (
              <div key={step} className="flex gap-4 bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-6">
                <div className="text-3xl font-black text-[#6272f1]/30 flex-shrink-0 leading-none">{step}</div>
                <div>
                  <h3 className="font-semibold text-white mb-1">{title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-gradient-to-b from-[#0d0d1f] to-[#0f0f1a]">
        <div className="max-w-2xl mx-auto text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-[#6272f1] to-[#4044cb] rounded-2xl flex items-center justify-center mx-auto mb-6">
            <span className="text-white font-black text-2xl">D</span>
          </div>
          <h2 className="text-3xl font-bold mb-4">Start Understanding Your DSA Journey</h2>
          <p className="text-gray-400 mb-8">
            Connect your profiles, let DSAURA analyze your history, and get a clear picture of where you stand — for free.
          </p>
          <Link to="/register" className="btn-primary text-base px-8 py-3">
            Create Your Account <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#2a2a4a] py-8 px-6 text-center text-gray-500 text-sm">
        <div className="flex items-center justify-center gap-2 mb-2">
          <div className="w-5 h-5 bg-gradient-to-br from-[#6272f1] to-[#4044cb] rounded flex items-center justify-center">
            <span className="text-white font-bold text-[9px]">D</span>
          </div>
          <span className="text-white font-semibold">DSAURA</span>
        </div>
        <p>Intelligent DSA Learning &amp; Knowledge Assessment Platform</p>
        <p className="mt-1 text-xs">Mastery scores are estimates based on available evidence, not certified assessments.</p>
      </footer>
    </div>
  );
}
