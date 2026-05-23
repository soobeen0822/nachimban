import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { StudentProfile, MbtiSpectrum } from '../types';

interface Props {
  profile: Partial<StudentProfile>;
  setProfile: React.Dispatch<React.SetStateAction<Partial<StudentProfile>>>;
}

interface MbtiQuestion {
  axis: keyof MbtiSpectrum;
  text: string;
  // 높은 점수 = 축의 두번째 글자 방향 (I, N, F, P)
}

const mbtiQuestions: MbtiQuestion[] = [
  // E-I 축 (8문항) — 높을수록 I(내향)
  { axis: 'EI', text: '사람들과 어울린 후 혼자만의 시간으로 에너지를 회복한다' },
  { axis: 'EI', text: '팀 활동보다 혼자 하는 작업이 더 편하고 집중이 잘 된다' },
  { axis: 'EI', text: '새로운 사람을 많이 만나는 자리가 끝나면 지친 느낌이 든다' },
  { axis: 'EI', text: '말하기 전에 속으로 먼저 충분히 생각을 정리하는 편이다' },
  { axis: 'EI', text: '넓은 인맥보다 소수의 깊은 관계를 훨씬 더 선호한다' },
  { axis: 'EI', text: '혼자 조용히 집중하는 환경이 가장 편안하다' },
  { axis: 'EI', text: '즉석 발표나 토론보다 글이나 메시지로 의견 전달을 선호한다' },
  { axis: 'EI', text: '가능하면 전화 통화보다 문자나 메시지로 소통하는 편이다' },
  // S-N 축 (8문항) — 높을수록 N(직관)
  { axis: 'SN', text: '경험하지 않은 미래의 가능성을 상상하는 것이 즐겁다' },
  { axis: 'SN', text: '세부 사항보다 전체적인 맥락과 큰 그림을 먼저 파악한다' },
  { axis: 'SN', text: '실용적인 활동보다 이론이나 개념을 탐구하는 것이 더 재미있다' },
  { axis: 'SN', text: '직접적인 표현보다 비유나 은유로 설명하는 것이 자연스럽다' },
  { axis: 'SN', text: '현재 상황보다 앞으로의 가능성과 변화에 더 관심이 간다' },
  { axis: 'SN', text: '익숙한 방법보다 새로운 방식으로 문제를 해결하고 싶다' },
  { axis: 'SN', text: '데이터나 경험보다 직감이나 영감이 판단에 더 중요하게 작용한다' },
  { axis: 'SN', text: '반복적인 작업보다 새로운 아이디어를 탐색하는 것이 훨씬 좋다' },
  // T-F 축 (8문항) — 높을수록 F(감정)
  { axis: 'TF', text: '결정할 때 논리적 분석보다 감정과 가치관이 더 중요하게 느껴진다' },
  { axis: 'TF', text: '비판을 받으면 내용 자체보다 말하는 방식과 태도가 더 신경 쓰인다' },
  { axis: 'TF', text: '결과의 공정함보다 구성원 간의 관계와 조화를 더 우선시한다' },
  { axis: 'TF', text: '주변 사람의 감정 변화나 분위기를 쉽게 알아채는 편이다' },
  { axis: 'TF', text: '논리적인 평가보다 따뜻한 격려와 인정이 더 큰 동기부여가 된다' },
  { axis: 'TF', text: '갈등 상황에서 옳고 그름보다 관계 유지와 화합을 먼저 생각한다' },
  { axis: 'TF', text: '문제를 해결할 때 최선의 결과보다 상대방의 감정을 먼저 챙긴다' },
  { axis: 'TF', text: '슬프거나 감동적인 상황에서 타인의 감정에 쉽게 공감하고 영향받는다' },
  // J-P 축 (8문항) — 높을수록 P(인식)
  { axis: 'JP', text: '세밀한 계획보다 상황에 따라 즉흥적으로 결정하는 편이다' },
  { axis: 'JP', text: '마감 직전에 오히려 집중력이 더 잘 발휘된다' },
  { axis: 'JP', text: '하나의 일을 완전히 마치기 전에 여러 일을 동시에 진행하는 것이 자연스럽다' },
  { axis: 'JP', text: '예상치 못한 변화나 돌발 상황에도 유연하게 잘 적응하는 편이다' },
  { axis: 'JP', text: '정해진 규칙과 절차보다 상황에 따라 유연하게 대처하는 것이 더 편하다' },
  { axis: 'JP', text: '계획이 갑자기 바뀌어도 크게 불편하거나 스트레스받지 않는다' },
  { axis: 'JP', text: '최종 결정을 서두르기보다 여러 선택지를 열어두는 것을 선호한다' },
  { axis: 'JP', text: '흥미로운 새 활동이 생기면 기존 일정을 기꺼이 조정하는 편이다' },
];

