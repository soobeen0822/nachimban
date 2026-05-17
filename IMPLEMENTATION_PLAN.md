# 🧭 나침반 (NACHIMBAN) - 구현 계획서

---

## 📐 전체 구현 구조

```
[사용자 브라우저]
       ↕ (REST API)
[Frontend - React]
       ↕ (API 호출)
[Backend - FastAPI]
       ↕
[데이터 레이어]
  ├── SQLite (가공된 공공데이터)
  ├── AI 매칭 엔진 (Python)
  └── 공공데이터 API 연동
```

---

## 🗓️ 구현 단계별 계획

### Phase 1: 데이터 수집 & 가공 (3~4일)

#### 1-1. 공공데이터 API 키 발급
| 데이터 | 플랫폼 | API 키 발급처 |
|--------|--------|--------------|
| 학교 기본정보 | 공공데이터포털 | data.go.kr |
| 개설 교과목 현황 | 학교알리미 | schoolinfo.go.kr |
| 졸업 후 진학 현황 | 학교알리미 | schoolinfo.go.kr |
| 직업 정보 (Holland 코드 포함) | 워크넷 | openapi.work.go.kr |
| 학과 정보 | 커리어넷 | career.go.kr/openapi |
| 대학 학과 정보 | 대학알리미 | academyinfo.go.kr |

#### 1-2. 데이터 수집 스크립트 작성
```
analysis/
├── 01_collect_school_info.py      # 학교 기본정보 수집
├── 02_collect_curriculum.py       # 개설 교과목 수집
├── 03_collect_career_path.py      # 졸업 후 진학현황 수집
├── 04_collect_jobs.py             # 워크넷 직업정보 수집
├── 05_collect_majors.py           # 커리어넷 학과정보 수집
└── 06_collect_university.py       # 대학 학과정보 수집
```

#### 1-3. 데이터 가공 & 테이블 설계

**핵심 테이블:**

```sql
-- 고등학교 정보
schools (
  id, name, type, region, address, homepage_url,
  admission_url, phone, lat, lng
)

-- 학교별 개설 교과목
school_subjects (
  school_id, subject_name, category, year
)

-- 학교별 졸업생 진학 현황
school_career_stats (
  school_id, year, university_type, major_category, count, ratio
)

-- 직업 정보 (Holland 코드 포함)
jobs (
  id, name, description, holland_code_1, holland_code_2, holland_code_3,
  required_skills, salary_range, growth_outlook
)

-- 대학 학과 정보
majors (
  id, name, university, category, related_jobs,
  required_subjects, employment_rate
)

-- 직업-학과 매핑
job_major_mapping (
  job_id, major_id, relevance_score
)

-- 진로-교과목 매핑 (AI 매칭에 사용)
career_subject_mapping (
  career_category, required_subjects, recommended_subjects
)
```

---

### Phase 2: AI 매칭 엔진 개발 (4~5일)

#### 2-1. MBTI 스펙트럼 처리 모듈

```python
# 입력: 각 축 0~100 연속값
mbti_profile = {
    "EI": 35,   # 0=극강E, 100=극강I → 35면 약한E
    "SN": 20,   # 0=극강S, 100=극강N → 20이면 강한S
    "TF": 70,   # 0=극강T, 100=극강F → 70이면 약한F
    "JP": 60    # 0=극강J, 100=극강P → 60이면 약한P
}

# 4단계 라벨링
def get_spectrum_label(axis, value):
    if value <= 25: return f"강한 {axis[0]}"
    elif value <= 50: return f"약한 {axis[0]}"
    elif value <= 75: return f"약한 {axis[1]}"
    else: return f"강한 {axis[1]}"
```

#### 2-2. Holland 검사 처리 모듈

```python
# 입력: 6개 유형별 점수 (0~100)
holland_profile = {
    "R": 45, "I": 85, "A": 30,
    "S": 55, "E": 40, "C": 60
}

# 상위 3개 코드 추출
top3_codes = sorted(holland_profile, key=holland_profile.get, reverse=True)[:3]
# → ["I", "C", "S"]
```

