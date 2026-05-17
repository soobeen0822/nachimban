import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { StudentProfile, StudentGoal } from '../types';
import schoolList from '../data/schoolList.json';
import majorList from '../data/majorList.json';
import jobList from '../data/jobList.json';

interface Props {
  profile: Partial<StudentProfile>;
  setProfile: React.Dispatch<React.SetStateAction<Partial<StudentProfile>>>;
}

const HIGH_SCHOOLS: string[] = schoolList;
const MAJORS: string[] = majorList;
const JOBS: string[] = jobList;

function AutocompleteInput({
  label,
  placeholder,
  value,
  onChange,
  suggestions,
  strict = false,
}: {
  label: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
  suggestions: string[];
  strict?: boolean;
}) {
  const [query, setQuery] = useState(value);
  const [showDropdown, setShowDropdown] = useState(false);
  const [isValid, setIsValid] = useState(true);

  const filtered = query.length >= 1
    ? suggestions.filter((s) =>
        s.replace(/고등학교$/, '').includes(query.replace(/고등학교$/, '').replace(/고$/, ''))
      ).slice(0, 8)
    : [];

  const handleBlur = () => {
    setTimeout(() => {
      setShowDropdown(false);
      if (strict && query && !suggestions.includes(query)) {
        setIsValid(false);
      } else {
        setIsValid(true);
      }
    }, 200);
  };

  return (
    <div className="relative">
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input
        type="text"
        placeholder={placeholder}
        className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none ${
          !isValid ? 'border-red-300 bg-red-50' : 'border-gray-200'
        }`}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          onChange(e.target.value);
          setShowDropdown(true);
          setIsValid(true);
        }}
        onFocus={() => setShowDropdown(true)}
        onBlur={handleBlur}
      />
      {!isValid && (
        <p className="text-xs text-red-500 mt-1">목록에서 선택해주세요. 유사한 항목을 검색해보세요.</p>
      )}
      {showDropdown && filtered.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
          {filtered.map((item) => (
            <button
              key={item}
              className="w-full text-left px-4 py-2 hover:bg-blue-50 text-sm text-gray-700 cursor-pointer"
              onMouseDown={() => {
                setQuery(item);
                onChange(item);
                setShowDropdown(false);
                setIsValid(true);
              }}
            >
              {item}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default function GoalInputPage({ profile, setProfile }: Props) {
  const navigate = useNavigate();
  const [goal, setGoal] = useState<StudentGoal>({
    hasGoal: true,
    targetHighSchool: '',
    targetUniversity: '',
    targetMajor: '',
    targetJob: '',
  });

  const handleNext = () => {
    const hasAnyInput =
      goal.targetHighSchool || goal.targetUniversity || goal.targetMajor || goal.targetJob;
    setProfile({
      ...profile,
      goal: { ...goal, hasGoal: !!hasAnyInput },
    });
    navigate('/assessment/holland');
  };

  const handleSkip = () => {
    setProfile({
      ...profile,
      goal: { hasGoal: false },
    });
    navigate('/assessment/holland');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8">
        {/* 진행 상태 */}
        <div className="flex items-center gap-2 mb-6">
          <div className="flex-1 h-2 bg-blue-600 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
          <div className="flex-1 h-2 bg-gray-200 rounded-full" />
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2">🎯 나의 목표</h2>
        <p className="text-gray-600 mb-6">
          희망하는 진로나 목표가 있다면 입력해주세요.
          <br />
          <span className="text-sm text-gray-400">AI 추천 결과와 비교 분석해드립니다.</span>
        </p>

        <div className="space-y-4">
          <AutocompleteInput
            label="희망 고등학교"
            placeholder="학교명을 입력하세요 (예: 서울과학)"
            value={goal.targetHighSchool || ''}
            onChange={(v) => setGoal({ ...goal, targetHighSchool: v })}
            suggestions={HIGH_SCHOOLS}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              희망 대학교
            </label>
            <input
              type="text"
              placeholder="예: 서울대학교, KAIST"
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              value={goal.targetUniversity}
              onChange={(e) => setGoal({ ...goal, targetUniversity: e.target.value })}
            />
          </div>

          <AutocompleteInput
            label="희망 학과/전공"
            placeholder="학과명을 입력하세요 (예: 컴퓨터)"
            value={goal.targetMajor || ''}
            onChange={(v) => setGoal({ ...goal, targetMajor: v })}
            suggestions={MAJORS}
            strict={true}
          />

          <AutocompleteInput
            label="희망 직업"
            placeholder="직업명을 입력하세요 (예: 소프트웨어)"
            value={goal.targetJob || ''}
            onChange={(v) => setGoal({ ...goal, targetJob: v })}
            suggestions={JOBS}
            strict={true}
          />
        </div>

        <div className="flex gap-3 mt-8">
          <button
            onClick={handleSkip}
            className="flex-1 py-3 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition cursor-pointer"
          >
            건너뛰기
          </button>
          <button
            onClick={handleNext}
            className="flex-1 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition cursor-pointer"
          >
            다음 →
          </button>
        </div>
      </div>
    </div>
  );
}
