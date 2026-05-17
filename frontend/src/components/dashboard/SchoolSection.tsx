import { SchoolRecommendation } from '../../types';

interface Props {
  schools: SchoolRecommendation[];
  showAll: boolean;
  totalCount: number;
  onToggle: () => void;
}

function getTypeColor(type: string): string {
  switch (type) {
    case '과학고': return 'bg-purple-100 text-purple-700';
    case '외국어고': return 'bg-pink-100 text-pink-700';
    case '국제고': return 'bg-indigo-100 text-indigo-700';
    case '자율형사립고': return 'bg-cyan-100 text-cyan-700';
    case '특성화고': return 'bg-orange-100 text-orange-700';
    case '마이스터고': return 'bg-red-100 text-red-700';
    default: return 'bg-green-100 text-green-700';
  }
}

function isGeneralHigh(type: string): boolean {
  return type === '일반고';
}

export default function SchoolSection({ schools, showAll, totalCount, onToggle }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-2">🏫 추천 고등학교</h2>
      <p className="text-sm text-gray-500 mb-6">
        진로 목표에 맞는 교육과정을 운영하는 학교를 추천합니다.
      </p>

      <div className="space-y-4">
        {schools.map((school) => (
          <div
            key={school.rank}
            className="border border-gray-100 rounded-xl p-5 hover:shadow-md transition"
          >
            {/* 상단: 학교명 + 유형 + 적합도 */}
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-900">{school.name}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getTypeColor(school.type)}`}>
                    {school.type}
                  </span>
                </div>
              </div>
              <span className="text-sm font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                적합도 {school.matchScore}%
              </span>
            </div>

            {/* 추천 이유 */}
            <div className="mb-3">
              <p className="text-xs font-medium text-gray-500 mb-1">추천 이유</p>
              <ul className="space-y-0.5">
                {school.reasons.map((reason, i) => (
                  <li key={i} className="text-sm text-gray-700">
                    {i + 1}. {reason}
                  </li>
                ))}
              </ul>
            </div>

            {/* 학교 유형별 정보 */}
            {isGeneralHigh(school.type) ? (
              // 일반고: 주소 + 홈페이지
              <div className="bg-gray-50 rounded-lg p-3 text-sm space-y-1">
                {school.address && (
                  <div className="flex items-start gap-2">
                    <span className="text-gray-400 shrink-0">📍 주소:</span>
                    <span className="text-gray-700">{school.address}</span>
                  </div>
                )}
                <div className="flex items-start gap-2">
                  <span className="text-gray-400 shrink-0">🌐 홈페이지:</span>
                  <a
                    href={school.homepageUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {school.homepageUrl}
                  </a>
                </div>
              </div>
            ) : (
              // 비일반고: 홈페이지만
              <div className="bg-gray-50 rounded-lg p-3 text-sm space-y-1">
                <div className="flex items-start gap-2">
                  <span className="text-gray-400 shrink-0">🌐 홈페이지:</span>
                  <a
                    href={school.homepageUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {school.homepageUrl}
                  </a>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* 더보기 버튼 */}
      {totalCount > 3 && (
        <button
          onClick={onToggle}
          className="w-full mt-4 py-3 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition cursor-pointer"
        >
          {showAll ? '접기 ↑' : `더보기 (${totalCount - 3}개 학교 더 보기) ↓`}
        </button>
      )}
    </div>
  );
}
