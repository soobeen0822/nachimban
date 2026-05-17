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
  // E-I 축 (8문항)
  { axis: 'EI', text: '모임에서 먼저 말을 거는 편이다 (아니다→그렇다)' },
  { axis: 'EI', text: '혼자 있는 시간이 충전이 된다' },
  { axis: 'EI', text: '새로운 사람을 만나는 것이 에너지를 소모한다' },
  { axis: 'EI', text: '조용한 환경에서 집중이 더 잘 된다' },
  { axis: 'EI', text: '깊은 대화를 넓은 교류보다 선호한다' },
  { axis: 'EI', text: '혼자 하는 활동이 그룹 활동보다 편하다' },
  { axis: 'EI', text: '발표나 토론보다 글로 의견을 전달하는 게 낫다' },
  { axis: 'EI', text: '대화보다 생각을 먼저 정리하는 편이다' },
  // S-N 축 (8문항)
  { axis: 'SN', text: '경험하지 않은 가능성을 상상하는 것이 좋다' },
  { axis: 'SN', text: '디테일보다 큰 그림을 먼저 본다' },
  { axis: 'SN', text: '이론적인 토론이 실용적 활동보다 재미있다' },
  { axis: 'SN', text: '비유나 상징적 표현을 자주 사용한다' },
  { axis: 'SN', text: '미래의 가능성이 현재의 사실보다 흥미롭다' },
  { axis: 'SN', text: '정해진 방법보다 새로운 시도를 선호한다' },
  { axis: 'SN', text: '패턴이나 의미를 찾으려는 경향이 있다' },
  { axis: 'SN', text: '추상적인 개념에 대해 생각하는 것을 즐긴다' },
  // T-F 축 (8문항)
  { axis: 'TF', text: '결정할 때 논리보다 사람의 감정을 먼저 고려한다' },
  { axis: 'TF', text: '비판을 받으면 내용보다 말투가 먼저 신경쓰인다' },
  { axis: 'TF', text: '공정함보다 조화를 더 중요하게 여긴다' },
  { axis: 'TF', text: '다른 사람의 기분에 쉽게 영향을 받는다' },
  { axis: 'TF', text: '칭찬과 인정이 성과보다 동기부여가 된다' },
  { axis: 'TF', text: '갈등 상황에서 관계 유지를 우선시한다' },
  { axis: 'TF', text: '상대방 입장에서 먼저 생각하는 편이다' },
  { axis: 'TF', text: '감동적인 이야기에 쉽게 울컥한다' },
  // J-P 축 (8문항)
  { axis: 'JP', text: '계획 없이 즉흥적으로 행동하는 편이다' },
  { axis: 'JP', text: '마감 직전에 집중력이 올라간다' },
  { axis: 'JP', text: '여러 가지를 동시에 진행하는 것이 편하다' },
  { axis: 'JP', text: '변화와 새로운 상황에 잘 적응한다' },
  { axis: 'JP', text: '규칙보다 상황에 따라 유연하게 대응하는 편이다' },
  { axis: 'JP', text: '일정이 바뀌어도 크게 스트레스 받지 않는다' },
  { axis: 'JP', text: '선택지를 열어두는 것을 선호한다' },
  { axis: 'JP', text: '흥미로운 것이 생기면 기존 계획을 바꾸는 편이다' },
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