function getSpectrumLabel(axis: string, value: number): string {
  const labels: Record<string, [string, string]> = {
    EI: ['E (외향)', 'I (내향)'],
    SN: ['S (감각)', 'N (직관)'],
    TF: ['T (사고)', 'F (감정)'],
    JP: ['J (판단)', 'P (인식)'],
  };
  const [left, right] = labels[axis];
  if (value <= 25) return `강한 ${left}`;
  if (value <= 50) return `약한 ${left}`;
  if (value <= 75) return `약한 ${right}`;
  return `강한 ${right}`;
}

export default function MbtiTestPage({ profile, setProfile }: Props) {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [currentPage, setCurrentPage] = useState(0);
  const questionsPerPage = 5;
  const totalPages = Math.ceil(mbtiQuestions.length / questionsPerPage);

  const handleAnswer = (questionIdx: number, value: number) => {
    setAnswers({ ...answers, [questionIdx]: value });
  };

  const calculateMbti = (): MbtiSpectrum => {
    const axisScores: Record<keyof MbtiSpectrum, number[]> = {
      EI: [],
      SN: [],
      TF: [],
      JP: [],
    };

    mbtiQuestions.forEach((q, idx) => {
      if (answers[idx] !== undefined) {
        // 1~7 척도 → 0~100 변환
        const normalized = ((answers[idx] - 1) / 6) * 100;
        axisScores[q.axis].push(normalized);
      }
    });

    const result: MbtiSpectrum = { EI: 50, SN: 50, TF: 50, JP: 50 };
    for (const axis of Object.keys(axisScores) as Array<keyof MbtiSpectrum>) {
      const scores = axisScores[axis];
      if (scores.length > 0) {
        result[axis] = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
      }
    }
    return result;
  };

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    } else {
      const mbtiResult = calculateMbti();
      setProfile({ ...profile, mbti: mbtiResult });
      navigate('/assessment/info');
    }
  };

  const pageQuestions = mbtiQuestions.slice(
    currentPage * questionsPerPage,
    (currentPage + 1) * questionsPerPage
  );

  const allAnswered = pageQuestions.every(
    (_, idx) => answers[currentPage * questionsPerPage + idx] !== undefined
  );

  // 현재까지 결과 미리보기
  const currentMbti = calculateMbti();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8">
        {/* 진행 상태 */}
        <div className="flex items-center gap-2 mb-6">
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2">🧠 MBTI 스펙트럼 검사</h2>
        <p className="text-gray-600 mb-6 text-sm">
          각 문항에 대해 나와 얼마나 가까운지 선택해주세요.
          <span className="text-gray-400 ml-1">({currentPage + 1}/{totalPages})</span>
        </p>

        <div className="space-y-6">
          {pageQuestions.map((q, idx) => {
            const globalIdx = currentPage * questionsPerPage + idx;
            return (
              <div key={globalIdx} className="border-b border-gray-100 pb-4">
                <p className="text-gray-800 mb-3 text-sm font-medium">{q.text}</p>
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5, 6, 7].map((v) => (
                    <button
                      key={v}
                      onClick={() => handleAnswer(globalIdx, v)}
                      className={`flex-1 py-2 rounded text-xs font-medium transition cursor-pointer ${
                        answers[globalIdx] === v
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                      }`}
                    >
                      {v}
                    </button>
                  ))}
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>전혀 아니다</span>
                  <span>매우 그렇다</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* 스펙트럼 미리보기 */}
        {Object.keys(answers).length > 0 && (
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-xs font-medium text-blue-700 mb-2">현재 스펙트럼 미리보기</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {(['EI', 'SN', 'TF', 'JP'] as const).map((axis) => (
                <span key={axis} className="text-blue-600">
                  {getSpectrumLabel(axis, currentMbti[axis])}
                </span>
              ))}
            </div>
          </div>
        )}

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
            {currentPage < totalPages - 1 ? '다음 →' : '추가 정보 입력 →'}
          </button>
        </div>
      </div>
    </div>
  );
}
