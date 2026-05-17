import { useState, useEffect } from 'react';
import { StudentProfile } from '../types';
import ProfileSection from '../components/dashboard/ProfileSection';
import CareerSection from '../components/dashboard/CareerSection';
import GoalComparisonSection from '../components/dashboard/GoalComparisonSection';
import SchoolSection from '../components/dashboard/SchoolSection';
import RoadmapSection from '../components/dashboard/RoadmapSection';
import { analyzeProfile, AnalyzeResponse } from '../services/api';

interface Props {
  profile: StudentProfile;
}

export default function ResultDashboard({ profile }: Props) {
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAllSchools, setShowAllSchools] = useState(false);

  useEffect(() => {
    async function fetchResult() {
      try {
        setLoading(true);
        const data = await analyzeProfile({
          holland: profile.holland || { R: 50, I: 50, A: 50, S: 50, E: 50, C: 50 },
          mbti: profile.mbti || { EI: 50, SN: 50, TF: 50, JP: 50 },
          goal: {
            hasGoal: profile.goal?.hasGoal || false,
            targetHighSchool: profile.goal?.targetHighSchool,
            targetUniversity: profile.goal?.targetUniversity,
            targetMajor: profile.goal?.targetMajor,
            targetJob: profile.goal?.targetJob,
          },
          region: profile.region || '',
          grade: profile.grade || '중3',
          gender: (profile as any).gender || '',
        });
        setResult(data);
      } catch (e) {
        setError('분석 중 오류가 발생했습니다. 서버 연결을 확인해주세요.');
        console.error(e);
      } finally {
        setLoading(false);
      }
    }

    fetchResult();
  }, [profile]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4 animate-spin">🧭</div>
          <p className="text-lg text-gray-700 font-medium">AI가 진로를 분석하고 있습니다...</p>
          <p className="text-sm text-gray-500 mt-2">교육 공공데이터 기반 매칭 중</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-2xl shadow-sm max-w-md">
          <p className="text-4xl mb-4">⚠️</p>
          <p className="text-gray-700">{error || '결과를 불러올 수 없습니다.'}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  // API 결과를 컴포넌트 props 형태로 변환
  const careerRecommendations = result.careers.map((c) => ({
    rank: c.rank,
    career: c.jobNm,
    matchScore: c.matchScore,
    reason: c.reason,
    relatedJobs: [c.jobLrclNm],
    relatedMajors: c.relatedMajors,
    jobSum: c.jobSum,
  }));

  const goalComparison = result.goalComparison
    ? {
        matchScore: result.goalComparison.matchScore,
        verdict: result.goalComparison.verdict as '매우 높음' | '높음' | '보통' | '낮음',
        message: result.goalComparison.message,
        strengths: result.goalComparison.strengths,
        improvements: result.goalComparison.improvements,
      }
    : null;

  const schoolRecommendations = result.schools.map((s, idx) => ({
    rank: idx + 1,
    name: s.name,
    type: s.type as any,
    matchScore: s.matchScore,
    reasons: s.reasons,
    homepageUrl: s.homepageUrl || '',
    address: s.type === '일반고' ? s.address : undefined,
    district: s.type === '일반고' ? s.region : undefined,
    admissionInfo: s.type !== '일반고' ? '상세 정보는 학교 홈페이지 참조' : undefined,
    admissionUrl: s.type !== '일반고' ? s.homepageUrl : undefined,
  }));

  const visibleSchools = showAllSchools
    ? schoolRecommendations
    : schoolRecommendations.slice(0, 3);

  const roadmap = result.roadmap.map((r) => ({
    grade: r.grade,
    goal: r.goal,
    subjects: r.subjects,
    activities: r.activities,
  }));

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* 헤더 */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">🧭 나침반 분석 결과</h1>
          <p className="text-gray-500 mt-2">AI가 교육 공공데이터를 기반으로 분석한 맞춤형 진로 리포트</p>
        </div>

        {/* 종합 의견 */}
        <div className="bg-gradient-to-r from-blue-50 to-emerald-50 rounded-2xl p-6 border border-blue-100">
          <h2 className="text-lg font-bold text-gray-900 mb-3">📋 종합 의견</h2>
          <p className="text-gray-700 leading-relaxed">
            분석 결과, <span className="font-semibold text-blue-700">{careerRecommendations[0]?.career}</span> 분야가
            가장 높은 적합도({careerRecommendations[0]?.matchScore}%)를 보였습니다.
            {goalComparison && (
              <> 입력하신 목표와의 매칭도는 <span className="font-semibold text-emerald-700">{goalComparison.matchScore}%({goalComparison.verdict})</span>입니다. </>
            )}
            추천 학과는 <span className="font-semibold">{careerRecommendations[0]?.relatedMajors.slice(0, 2).join(', ')}</span> 계열이며,
            거주지 인근 <span className="font-semibold">{visibleSchools[0]?.name}</span> 등에서 관련 교과목을 이수할 수 있습니다.
          </p>
          {goalComparison && !goalComparison.improvements.length && (
            <p className="text-emerald-600 text-sm mt-2 font-medium">
              ✨ 적성과 목표가 잘 맞으니, 자신감을 가지고 준비하세요!
            </p>
          )}
        </div>

        {/* 섹션 1: 프로필 시각화 */}
        <ProfileSection profile={profile} />

        {/* 섹션 2: 목표 비교 (목표 입력한 경우만) */}
        {profile.goal?.hasGoal && goalComparison && (
          <GoalComparisonSection goal={profile.goal} comparison={goalComparison} />
        )}

        {/* 섹션 3: 진로 추천 */}
        <CareerSection recommendations={careerRecommendations} />

        {/* 섹션 4: 고등학교 매칭 */}
        <SchoolSection
          schools={visibleSchools}
          showAll={showAllSchools}
          totalCount={schoolRecommendations.length}
          onToggle={() => setShowAllSchools(!showAllSchools)}
        />

        {/* 섹션 5: 교육과정 로드맵 */}
        <RoadmapSection roadmap={roadmap} />

        {/* 푸터 */}
        <div className="text-center text-xs text-gray-400 py-8 border-t border-gray-200">
          <p>본 결과는 교육 공공데이터 기반 AI 분석으로, 참고용입니다.</p>
          <p className="mt-1">
            활용 데이터: 나이스(NEIS) 학교정보 · 워크넷 직업정보
          </p>
          <p className="mt-1">나침반 (NACHIMBAN) ©2025</p>
        </div>
      </div>
    </div>
  );
}
