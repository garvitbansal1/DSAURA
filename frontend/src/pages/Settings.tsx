import { useState } from 'react';
import { Settings as SettingsIcon, User, Save, Shield, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';
import { authAPI } from '../api/auth';

export function Settings() {
  const user = useAuthStore((s) => s.user);
  const updateUser = useAuthStore((s) => s.updateUser);

  const [name, setName] = useState(user?.name || '');
  const [learningGoal, setLearningGoal] = useState(user?.learning_goal || 'placement');
  const [preferredLang, setPreferredLang] = useState(user?.preferred_language || 'python');
  const [experienceLevel, setExperienceLevel] = useState(user?.experience_level || 'intermediate');
  const [saving, setSaving] = useState(false);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      const updated = await authAPI.updateMe({
        name,
        learning_goal: learningGoal,
        preferred_language: preferredLang,
        experience_level: experienceLevel,
      });
      updateUser(updated.data);
      toast.success('Settings updated successfully');
    } catch {
      toast.error('Failed to update settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-[#6272f1]" />
          Account & Learning Preferences
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Customize your learning goals, target programming language, and experience level.
        </p>
      </div>

      {/* Settings Form */}
      <form onSubmit={handleSave} className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-6">
        <div>
          <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
            required
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Email Address (Read-Only)
          </label>
          <input
            type="email"
            value={user?.email || ''}
            disabled
            className="w-full bg-[#0f0f1a]/50 border border-[#2a2a4a] rounded-lg px-4 py-2.5 text-sm text-gray-500 cursor-not-allowed"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
              Primary Learning Goal
            </label>
            <select
              value={learningGoal}
              onChange={(e) => setLearningGoal(e.target.value as any)}
              className="w-full bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
            >
              <option value="placement">Campus Placement Preparation</option>
              <option value="interview">Tech Company Interviews</option>
              <option value="competitive">Competitive Programming</option>
              <option value="fundamentals">DSA Fundamentals</option>
              <option value="advanced">Advanced Problem Solving</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
              Preferred Language for Templates
            </label>
            <select
              value={preferredLang}
              onChange={(e) => setPreferredLang(e.target.value as any)}
              className="w-full bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
            >
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Coding Experience Level
          </label>
          <select
            value={experienceLevel}
            onChange={(e) => setExperienceLevel(e.target.value as any)}
            className="w-full bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
          >
            <option value="beginner">Beginner — Just starting DSA</option>
            <option value="intermediate">Intermediate — Familiar with basic data structures</option>
            <option value="advanced">Advanced — Solid algorithmic foundation</option>
          </select>
        </div>

        <div className="pt-4 border-t border-[#2a2a4a] flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 bg-[#6272f1] hover:bg-[#4f56e5] text-white text-xs font-semibold rounded-lg flex items-center gap-2 transition-all shadow-md shadow-[#6272f1]/20 disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving Changes...' : 'Save Preferences'}
          </button>
        </div>
      </form>
    </div>
  );
}
