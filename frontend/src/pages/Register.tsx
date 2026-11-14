import { useState, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { authAPI } from '../api/auth';
import { useAuthStore } from '../store/authStore';

const EXPERIENCE_LEVELS = [
  { value: 'beginner', label: 'Beginner — just starting DSA' },
  { value: 'intermediate', label: 'Intermediate — familiar with basics' },
  { value: 'advanced', label: 'Advanced — solid DSA foundation' },
];

const LEARNING_GOALS = [
  { value: 'placement', label: 'Campus Placement Preparation' },
  { value: 'interview', label: 'Technical Interview Preparation' },
  { value: 'competitive', label: 'Competitive Programming' },
  { value: 'fundamentals', label: 'DSA Fundamentals' },
  { value: 'advanced', label: 'Advanced Problem Solving' },
];

const LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
];

export function Register() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    experience_level: 'beginner',
    learning_goal: 'interview',
    preferred_language: 'python',
  });
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.password) { toast.error('Please fill in all required fields'); return; }
    if (form.password.length < 8) { toast.error('Password must be at least 8 characters'); return; }
    setLoading(true);
    try {
      const { data } = await authAPI.register(form);
      setAuth(data.user, data.access_token, data.refresh_token);
      toast.success(`Welcome to DSAURA, ${data.user.name}!`);
      navigate('/dashboard');
    } catch (err: any) {
      if (err?.response?.status === 404 || err?.code === 'ERR_NETWORK') {
        toast.error('API server unreachable. Ensure backend is deployed or check connection.');
      } else {
        toast.error(err?.response?.data?.detail || 'Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f0f1a] flex items-center justify-center p-4 py-10">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-[#6272f1]/5 rounded-full blur-3xl pointer-events-none" />
      <div className="relative w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2.5 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-[#6272f1] to-[#4044cb] rounded-xl flex items-center justify-center">
              <span className="text-white font-black text-lg">D</span>
            </div>
            <span className="text-white font-bold text-2xl">DSAURA</span>
          </Link>
          <h1 className="text-2xl font-bold text-white mb-1">Create your account</h1>
          <p className="text-gray-400 text-sm">Start understanding your DSA journey</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-2xl p-6 space-y-4"
        >
          <div>
            <label className="label">Full Name *</label>
            <input type="text" value={form.name} onChange={set('name')} placeholder="Alex Kumar" className="input" />
          </div>

          <div>
            <label className="label">Email *</label>
            <input type="email" value={form.email} onChange={set('email')} placeholder="you@example.com" className="input" />
          </div>

          <div>
            <label className="label">Password *</label>
            <div className="relative">
              <input
                type={showPw ? 'text' : 'password'}
                value={form.password}
                onChange={set('password')}
                placeholder="Min. 8 characters"
                className="input pr-10"
              />
              <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
                {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div>
            <label className="label">Experience Level</label>
            <select value={form.experience_level} onChange={set('experience_level')} className="input">
              {EXPERIENCE_LEVELS.map(({ value, label }) => <option key={value} value={value}>{label}</option>)}
            </select>
          </div>

          <div>
            <label className="label">Learning Goal</label>
            <select value={form.learning_goal} onChange={set('learning_goal')} className="input">
              {LEARNING_GOALS.map(({ value, label }) => <option key={value} value={value}>{label}</option>)}
            </select>
          </div>

          <div>
            <label className="label">Preferred Language</label>
            <select value={form.preferred_language} onChange={set('preferred_language')} className="input">
              {LANGUAGES.map(({ value, label }) => <option key={value} value={value}>{label}</option>)}
            </select>
          </div>

          <button type="submit" disabled={loading} className="w-full btn-primary justify-center py-2.5 mt-2">
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-400 mt-5">
          Already have an account?{' '}
          <Link to="/login" className="text-[#6272f1] hover:text-[#8197f8] font-medium">Sign In</Link>
        </p>
      </div>
    </div>
  );
}
