"""
나침반 (NACHIMBAN) - FastAPI Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from matching_engine import MatchingEngine

app = FastAPI(title="나침반 API", version="1.0.0")

# CORS 설정 (프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 매칭 엔진 초기화
engine = MatchingEngine()


# ============================
# Request/Response 모델
# ============================

class HollandScores(BaseModel):
    R: int = 50
    I: int = 50
    A: int = 50
    S: int = 50
    E: int = 50
    C: int = 50


class MbtiSpectrum(BaseModel):
    EI: int = 50
    SN: int = 50
    TF: int = 50
    JP: int = 50


class StudentGoal(BaseModel):
    hasGoal: bool = False
    targetHighSchool: str | None = None
    targetUniversity: str | None = None
    targetMajor: str | None = None
    targetJob: str | None = None


class AssessmentRequest(BaseModel):
    holland: HollandScores
    mbti: MbtiSpectrum
    goal: StudentGoal
    region: str = ""
    grade: str = "중3"
    gender: str = ""


class CareerRecommendResponse(BaseModel):
    rank: int
    jobNm: str
    matchScore: float
    reason: str
    relatedMajors: list[str]
    hollandScore: float
    mbtiScore: float
    jobLrclNm: str = ""
    sal: str = ""
    jobSum: str = ""


class GoalComparisonResponse(BaseModel):
    matchScore: int
    verdict: str
    message: str
    strengths: list[str]
    improvements: list[str]


class SchoolResponse(BaseModel):
    name: str
    type: str
    matchScore: float
    address: str
    homepageUrl: str
    region: str
    reasons: list[str]


class RoadmapItem(BaseModel):
    grade: str
    goal: str
    subjects: list[str]
    activities: list[str]


class FullResultResponse(BaseModel):
    careers: list[CareerRecommendResponse]
    goalComparison: GoalComparisonResponse | None
    schools: list[SchoolResponse]
    roadmap: list[RoadmapItem]


# ============================
# API 엔드포인트
# ============================

@app.get("/")
def root():
    return {"service": "나침반 (NACHIMBAN)", "version": "1.0.0", "status": "running"}


@app.post("/api/analyze", response_model=FullResultResponse)
def analyze(req: AssessmentRequest):
    """전체 분석: 진로추천 + 목표비교 + 학교매칭 + 로드맵"""

    holland_dict = req.holland.model_dump()
    mbti_dict = req.mbti.model_dump()

    # 1. 진로 추천
    careers = engine.recommend_careers(holland_dict, mbti_dict, top_n=5)

    # 2. 목표 비교
    goal_comparison = None
    if req.goal.hasGoal:
        goal_comparison = engine.compare_with_goal(
            holland_dict, mbti_dict,
            goal_job=req.goal.targetJob,
            goal_major=req.goal.targetMajor,
        )

    # 3. 학교 매칭
    schools = engine.match_schools(careers, region=req.region, gender=req.gender, top_n=10)

    # 4. 로드맵
    roadmap = engine.generate_roadmap(careers, grade=req.grade)

    return FullResultResponse(
        careers=[CareerRecommendResponse(
            rank=c["rank"],
            jobNm=c["jobNm"],
            matchScore=c["matchScore"],
            reason=c["reason"],
            relatedMajors=c["relatedMajors"],
            hollandScore=c["hollandScore"],
            mbtiScore=c["mbtiScore"],
            jobLrclNm=c.get("jobLrclNm", ""),
            sal=c.get("sal", ""),
            jobSum=c.get("jobSum", ""),
        ) for c in careers],
        goalComparison=GoalComparisonResponse(**goal_comparison) if goal_comparison else None,
        schools=[SchoolResponse(
            name=s["name"],
            type=s["type"],
            matchScore=s["matchScore"],
            address=s.get("address", ""),
            homepageUrl=s.get("homepageUrl", ""),
            region=s.get("region", ""),
            reasons=s.get("reasons", []),
        ) for s in schools],
        roadmap=[RoadmapItem(**r) for r in roadmap],
    )


@app.post("/api/career/recommend")
def recommend_careers(req: AssessmentRequest):
    """진로 추천만"""
    holland_dict = req.holland.model_dump()
    mbti_dict = req.mbti.model_dump()
    careers = engine.recommend_careers(holland_dict, mbti_dict, top_n=5)
    return {"careers": careers}


@app.post("/api/school/match")
def match_schools(req: AssessmentRequest):
    """학교 매칭만"""
    holland_dict = req.holland.model_dump()
    mbti_dict = req.mbti.model_dump()
    careers = engine.recommend_careers(holland_dict, mbti_dict, top_n=3)
    schools = engine.match_schools(careers, region=req.region, gender=req.gender, top_n=10)
    return {"schools": schools}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