#### 2-3. 진로 매칭 알고리즘

```python
def calculate_career_match(holland_profile, mbti_profile, job):
    # 1. Holland 코드 유사도 (코사인 유사도)
    holland_score = cosine_similarity(
        student_holland_vector,
        job_holland_vector
    )

    # 2. MBTI 스펙트럼 매칭
    # 직업별 평균 MBTI 프로필과 비교
    mbti_score = 1 - euclidean_distance(
        student_mbti_vector,
        job_avg_mbti_vector
    ) / max_distance

    # 3. 가중 합산
    final_score = holland_score * 0.5 + mbti_score * 0.3 + bonus * 0.2

    return final_score  # 0~100
```

#### 2-4. 고등학교 매칭 알고리즘

```python
def match_high_school(career_target, region, student_profile):
    # 1. 목표 진로 → 필요 교과목 추출
    required_subjects = get_required_subjects(career_target)

    # 2. 해당 교과목 개설 학교 필터
    candidate_schools = filter_schools_by_subjects(required_subjects, region)

    # 3. 적합도 점수 계산
    for school in candidate_schools:
        score = (
            subject_coverage_score(school, required_subjects) * 0.4 +
            career_success_rate(school, career_target) * 0.4 +
            accessibility_score(school, student_location) * 0.2
        )

    # 4. 학교 유형 다양성 보장 (특목/일반/특성화 섞기)
    return diversified_top_n(candidate_schools, n=5)
```

#### 2-5. 교육과정 로드맵 생성

```python
def generate_roadmap(career_target, current_grade, school):
    # 학교 개설 과목 중 진로 연계 과목 선별
    # 학년별 이수 순서 최적화
    roadmap = {
        "고1": {"교과": [...], "비교과": [...], "목표": "기초 다지기"},
        "고2": {"교과": [...], "비교과": [...], "목표": "심화 준비"},
        "고3": {"교과": [...], "비교과": [...], "목표": "전공 연계"},
    }
    return roadmap
```

---

### Phase 3: Backend 개발 (3~4일)

#### 3-1. FastAPI 서버 구조

```
backend/
├── main.py                  # FastAPI 앱 엔트리포인트
├── config.py                # 설정 (DB 경로, API 키 등)
├── database.py              # SQLite 연결
├── models/                  # Pydantic 모델 (요청/응답 스키마)
│   ├── student.py
│   ├── school.py
│   ├── career.py
│   └── roadmap.py
├── routers/                 # API 라우터
│   ├── assessment.py        # 검사 결과 제출
│   ├── career.py            # 진로 추천 API
│   ├── school.py            # 학교 매칭 API
│   ├── roadmap.py           # 로드맵 생성 API
│   └── data.py              # 데이터 조회 API
├── services/                # 비즈니스 로직
│   ├── matching_engine.py   # AI 매칭 엔진
│   ├── holland.py           # Holland 검사 처리
│   ├── mbti.py              # MBTI 스펙트럼 처리
│   └── roadmap_generator.py # 로드맵 생성
└── data/
    └── nachimban.db         # SQLite DB 파일
```

#### 3-2. 핵심 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/assessment/submit` | Holland + MBTI 검사 결과 제출 |
| POST | `/api/career/recommend` | 진로 추천 (+ 목표 매칭도) |
| POST | `/api/school/match` | 고등학교 매칭 |
| POST | `/api/roadmap/generate` | 교육과정 로드맵 생성 |
| GET | `/api/jobs/{id}` | 직업 상세 정보 |
| GET | `/api/schools/{id}` | 학교 상세 정보 |
| GET | `/api/majors/{id}` | 학과 상세 정보 |

#### 3-3. 요청/응답 예시

