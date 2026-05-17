import { CareerRecommendation } from '../../types';

interface CareerItem {
  rank: number;
  career: string;
  matchScore: number;
  reason: string;
  relatedJobs: string[];
  relatedMajors: string[];
  jobSum?: string;
}

interface Props {
  recommendations: CareerItem[];
}

function getScoreColor(score: number): string {
  if (score >= 90) return 'text-green-600 bg-green-100';
  if (score >= 80) return 'text-blue-600 bg-blue-100';
  if (score >= 70) return 'text-yellow-600 bg-yellow-100';
  return 'text-gray-600 bg-gray-100';
}

export default function CareerSection({ recommendations }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-2">🎯 AI 추천 진로 Top 5</h2>
      <p className="text-sm text-gray-500 mb-6">
        Holland 검사 + MBTI 스펙트럼 + 교육 공공데이터를 종합 분석한 결과입니다.
      </p>

      <div className="space-y-4">
        {recommendations.map((rec) => (
          <div
            key={rec.rank}
            className="border border-gray-100 rounded-xl p-4 hover:shadow-md transition"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-2xl font-bold text-gray-300">
                  {rec.rank}
                </span>
                <div>
                  <h3 className="font-semibold text-gray-900">{rec.career}</h3>
                  {rec.jobSum && (
                    <p className="text-xs text-gray-500 mt-1 line-clamp-2">{rec.jobSum}</p>
                  )}
                  <p className="text-xs text-blue-600 mt-1">💡 {rec.reason}</p>
                </div>
              </div>
              <span
                className={`text-sm font-bold px-3 py-1 rounded-full ${getScoreColor(rec.matchScore)}`}
              >
                {rec.matchScore}%
              </span>
            </div>

            <div className="mt-3 flex flex-wrap gap-4 text-xs">
              <div>
                <span className="text-gray-400">관련 직업: </span>
                <span className="text-gray-600">{rec.relatedJobs.join(', ')}</span>
              </div>
              <div>
                <span className="text-gray-400">관련 학과: </span>
                <span className="text-gray-600">{rec.relatedMajors.join(', ')}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
