import {
  CareerRecommendation,
  GoalComparison,
  SchoolRecommendation,
  RoadmapItem,
} from '../types';

// 진로 추천 목업 데이터
export const mockCareerRecommendations: CareerRecommendation[] = [
  {
    rank: 1,
    career: '소프트웨어 개발',
    matchScore: 94,
    reason:
      '탐구형(I)과 관습형(C) 조합에 강한 사고(T) 성향이 논리적 문제 해결과 체계적 코딩 작업에 매우 적합합니다.',
    relatedJobs: ['백엔드 개발자', '시스템 엔지니어', 'AI 엔지니어'],
    relatedMajors: ['컴퓨터공학', '소프트웨어학', '인공지능학'],
  },
  {
    rank: 2,
    career: '데이터 사이언스',
    matchScore: 91,
    reason:
      '탐구형(I) 기반의 분석 성향과 감각(S) 우세가 데이터 기반 의사결정에 강점을 보입니다.',
    relatedJobs: ['데이터 분석가', '머신러닝 엔지니어', '비즈니스 분석가'],
    relatedMajors: ['데이터사이언스', '통계학', '산업공학'],
  },
  {
    rank: 3,
    career: '전자공학',
    matchScore: 86,
    reason:
      '현실형(R)과 탐구형(I)의 조합이 하드웨어 설계와 실험적 연구에 적합합니다.',
    relatedJobs: ['회로설계 엔지니어', '반도체 공정 엔지니어', '임베디드 개발자'],
    relatedMajors: ['전자공학', '전기공학', '반도체공학'],
  },
  {
    rank: 4,
    career: '건축설계',
    matchScore: 79,
    reason:
      '현실형(R)의 실용성과 약한 직관(N)이 창의적이면서도 구현 가능한 설계에 강점입니다.',
    relatedJobs: ['건축가', '인테리어 디자이너', '도시계획가'],
    relatedMajors: ['건축학', '건축공학', '도시공학'],
  },
  {
    rank: 5,
    career: '수학/통계 연구',
    matchScore: 75,
    reason:
      '탐구형(I)과 강한 사고(T), 판단(J) 성향이 추상적 문제를 체계적으로 접근하는 연구에 적합합니다.',
    relatedJobs: ['수학 연구원', '보험계리사', '퀀트 분석가'],
    relatedMajors: ['수학', '통계학', '금융수학'],
  },
];

// 목표 비교 목업 데이터
export const mockGoalComparison: GoalComparison = {
  matchScore: 92,
  verdict: '매우 높음',
  message: '목표와 적성이 매우 잘 맞습니다!',
  strengths: [
    '논리적 사고력(강한T)이 컴퓨터공학에 매우 적합',
    '탐구형(I) 성향이 깊이있는 기술 연구에 유리',
    '체계적(J) 성향이 복잡한 프로젝트 관리에 도움',
  ],
  improvements: [
    '약한 외향(E) → 팀 프로젝트/해커톤 경험 권장',
    '물리학Ⅱ, 미적분 이수 필요 (현재 미이수 시)',
  ],
};

// 학교 추천 목업 데이터
export const mockSchoolRecommendations: SchoolRecommendation[] = [
  {
    rank: 1,
    name: '서울과학고등학교',
    type: '과학고',
    matchScore: 96,
    reasons: [
      '이공계열 진학률 97%로 전국 최상위',
      '정보과학·AI 심화과정 별도 운영',
      '졸업생 중 컴퓨터공학 계열 진학 38%',
    ],
    homepageUrl: 'https://www.sshs.hs.kr',
    admissionInfo: '1단계: 서류평가 (학교생활기록부+자기소개서) → 2단계: 과학창의성 면접',
    admissionPeriod: '매년 10월~11월 (전기 모집)',
    admissionUrl: 'https://www.sshs.hs.kr/admission',
  },
  {
    rank: 2,
    name: '세종과학예술영재학교',
    type: '과학고',
    matchScore: 93,
    reasons: [
      '과학·수학 융합 교육과정으로 SW 기초 탄탄',
      '자율 연구 프로젝트 필수 → 탐구형(I)에 적합',
      'AI·빅데이터 특화 트랙 운영',
    ],
    homepageUrl: 'https://www.sjsa.hs.kr',
    admissionInfo: '1단계: 지원서 및 추천서 → 2단계: 창의적 문제해결력 캠프 → 3단계: 면접',
    admissionPeriod: '매년 5월~7월 (전기 모집)',
    admissionUrl: 'https://www.sjsa.hs.kr/admission',
  },
  {
    rank: 3,
    name: '단국대학교부속고등학교',
    type: '일반고',
    matchScore: 88,
    reasons: [
      '정보·물리학Ⅱ·미적분·기하 모두 개설',
      '이공계열 진학률 72%로 강남구 일반고 1위',
      'SW 동아리(3개)·과학탐구동아리 활발',
    ],
    homepageUrl: 'https://www.dankook-h.hs.kr',
    address: '서울특별시 강남구 도곡로 123',
    district: '강남서초 학군, 거주지에서 도보 12분',
    commuteInfo: '지하철 3호선 매봉역 도보 5분, 버스 3개 노선',
  },
  {
    rank: 4,
    name: '중앙대학교사범대학부속고등학교',
    type: '일반고',
    matchScore: 85,
    reasons: [
      '공학일반 과목 개설 (서울 일반고 중 소수)',
      '수학·과학 교과 심화반 운영',
      '대학 연계 연구 체험 프로그램 연 4회',
    ],
    homepageUrl: 'https://www.cauhs.hs.kr',
    address: '서울특별시 동작구 흑석로 84',
    district: '동작관악 학군',
    commuteInfo: '지하철 9호선 흑석역 도보 7분',
  },
  {
    rank: 5,
    name: '미림마이스터고등학교',
    type: '마이스터고',
    matchScore: 82,
    reasons: [
      'SW 개발 분야 취업률 94% (전국 마이스터고 1위)',
      '네이버·카카오·삼성전자 등 협약기업 35개',
      '재직자 전형으로 대학 진학 경로 확보 가능',
    ],
    homepageUrl: 'https://www.e-mirim.hs.kr',
    admissionInfo: '1단계: 출석성적+봉사 → 2단계: 직업적성 면접 (SW 관심도)',
    admissionPeriod: '매년 10월 (전기 모집, 전국 단위)',
    admissionUrl: 'https://www.e-mirim.hs.kr/admission',
  },
];

// 교육과정 로드맵 목업 데이터
export const mockRoadmap: RoadmapItem[] = [
  {
    grade: '고1',
    goal: '기초 다지기',
    subjects: ['통합과학', '수학Ⅰ', '수학Ⅱ', '정보', '영어Ⅰ'],
    activities: [
      'SW 동아리 가입',
      '코딩 기초 대회 참가',
      '수학 자율 스터디 구성',
    ],
  },
  {
    grade: '고2',
    goal: '심화 준비',
    subjects: ['물리학Ⅰ', '미적분', '확률과 통계', '프로그래밍', '영어Ⅱ'],
    activities: [
      '정보올림피아드 도전',
      'AI 관련 독서 (인공지능 시대의 비즈니스)',
      '교내 과학탐구 발표대회',
    ],
  },
  {
    grade: '고3',
    goal: '전공 연계',
    subjects: ['물리학Ⅱ', '기하', '인공지능 수학', '공학일반'],
    activities: [
      '자율 연구 보고서 작성 (AI 프로젝트)',
      '대학 연계 SW 캠프 참가',
      '포트폴리오 정리',
    ],
  },
];