**진로 추천 요청:**
```json
{
  "holland_scores": {"R": 45, "I": 85, "A": 30, "S": 55, "E": 40, "C": 60},
  "mbti_spectrum": {"EI": 35, "SN": 20, "TF": 70, "JP": 60},
  "region": "서울 강남구",
  "grade": "중3",
  "goal": {
    "has_goal": true,
    "target_university": "서울대학교",
    "target_major": "컴퓨터공학과",
    "target_job": "소프트웨어 개발자"
  }
}
```

**진로 추천 응답:**
```json
{
  "profile_summary": {
    "holland_top3": ["I", "C", "S"],
    "mbti_label": "약한E / 강한S / 약한F / 약한P",
    "personality_keywords": ["분석적", "실용적", "체계적"]
  },
  "recommendations": [
    {
      "rank": 1,
      "career": "소프트웨어공학",
      "match_score": 95,
      "reason": "탐구형(I) + 강한S + 약한F 조합이 ...",
      "related_jobs": ["백엔드 개발자", "시스템 엔지니어"],
      "related_majors": ["컴퓨터공학", "소프트웨어학"]
    }
  ],
  "goal_comparison": {
    "match_score": 92,
    "verdict": "매우 높음",
    "message": "목표와 적성이 매우 잘 맞습니다!",
    "strengths": ["논리적 사고력이 컴퓨터공학에 적합"],
    "improvements": ["팀 프로젝트 경험 보완 권장"]
  }
}
```

---

### Phase 4: Frontend 개발 (5~7일)

#### 4-1. 프로젝트 구조

