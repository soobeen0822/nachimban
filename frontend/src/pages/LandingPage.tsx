import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-emerald-50 px-4">
      <div className="text-center max-w-2xl">
        {/* 로고 & 서비스명 */}
        <div className="mb-8">
          <span className="text-6xl">🧭</span>
          <h1 className="text-4xl font-bold mt-4 text-gray-900">나침반</h1>
          <p className="text-sm text-gray-500 mt-2 tracking-wide">NACHIMBAN</p>
          <p className="text-xs text-gray-400 mt-1">
            Navigating Academic Careers through Holistic Intelligence
            <br />with Mined puBlic data And Networks
          </p>
        </div>

        {/* 설명 */}
        <p className="text-lg text-gray-700 mb-4">
          AI가 당신의 적성을 분석하고,
          <br />
          <span className="font-semibold text-blue-600">교육 공공데이터</span>를 기반으로
          <br />
          맞춤형 진로와 고등학교를 추천합니다.
        </p>

        <div className="flex flex-wrap justify-center gap-3 mb-8 text-sm text-gray-600">
          <span className="bg-white px-3 py-1 rounded-full shadow-sm">🔬 Holland 검사</span>
          <span className="bg-white px-3 py-1 rounded-full shadow-sm">🧠 MBTI 스펙트럼</span>
          <span className="bg-white px-3 py-1 rounded-full shadow-sm">📊 공공데이터 AI 매칭</span>
        </div>

        {/* CTA */}
        <button
          onClick={() => navigate('/assessment/goal')}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg px-8 py-4 rounded-xl shadow-lg transition-all hover:scale-105 cursor-pointer"
        >
          진로 탐색 시작하기 →
        </button>

        <p className="text-xs text-gray-400 mt-6">
          약 5~10분 소요 | 무료 | 회원가입 불필요
        </p>
      </div>

      {/* 하단 배지 */}
      <div className="absolute bottom-8 text-center text-xs text-gray-400">
        <p>교육공공데이터 AI 활용 대회 출품작</p>
        <p className="mt-1">활용 데이터: 학교알리미 · 커리어넷 · 워크넷 · 대학알리미</p>
      </div>
    </div>
  );
}
