import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';
import { StudentProfile } from '../../types';

interface Props {
  profile: StudentProfile;
}

function getSpectrumLabel(axis: string, value: number): string {
  const labels: Record<string, [string, string]> = {
    EI: ['E', 'I'],
    SN: ['S', 'N'],
    TF: ['T', 'F'],
    JP: ['J', 'P'],
  };
  const [left, right] = labels[axis];
  if (value <= 25) return `강한 ${left}`;
  if (value <= 50) return `약한 ${left}`;
  if (value <= 75) return `약한 ${right}`;
  return `강한 ${right}`;
}

function getSpectrumColor(value: number): string {
  if (value <= 25 || value >= 75) return 'bg-blue-600';
  return 'bg-blue-400';
}

export default function ProfileSection({ profile }: Props) {
  const hollandData = [
    { type: '현실형(R)', value: profile.holland?.R || 0 },
    { type: '탐구형(I)', value: profile.holland?.I || 0 },
    { type: '예술형(A)', value: profile.holland?.A || 0 },
    { type: '사회형(S)', value: profile.holland?.S || 0 },
    { type: '진취형(E)', value: profile.holland?.E || 0 },
    { type: '관습형(C)', value: profile.holland?.C || 0 },
  ];

  const mbtiAxes = [
    { key: 'EI' as const, left: 'E (외향)', right: 'I (내향)' },
    { key: 'SN' as const, left: 'S (감각)', right: 'N (직관)' },
    { key: 'TF' as const, left: 'T (사고)', right: 'F (감정)' },
    { key: 'JP' as const, left: 'J (판단)', right: 'P (인식)' },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6">📊 나의 프로필</h2>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Holland 레이더 차트 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3 text-center">Holland 흥미 유형</h3>
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={hollandData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="type" tick={{ fontSize: 11 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Radar
                name="나의 점수"
                dataKey="value"
                stroke="#2563eb"
                fill="#2563eb"
                fillOpacity={0.3}
              />
            </RadarChart>
          </ResponsiveContainer>
          <p className="text-center text-sm text-gray-500 mt-2">
            상위 유형:{' '}
            <span className="font-semibold text-blue-600">
              {hollandData
                .sort((a, b) => b.value - a.value)
                .slice(0, 3)
                .map((d) => d.type)
                .join(' > ')}
            </span>
          </p>
          <div className="grid grid-cols-3 gap-2 mt-3">
            {[...hollandData].sort((a, b) => b.value - a.value).map((d) => (
              <div key={d.type} className="text-center text-xs bg-gray-50 rounded py-1">
                <span className="text-gray-500">{d.type}</span>
                <span className="ml-1 font-semibold text-blue-600">{d.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* MBTI 스펙트럼 바 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3 text-center">MBTI 스펙트럼</h3>
          <div className="space-y-5 mt-4">
            {mbtiAxes.map(({ key, left, right }) => {
              const value = profile.mbti?.[key] || 50;
              return (
                <div key={key}>
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>{left}</span>
                    <span className="font-semibold text-blue-600">
                      {getSpectrumLabel(key, value)} ({value})
                    </span>
                    <span>{right}</span>
                  </div>
                  <div className="relative h-3 bg-gray-200 rounded-full">
                    <div
                      className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full transition-all"
                      style={{ width: `${value}%` }}
                    />
                    <div
                      className={`absolute top-1/2 -translate-y-1/2 w-4 h-4 ${getSpectrumColor(value)} rounded-full border-2 border-white shadow`}
                      style={{ left: `calc(${value}% - 8px)` }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-gray-300 mt-0.5">
                    <span>0</span>
                    <span>25</span>
                    <span>50</span>
                    <span>75</span>
                    <span>100</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
