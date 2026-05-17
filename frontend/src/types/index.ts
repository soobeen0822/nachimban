// Holland 검사 유형
export type HollandCode = 'R' | 'I' | 'A' | 'S' | 'E' | 'C';

export interface HollandProfile {
  R: number; // 현실형 0~100
  I: number; // 탐구형
  A: number; // 예술형
  S: number; // 사회형
  E: number; // 진취형
  C: number; // 관습형
}

// MBTI 스펙트럼 (각 축 0~100)
export interface MbtiSpectrum {
  EI: number; // 0=극강E, 100=극강I
  SN: number; // 0=극강S, 100=극강N
  TF: number; // 0=극강T, 100=극강F
  JP: number; // 0=극강J, 100=극강P
}

// 목표 정보
export interface StudentGoal {
  hasGoal: boolean;
  targetHighSchool?: string;
  targetUniversity?: string;
  targetMajor?: string;
  targetJob?: string;
}

// 학생 전체 프로필
export interface StudentProfile {
  goal: StudentGoal;
  holland: HollandProfile;
  mbti: MbtiSpectrum;
  region: string;
  grade: string;
}

// 추천 결과
export interface CareerRecommendation {
  rank: number;
  career: string;
  matchScore: number;
  reason: string;
  relatedJobs: string[];
  relatedMajors: string[];
}

// 목표 비교 결과
export interface GoalComparison {
  matchScore: number;
  verdict: '매우 높음' | '높음' | '보통' | '낮음';
  message: string;
  strengths: string[];
  improvements: string[];
}

// 학교 추천
export type SchoolType = '일반고' | '자율형사립고' | '과학고' | '외국어고' | '국제고' | '특성화고' | '마이스터고';

export interface SchoolRecommendation {
  rank: number;
  name: string;
  type: SchoolType;
  matchScore: number;
  reasons: string[];
  // 공통
  homepageUrl: string;
  // 일반고 전용
  address?: string;
  district?: string;
  commuteInfo?: string;
  // 비일반고 전용
  admissionInfo?: string;
  admissionPeriod?: string;
  admissionUrl?: string;
}

// 교육과정 로드맵
export interface RoadmapItem {
  grade: string;
  goal: string;
  subjects: string[];
  activities: string[];
}
