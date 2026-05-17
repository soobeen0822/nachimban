import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { StudentProfile, HollandProfile } from '../types';

interface Props {
  profile: Partial<StudentProfile>;
  setProfile: React.Dispatch<React.SetStateAction<Partial<StudentProfile>>>;
}

const hollandQuestions = [
  // R - 현실형
  { code: 'R' as const, text: '기계나 도구를 다루는 활동을 좋아한다' },
  { code: 'R' as const, text: '야외 활동이나 신체를 사용하는 일을 선호한다' },
  { code: 'R' as const, text: '구체적이고 실용적인 결과물을 만드는 것이 좋다' },
  // I - 탐구형
  { code: 'I' as const, text: '새로운 것을 조사하고 연구하는 것이 재미있다' },
  { code: 'I' as const, text: '수학이나 과학 문제를 푸는 것을 좋아한다' },
  { code: 'I' as const, text: '현상의 원인과 원리를 알고 싶어한다' },
  // A - 예술형
  { code: 'A' as const, text: '글, 그림, 음악 등 창작 활동을 즐긴다' },
  { code: 'A' as const, text: '독창적인 아이디어를 떠올리는 것이 좋다' },
  { code: 'A' as const, text: '자유롭고 규칙에 얽매이지 않는 환경을 선호한다' },
  // S - 사회형
  { code: 'S' as const, text: '다른 사람을 돕거나 가르치는 일이 보람있다' },
  { code: 'S' as const, text: '사람들과 어울려 활동하는 것을 좋아한다' },
  { code: 'S' as const, text: '타인의 감정을 잘 이해하고 공감한다' },
  // E - 진취형
  { code: 'E' as const, text: '사람들을 이끌고 설득하는 것을 잘한다' },
  { code: 'E' as const, text: '경쟁에서 이기는 것이 동기부여가 된다' },
  { code: 'E' as const, text: '목표를 세우고 달성하는 과정이 즐겁다' },
  // C - 관습형
  { code: 'C' as const, text: '정리정돈하고 체계적으로 관리하는 것을 좋아한다' },
  { code: 'C' as const, text: '데이터나 숫자를 다루는 작업이 편하다' },
  { code: 'C' as const, text: '규칙과 절차를 따르는 것이 자연스럽다' },
];

export default function HollandTestPage({ profile, setProfile }: Props) {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [currentPage, setCurrentPage] = useState(0);
  const questionsPerPage = 6;
  const totalPages = Math.ceil(hollandQuestions.length / questionsPerPage);

  const handleAnswer = (questionIdx: number, value: number) => {
    setAnswers({ ...answers, [questionIdx]: value });
  };

  const calculateHolland = (): HollandProfile => {
    const scores: HollandProfile = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
    const counts: Record<string, number> = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };

    hollandQuestions.forEach((q, idx) => {
      if (answers[idx] !== undefined) {
        scores[q.code] += answers[idx];
        counts[q.code]++;
      }
    });

    // 각 유형별 평균을 0~100으로 변환 (각 유형 3문항, 각 1~5점)
    const result: HollandProfile = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
    for (const code of Object.keys(scores) as Array<keyof HollandProfile>) {
      if (counts[code] > 0) {
        result[code] = Math.round((scores[code] / (counts[code] * 5)) * 100);
      }
    }
    return result;
  };

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    } else {
      const hollandResult = calculateHolland();
      setProfile({ ...profile, holland: hollandResult });
      navigate('/assessment/mbti');
    }
  };

  const pageQuestions = hollandQuestions.slice(
    currentPage * questionsPerPage,
    (currentPage + 1) * questionsPerPage
  );

  const allAnswered = pageQuestions.every(
    (_, idx) => answers[currentPage * questionsPerPage + idx] !== undefined
  );

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8">
        {/* 진행 상태 */}
        <div className="flex items-center gap-2 mb-6">
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2">🔬 Holland 흥미 검사</h2>
        <p className="text-gray-600 mb-6 text-sm">
          각 문항이 나를 얼마나 잘 설명하는지 선택해주세요.
          <span className="text-gray-400 ml-1">({currentPage + 1}/{totalPages})</span>
        </p>

        <div className="space-y-5">
          {pageQuestions.map((q, idx) => {
            const globalIdx = currentPage * questionsPerPage + idx;
            return (
              <div key={globalIdx} className="border-b border-gray-100 pb-4">
                <p className="text-gray-800 mb-2 text-sm font-medium">{q.text}</p>
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map((v) => (
                    <button
                      key={v}
                      onClick={() => handleAnswer(globalIdx, v)}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium transition cursor-pointer ${
                        answers[globalIdx] === v
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {v === 1 ? '전혀' : v === 2 ? '조금' : v === 3 ? '보통' : v === 4 ? '꽤' : '매우'}
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        <div className="flex gap-3 mt-8">
          {currentPage > 0 && (
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              className="flex-1 py-3 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition cursor-pointer"
            >
              ← 이전
            </button>
          )}
          <button
            onClick={handleNext}
            disabled={!allAnswered}
            className={`flex-1 py-3 font-semibold rounded-lg transition cursor-pointer ${
              allAnswered
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            {currentPage < totalPages - 1 ? '다음 →' : 'MBTI 검사로 →'}
          </button>
        </div>
      </div>
    </div>
  );
}
