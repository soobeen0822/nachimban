import { StudentGoal, GoalComparison } from '../../types';

interface Props {
  goal: StudentGoal;
  comparison: GoalComparison;
}

function getVerdictColor(verdict: string): string {
  switch (verdict) {
    case '매우 높음': return 'text-green-600 bg-green-50';
    case '높음': return 'text-yellow-600 bg-yellow-50';
    case '보통': return 'text-orange-600 bg-orange-50';
    case '낮음': return 'text-red-600 bg-red-50';
    default: return 'text-gray-600 bg-gray-50';
  }
}

function getVerdictEmoji(verdict: string): string {
  switch (verdict) {
    case '매우 높음': return '🟢';
    case '높음': return '🟡';
    case '보통': return '🟠';
    case '낮음': return '🔴';
    default: return '⚪';
  }
}

export default function GoalComparisonSection({ goal, comparison }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">🎯 나의 목표 vs AI 추천 비교</h2>

      {/* 목표 요약 */}
      <div className="bg-gray-50 rounded-lg p-4 mb-4">
        <p className="text-sm text-gray-500 mb-2">나의 목표</p>
        <div className="flex flex-wrap gap-2">
          {goal.targetHighSchool && (
            <span className="bg-white px-3 py-1 rounded-full text-sm border">🏫 {goal.targetHighSchool}</span>
          )}
          {goal.targetUniversity && (
            <span className="bg-white px-3 py-1 rounded-full text-sm border">🎓 {goal.targetUniversity}</span>
          )}
          {goal.targetMajor && (
            <span className="bg-white px-3 py-1 rounded-full text-sm border">📚 {goal.targetMajor}</span>
          )}
          {goal.targetJob && (
            <span className="bg-white px-3 py-1 rounded-full text-sm border">💼 {goal.targetJob}</span>
          )}
        </div>
      </div>

      {/* 매칭도 */}
      <div className={`rounded-lg p-5 ${getVerdictColor(comparison.verdict)}`}>
        <div className="flex items-center justify-between mb-3">
          <span className="text-lg font-bold">
            {getVerdictEmoji(comparison.verdict)} 매칭도: {comparison.matchScore}%
          </span>
          <span className="text-sm font-semibold px-3 py-1 rounded-full bg-white/50">
            {comparison.verdict}
          </span>
        </div>
        <p className="text-sm">{comparison.message}</p>

        {/* 매칭도 바 */}
        <div className="mt-3 h-3 bg-white/50 rounded-full overflow-hidden">
          <div
            className="h-full bg-current rounded-full transition-all duration-1000"
            style={{ width: `${comparison.matchScore}%`, opacity: 0.7 }}
          />
        </div>
      </div>

      {/* 강점 & 보완점 */}
      <div className="grid md:grid-cols-2 gap-4 mt-4">
        <div className="bg-green-50 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-green-700 mb-2">✅ 강점</h4>
          <ul className="space-y-1">
            {comparison.strengths.map((s, i) => (
              <li key={i} className="text-sm text-green-800">• {s}</li>
            ))}
          </ul>
        </div>
        <div className="bg-amber-50 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-amber-700 mb-2">⚠️ 보완 포인트</h4>
          <ul className="space-y-1">
            {comparison.improvements.map((s, i) => (
              <li key={i} className="text-sm text-amber-800">• {s}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
