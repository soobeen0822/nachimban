const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface AnalyzeRequest {
  holland: { R: number; I: number; A: number; S: number; E: number; C: number };
  mbti: { EI: number; SN: number; TF: number; JP: number };
  goal: {
    hasGoal: boolean;
    targetHighSchool?: string;
    targetUniversity?: string;
    targetMajor?: string;
    targetJob?: string;
  };
  region: string;
  grade: string;
  gender: string;
}

export interface CareerResult {
  rank: number;
  jobNm: string;
  matchScore: number;
  reason: string;
  relatedMajors: string[];
  hollandScore: number;
  mbtiScore: number;
  jobLrclNm: string;
  sal: string;
  jobSum: string;
}

export interface GoalComparisonResult {
  matchScore: number;
  verdict: string;
  message: string;
  strengths: string[];
  improvements: string[];
}

export interface SchoolResult {
  name: string;
  type: string;
  matchScore: number;
  address: string;
  homepageUrl: string;
  region: string;
  reasons: string[];
}

export interface RoadmapResult {
  grade: string;
  goal: string;
  subjects: string[];
  activities: string[];
}

export interface AnalyzeResponse {
  careers: CareerResult[];
  goalComparison: GoalComparisonResult | null;
  schools: SchoolResult[];
  roadmap: RoadmapResult[];
}

export async function analyzeProfile(data: AnalyzeRequest): Promise<AnalyzeResponse> {
  const resp = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!resp.ok) {
    throw new Error(`API error: ${resp.status}`);
  }

  return resp.json();
}