```
frontend/
├── src/
│   ├── app/                    # 라우팅 & 레이아웃
│   ├── components/
│   │   ├── common/             # 공통 UI (버튼, 카드 등)
│   │   ├── assessment/         # 검사 관련
│   │   │   ├── GoalInput.tsx        # 목표 입력 (Step 1)
│   │   │   ├── HollandTest.tsx      # Holland 검사 (Step 2)
│   │   │   ├── MbtiSpectrum.tsx     # MBTI 스펙트럼 검사 (Step 3)
│   │   │   └── AdditionalInfo.tsx   # 추가 정보 (Step 4)
│   │   ├── dashboard/          # 결과 대시보드
│   │   │   ├── ProfileChart.tsx     # 프로필 시각화
│   │   │   ├── CareerRecommend.tsx  # 진로 추천 결과
│   │   │   ├── GoalComparison.tsx   # 목표 매칭 비교
│   │   │   ├── SchoolMatch.tsx      # 고등학교 매칭
│   │   │   └── Roadmap.tsx          # 교육과정 로드맵
│   │   └── charts/             # 차트 컴포넌트
│   │       ├── HollandHexagon.tsx   # Holland 6각형
│   │       ├── MbtiSlider.tsx       # MBTI 스펙트럼 바
│   │       └── MatchBubble.tsx      # 적합도 버블차트
│   ├── hooks/                  # 커스텀 훅
│   ├── services/               # API 호출
│   │   └── api.ts
│   ├── types/                  # TypeScript 타입
│   └── utils/                  # 유틸 함수
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

#### 4-2. 페이지 구성

| 페이지 | 경로 | 설명 |
|--------|------|------|
| 랜딩 | `/` | 서비스 소개, 시작하기 버튼 |
| 목표 입력 | `/assessment/goal` | 희망 진로 입력 or 건너뛰기 |
| Holland 검사 | `/assessment/holland` | 간소화된 Holland 검사 |
| MBTI 검사 | `/assessment/mbti` | 스펙트럼 방식 MBTI 검사 |
| 추가 정보 | `/assessment/info` | 지역, 학년 등 |
| 결과 대시보드 | `/result` | 통합 결과 (시나리오 1/2/3) |
| 학교 상세 | `/school/:id` | 개별 학교 상세 정보 |

#### 4-3. 핵심 UI 구현 포인트

**MBTI 스펙트럼 입력 UI:**
- 각 축별 슬라이더 (0~100)
- 실시간으로 "강한E / 약한E / 약한I / 강한I" 라벨 변경
- 설문 문항 답변에 따라 자동 계산

**결과 대시보드:**
- 스크롤 기반 원페이지 (섹션별 구분)
- 각 섹션 진입 시 애니메이션
- 학교 매칭: 기본 5개 카드 + "더보기" → 10개 확장

---

### Phase 5: 통합 & 배포 (2~3일)

#### 5-1. 연동 테스트
- Frontend ↔ Backend API 연동 확인
- 각 시나리오별 end-to-end 테스트
- 엣지 케이스: 건너뛰기 흐름, 데이터 없는 지역 등

#### 5-2. 배포

| 구분 | 서비스 | 무료 티어 |
|------|--------|----------|
| Frontend | Vercel | ✅ 무료 |
| Backend | Railway 또는 Render | ✅ 무료 (제한적) |
| DB | SQLite (Backend에 포함) | ✅ |
| 도메인 | Vercel 기본 도메인 | ✅ nachimban.vercel.app |

#### 5-3. 시연용 데모 데이터
- 실제 API 호출 제한 대비, 주요 시나리오용 캐싱 데이터 준비
- 서울/부산/대전 등 3개 지역 기준 데모 시나리오 구성

---

### Phase 6: 시각화 & 보고서 (2~3일)

#### 6-1. 데이터 인사이트 시각화 (제출용)
- 공공데이터 EDA 결과 차트 5~7개
- 예: 지역별 특목고 분포, 학과별 취업률, Holland 유형별 인기 직업 등

#### 6-2. 최종 보고서 구성
1. 문제 정의 & 배경
2. 활용 공공데이터 목록 & 수집 방법
3. AI 모델 설계 (Holland + MBTI 스펙트럼 조합)
4. 서비스 시연 스크린샷
5. 기대효과 & 사회적 가치
6. 향후 발전 방향

---

## ⏱️ 전체 일정 요약

| Phase | 작업 | 소요일 | 산출물 |
|-------|------|--------|--------|
| 1 | 데이터 수집 & 가공 | 3~4일 | SQLite DB, 수집 스크립트 |
| 2 | AI 매칭 엔진 | 4~5일 | matching_engine.py |
| 3 | Backend (FastAPI) | 3~4일 | API 서버 |
| 4 | Frontend (React) | 5~7일 | 웹 프로토타입 |
| 5 | 통합 & 배포 | 2~3일 | 라이브 URL |
| 6 | 시각화 & 보고서 | 2~3일 | 보고서 PDF |
| **합계** | | **19~26일** | |

---

## 🛠️ 개발 환경 세팅

### 필요 도구
```bash
# Python (Backend + 데이터 분석)
python 3.11+
pip install fastapi uvicorn pandas numpy scikit-learn requests

# Node.js (Frontend)
node 18+
npx create-react-app frontend --template typescript
npm install tailwindcss recharts axios react-router-dom
```

### 시작 순서
1. `data/` 폴더 생성 → 공공데이터 API 키 발급
2. 수집 스크립트 실행 → `data/raw/`에 저장
3. 가공 스크립트 → `data/nachimban.db` 생성
4. Backend 개발 → `localhost:8000`에서 API 테스트
5. Frontend 개발 → `localhost:3000`에서 UI 확인
6. 연동 → 배포

---

## ⚠️ 리스크 & 대응

| 리스크 | 대응 방안 |
|--------|----------|
| 공공데이터 API 응답 느림/장애 | 사전 수집 후 DB에 저장, 실시간 호출 최소화 |
| Holland-직업 매핑 데이터 부족 | 워크넷 직업사전에 Holland 코드 이미 포함, 부족 시 수동 매핑 |
| MBTI 스펙트럼 → 직업 매핑 근거 | 학술 논문 기반 + 커리어넷 적성검사 데이터로 보완 |
| 학교 홈페이지 URL 변경 | 학교알리미 데이터에 홈페이지 포함, 주기적 검증 |
| 프로토타입 완성도 | 핵심 플로우(검사→추천→학교매칭) 우선 구현, 나머지는 목업 |
