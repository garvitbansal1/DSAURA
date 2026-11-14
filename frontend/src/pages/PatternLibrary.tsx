import { useEffect, useState } from 'react';
import {
  BookOpen, Search, Code2, Clock, Cpu,
  AlertTriangle, ChevronRight, ExternalLink, Sparkles
} from 'lucide-react';
import { knowledgeAPI } from '../api/knowledge';
import type { DSATopicItem, DSAPatternItem, ProblemSummaryItem } from '../api/knowledge';

export function PatternLibrary() {
  const [topics, setTopics] = useState<DSATopicItem[]>([]);
  const [patterns, setPatterns] = useState<DSAPatternItem[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>('all');
  const [selectedPattern, setSelectedPattern] = useState<DSAPatternItem | null>(null);
  const [relatedProblems, setRelatedProblems] = useState<ProblemSummaryItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'python' | 'java' | 'pseudocode'>('python');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [topData, patData] = await Promise.all([
          knowledgeAPI.getTopics(),
          knowledgeAPI.getPatterns(),
        ]);
        setTopics(topData);
        setPatterns(patData);
        if (patData.length > 0) {
          setSelectedPattern(patData[0]);
          loadProblems(patData[0].id);
        }
      } catch (err) {
        console.error('Failed to load patterns', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  async function loadProblems(patternId: string) {
    try {
      const probs = await knowledgeAPI.getPatternProblems(patternId);
      setRelatedProblems(probs);
    } catch {
      setRelatedProblems([]);
    }
  }

  const handleSelectPattern = (pat: DSAPatternItem) => {
    setSelectedPattern(pat);
    loadProblems(pat.id);
  };

  const filteredPatterns = patterns.filter((p) => {
    const matchesTopic = selectedTopic === 'all' || p.topic_id === selectedTopic;
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.explanation?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.recognition_clues?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesTopic && matchesSearch;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Loading Pattern Library...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-[#6272f1]" />
          DSA Pattern Library
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Explore architectural problem-solving patterns with language templates, complexity analysis, and recognition heuristics.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-[#1a1a2e] border border-[#2a2a4a] p-4 rounded-xl">
        <div className="relative md:col-span-2">
          <Search className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search patterns, recognition clues, keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
          />
        </div>

        <select
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
          className="bg-[#0f0f1a] border border-[#2a2a4a] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-[#6272f1]"
        >
          <option value="all">All Topics ({patterns.length} patterns)</option>
          {topics.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name} ({t.patterns.length})
            </option>
          ))}
        </select>
      </div>

      {/* Main split: Patterns List + Pattern Detail Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Pattern Cards */}
        <div className="lg:col-span-5 space-y-2.5 max-h-[750px] overflow-y-auto pr-1">
          {filteredPatterns.length === 0 ? (
            <div className="p-8 text-center text-gray-500 bg-[#1a1a2e] rounded-xl border border-[#2a2a4a]">
              No patterns matched your search.
            </div>
          ) : (
            filteredPatterns.map((pat) => {
              const isSelected = selectedPattern?.id === pat.id;
              return (
                <div
                  key={pat.id}
                  onClick={() => handleSelectPattern(pat)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-[#6272f1]/15 border-[#6272f1] shadow-lg shadow-[#6272f1]/10'
                      : 'bg-[#1a1a2e] border-[#2a2a4a] hover:border-[#6272f1]/50'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-white text-sm flex items-center gap-1.5">
                        {pat.name}
                        {isSelected && <ChevronRight className="w-4 h-4 text-[#6272f1]" />}
                      </h3>
                      <p className="text-gray-400 text-xs mt-1 line-clamp-2">
                        {pat.explanation || 'Reusable algorithmic template'}
                      </p>
                    </div>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-medium border uppercase ${
                        pat.difficulty_level === 'easy'
                          ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                          : pat.difficulty_level === 'hard'
                          ? 'text-red-400 bg-red-500/10 border-red-500/20'
                          : 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                      }`}
                    >
                      {pat.difficulty_level || 'medium'}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 mt-3 text-[11px] text-gray-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-gray-500" />
                      {pat.time_complexity || 'O(n)'}
                    </span>
                    <span className="flex items-center gap-1">
                      <Cpu className="w-3 h-3 text-gray-500" />
                      {pat.space_complexity || 'O(1)'}
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right Column: In-Depth Pattern Inspector */}
        <div className="lg:col-span-7">
          {selectedPattern ? (
            <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-6 space-y-6">
              {/* Pattern Header */}
              <div className="border-b border-[#2a2a4a] pb-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white flex items-center gap-2">
                    {selectedPattern.name}
                  </h2>
                  <span
                    className={`text-xs px-2.5 py-1 rounded font-semibold border uppercase ${
                      selectedPattern.difficulty_level === 'easy'
                        ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                        : selectedPattern.difficulty_level === 'hard'
                        ? 'text-red-400 bg-red-500/10 border-red-500/20'
                        : 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                    }`}
                  >
                    {selectedPattern.difficulty_level || 'medium'}
                  </span>
                </div>
                <p className="text-gray-300 text-sm mt-2 leading-relaxed">
                  {selectedPattern.explanation}
                </p>
              </div>

              {/* Heuristics: When to use & Clues */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedPattern.when_to_use && (
                  <div className="bg-[#0f0f1a] border border-[#2a2a4a] p-3.5 rounded-lg">
                    <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" /> When to Use
                    </h4>
                    <p className="text-gray-300 text-xs leading-relaxed">
                      {selectedPattern.when_to_use}
                    </p>
                  </div>
                )}

                {selectedPattern.recognition_clues && (
                  <div className="bg-[#0f0f1a] border border-[#2a2a4a] p-3.5 rounded-lg">
                    <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5" /> Recognition Clues
                    </h4>
                    <p className="text-gray-300 text-xs leading-relaxed">
                      {selectedPattern.recognition_clues}
                    </p>
                  </div>
                )}
              </div>

              {/* Complexity Metrics */}
              <div className="flex items-center gap-6 bg-[#0f0f1a] border border-[#2a2a4a] px-4 py-2.5 rounded-lg text-xs">
                <div>
                  <span className="text-gray-500 block">Time Complexity</span>
                  <span className="text-emerald-400 font-mono font-medium">
                    {selectedPattern.time_complexity || 'O(n)'}
                  </span>
                </div>
                <div className="h-6 w-px bg-[#2a2a4a]" />
                <div>
                  <span className="text-gray-500 block">Space Complexity</span>
                  <span className="text-cyan-400 font-mono font-medium">
                    {selectedPattern.space_complexity || 'O(1)'}
                  </span>
                </div>
              </div>

              {/* Code Templates with Language Switcher */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Code2 className="w-3.5 h-3.5 text-[#6272f1]" /> Implementation Template
                  </span>

                  <div className="flex items-center gap-1 bg-[#0f0f1a] p-0.5 rounded-lg border border-[#2a2a4a]">
                    <button
                      onClick={() => setActiveTab('python')}
                      className={`text-xs px-2.5 py-1 rounded font-medium transition-all ${
                        activeTab === 'python'
                          ? 'bg-[#6272f1] text-white shadow'
                          : 'text-gray-400 hover:text-white'
                      }`}
                    >
                      Python
                    </button>
                    <button
                      onClick={() => setActiveTab('java')}
                      className={`text-xs px-2.5 py-1 rounded font-medium transition-all ${
                        activeTab === 'java'
                          ? 'bg-[#6272f1] text-white shadow'
                          : 'text-gray-400 hover:text-white'
                      }`}
                    >
                      Java
                    </button>
                    {selectedPattern.pseudocode && (
                      <button
                        onClick={() => setActiveTab('pseudocode')}
                        className={`text-xs px-2.5 py-1 rounded font-medium transition-all ${
                          activeTab === 'pseudocode'
                            ? 'bg-[#6272f1] text-white shadow'
                            : 'text-gray-400 hover:text-white'
                        }`}
                      >
                        Pseudocode
                      </button>
                    )}
                  </div>
                </div>

                <pre className="bg-[#0f0f1a] border border-[#2a2a4a] p-4 rounded-xl text-xs text-gray-200 font-mono overflow-x-auto max-h-72 leading-relaxed">
                  <code>
                    {activeTab === 'python'
                      ? selectedPattern.python_template || '# Python template coming soon'
                      : activeTab === 'java'
                      ? selectedPattern.java_template || '// Java template coming soon'
                      : selectedPattern.pseudocode || '// Pseudocode'}
                  </code>
                </pre>
              </div>

              {/* Curated Related Problems */}
              {relatedProblems.length > 0 && (
                <div className="border-t border-[#2a2a4a] pt-4">
                  <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2.5">
                    Curated Practice Problems ({relatedProblems.length})
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {relatedProblems.map((prob) => (
                      <a
                        key={prob.id}
                        href={prob.url || `https://leetcode.com/problems/${prob.slug}/`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center justify-between p-2.5 bg-[#0f0f1a] hover:bg-[#252540] border border-[#2a2a4a] rounded-lg transition-colors group"
                      >
                        <div className="truncate pr-2">
                          <span className="text-xs text-white group-hover:text-[#6272f1] transition-colors font-medium">
                            {prob.title}
                          </span>
                        </div>
                        <div className="flex items-center gap-1.5 shrink-0">
                          <span
                            className={`text-[10px] px-1.5 py-0.5 rounded font-medium uppercase ${
                              prob.difficulty === 'easy'
                                ? 'text-emerald-400 bg-emerald-500/10'
                                : prob.difficulty === 'hard'
                                ? 'text-red-400 bg-red-500/10'
                                : 'text-amber-400 bg-amber-500/10'
                            }`}
                          >
                            {prob.difficulty}
                          </span>
                          <ExternalLink className="w-3 h-3 text-gray-500 group-hover:text-[#6272f1]" />
                        </div>
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-12 text-center text-gray-500">
              Select a pattern to view in-depth implementation templates.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
