import { RoadmapItem } from '../../types';

interface Props {
  roadmap: RoadmapItem[];
}

const gradeColors = [
  'border-blue-400 bg-blue-50',
  'border-emerald-400 bg-emerald-50',
  'border-purple-400 bg-purple-50',
];

export default function RoadmapSection({ roadmap }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-2">📚 맞춤형 교육과정 로드맵</h2>
      <p className="text-sm text-gray-500 mb-6">
        목표 진로 달성을 위한 학년별 추천 교육과정입니다.
      </p>

      <div className="relative">
        {/* 타임라인 선 */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200" />

        <div className="space-y-6">
          {roadmap.map((item, idx) => (
            <div key={item.grade} className="relative pl-14">
              {/* 타임라인 도트 */}
              <div className="absolute left-4 top-4 w-5 h-5 bg-blue-600 rounded-full border-4 border-white shadow z-10" />

              <div className={`border-l-4 ${gradeColors[idx]} rounded-xl p-5`}>
                {/* 학년 & 목표 */}
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-lg font-bold text-gray-900">{item.grade}</span>
                  <span className="text-sm text-gray-500 bg-white px-2 py-0.5 rounded">
                    🎯 {item.goal}
                  </span>
                </div>

                {/* 추천 교과 */}
                <div className="mb-3">
                  <p className="text-xs font-medium text-gray-500 mb-1">📖 추천 교과목</p>
                  <div className="flex flex-wrap gap-1.5">
                    {item.subjects.map((subject) => (
                      <span
                        key={subject}
                        className="text-xs bg-white px-2 py-1 rounded border border-gray-200 text-gray-700"
                      >
                        {subject}
                      </span>
                    ))}
                  </div>
                </div>

                {/* 추천 비교과 */}
                <div>
                  <p className="text-xs font-medium text-gray-500 mb-1">🏆 추천 활동</p>
                  <ul className="space-y-0.5">
                    {item.activities.map((activity, i) => (
                      <li key={i} className="text-sm text-gray-700">
                        • {activity}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
