import { useEffect, useState } from 'react';
import {
  HelpCircle, CheckCircle2, XCircle, Award,
  ArrowRight, RotateCcw, AlertCircle, Sparkles
} from 'lucide-react';
import { masteryAPI } from '../api/mastery';

export function Assessment() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, []);

  async function loadQuestions() {
    try {
      setLoading(true);
      setResult(null);
      setAnswers({});
      const data = await masteryAPI.getAssessmentQuestions();
      setQuestions(data.questions || []);
    } catch (err) {
      console.error('Failed to load questions', err);
    } finally {
      setLoading(false);
    }
  }

  const handleSelect = (questionId: string, optionId: string) => {
    if (result) return; // Locked after submission
    setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      if (!confirm('You have unanswered questions. Are you sure you want to submit?')) {
        return;
      }
    }
    try {
      setSubmitting(true);
      const res = await masteryAPI.submitAssessment(answers);
      setResult(res);
    } catch (err) {
      console.error('Failed to submit assessment', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Preparing Knowledge Assessment Suite...
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <HelpCircle className="w-6 h-6 text-[#6272f1]" />
          DSA Pattern Recognition Assessment
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Test your conceptual understanding and pattern diagnosis ability on realistic DSA problem scenarios.
        </p>
      </div>

      {/* Result Card if submitted */}
      {result && (
        <div className="bg-[#1a1a2e] border border-[#2a2a4a] p-6 rounded-xl space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-[#6272f1]/15 border border-[#6272f1]/30 flex items-center justify-center text-[#6272f1]">
                <Award className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Assessment Completed</h2>
                <p className="text-gray-400 text-xs mt-0.5">
                  Score: <strong className="text-white">{result.score}</strong> / {result.total_questions} ({result.percentage}%)
                </p>
              </div>
            </div>

            <button
              onClick={loadQuestions}
              className="px-4 py-2 bg-[#0f0f1a] hover:bg-[#252540] border border-[#2a2a4a] text-xs font-semibold text-white rounded-lg flex items-center gap-1.5 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Retake Assessment
            </button>
          </div>

          <p className="text-gray-300 text-sm bg-[#0f0f1a] p-4 rounded-lg border border-[#2a2a4a]">
            {result.feedback}
          </p>
        </div>
      )}

      {/* Questions List */}
      <div className="space-y-6">
        {questions.map((q, idx) => {
          const selectedOptionId = answers[q.id];
          const evaluated = result?.breakdown?.find((b: any) => b.question_id === q.id);

          return (
            <div
              key={q.id}
              className={`bg-[#1a1a2e] border rounded-xl p-6 transition-all ${
                evaluated
                  ? evaluated.is_correct
                    ? 'border-emerald-500/50'
                    : 'border-red-500/50'
                  : 'border-[#2a2a4a]'
              }`}
            >
              {/* Question Meta */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#6272f1] bg-[#6272f1]/10 px-2.5 py-0.5 rounded border border-[#6272f1]/20">
                  Question {idx + 1} of {questions.length} • {q.topic}
                </span>

                <span className="text-[10px] uppercase font-semibold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                  {q.difficulty}
                </span>
              </div>

              {/* Scenario */}
              <div className="bg-[#0f0f1a] border border-[#2a2a4a] p-3.5 rounded-lg text-xs text-gray-300 leading-relaxed mb-4">
                <span className="text-gray-500 block text-[10px] uppercase font-semibold mb-1">
                  Scenario
                </span>
                {q.scenario}
              </div>

              {/* Question Text */}
              <h3 className="text-sm font-semibold text-white mb-4 leading-normal">
                {q.question}
              </h3>

              {/* Options */}
              <div className="space-y-2">
                {q.options.map((opt: any) => {
                  const isSelected = selectedOptionId === opt.id;
                  let optStyle = 'bg-[#0f0f1a] border-[#2a2a4a] text-gray-300 hover:bg-[#252540]';

                  if (isSelected && !evaluated) {
                    optStyle = 'bg-[#6272f1]/20 border-[#6272f1] text-white';
                  }

                  return (
                    <div
                      key={opt.id}
                      onClick={() => handleSelect(q.id, opt.id)}
                      className={`p-3 rounded-lg border text-xs cursor-pointer flex items-center justify-between transition-all ${optStyle}`}
                    >
                      <span>{opt.text}</span>
                      <span
                        className={`w-4 h-4 rounded-full border flex items-center justify-center text-[10px] ${
                          isSelected
                            ? 'border-[#6272f1] bg-[#6272f1] text-white'
                            : 'border-gray-600'
                        }`}
                      >
                        {isSelected && '✓'}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Explanation if evaluated */}
              {evaluated && (
                <div
                  className={`mt-4 p-3.5 rounded-lg border text-xs leading-relaxed ${
                    evaluated.is_correct
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-red-500/10 border-red-500/30 text-red-300'
                  }`}
                >
                  <div className="font-semibold mb-1 flex items-center gap-1.5">
                    {evaluated.is_correct ? (
                      <>
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Correct Analysis!
                      </>
                    ) : (
                      <>
                        <XCircle className="w-4 h-4 text-red-400" /> Incorrect
                      </>
                    )}
                  </div>
                  <p className="text-gray-300 text-xs mt-1">{evaluated.explanation}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Submit Button */}
      {!result && (
        <div className="pt-2 text-center">
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="px-8 py-3 bg-[#6272f1] hover:bg-[#4f56e5] disabled:opacity-50 text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-[#6272f1]/25 inline-flex items-center gap-2"
          >
            {submitting ? 'Evaluating...' : 'Submit Assessment & Analyze Mastery'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
