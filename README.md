# 🧭 나침반 (NACHIMBAN)

**Navigating Academic Careers through Holistic Intelligence with Mined puBlic data And Networks**

> 교육 공공데이터와 AI를 활용한 고등학교 진로 매칭 서비스

🔗 **서비스 URL**: [https://nachimban-nine.vercel.app](https://nachimban-nine.vercel.app)

---

## 📋 프로젝트 개요

나침반은 **Holland 흥미 검사**와 **MBTI 연속 스펙트럼**(256가지+ 세분화)을 결합하고, **교육 공공데이터**를 AI로 분석하여 학생 맞춤형 진로와 고등학교를 추천하는 서비스입니다.

### 핵심 차별점
- **MBTI 연속 스펙트럼**: 기존 16유형이 아닌 4축 0~100 연속값으로 정밀 매칭
- **공공데이터 기반**: 나이스 2,407개 학교 + 워크넷 462개 직업 실제 데이터 활용
- **AI 매칭 엔진**: Holland 코사인 유사도 + MBTI 유클리드 거리 기반 추천 알고리즘

---

## 🎯 주요 기능

| 기능 | 설명 |
|------|------|
| 진로 추천 | Holland + MBTI 스펙트럼 기반 적합 직업 Top 5 추천 |
| 목표 매칭 비교 | 학생이 입력한 목표와 AI 추천 간 적합도 비교 |
| 고등학교 매칭 | 진로 필수 과목 개설 여부 + 거주지 기반 학교 추천 |
| 교육과정 로드맵 | 고1~고3 학년별 추천 교과목 및 비교과 활동 |

---

## 📊 활용 공공데이터

| 데이터 | 출처 | 건수 |
|--------|------|------|
| 전국 고등학교 기본정보 | 나이스(NEIS) 교육정보 개방 포털 | 2,407개 학교 |
| 고등학교별 개설 교과목 | 나이스(NEIS) 시간표 API | 2,307개 학교, 18,044개 과목 |
| 직업 상세정보 | 워크넷(work24) 직업정보 API | 462개 직업 |
| 직업별 능력/지식 데이터 | 워크넷(work24) 직업정보 API | 462개 직업 |

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | React, TypeScript, Tailwind CSS, Vite, Recharts |
| Backend | Python, FastAPI |
| AI/매칭 | NumPy, Pandas, 코사인 유사도, 유클리드 거리 |
| 배포 | Vercel (Frontend), Render (Backend) |

---

## 🔬 AI 매칭 알고리즘

```
학생 입력: Holland 6축 점수 + MBTI 4축 연속값 (0~100)
                    ↓
[Step 1] Holland 코사인 유사도로 직업군 1차 매칭 (가중치 60%)
[Step 2] MBTI 유클리드 거리로 세부 매칭 (가중치 40%)
[Step 3] 직업 → 관련 학과 → 필요 교과목 추출
[Step 4] 교과목 개설 학교 필터 + 거주지 근접도 반영
                    ↓
결과: 추천 진로 Top5 + 맞춤 학교 + 교육과정 로드맵
```

---

## 📁 프로젝트 구조

```
nachimban/
├── frontend/               # React 웹 프로토타입
│   └── src/
│       ├── pages/          # 6개 페이지 (랜딩~결과)
│       ├── components/     # 대시보드 섹션 컴포넌트
│       ├── services/       # API 호출
│       └── data/           # 학교/학과/직업 목록 JSON
├── backend/                # FastAPI 서버
│   ├── main.py             # API 엔드포인트
│   └── matching_engine.py  # AI 매칭 엔진
├── scripts/                # 데이터 수집 & 가공 스크립트
│   ├── 01_collect_neis_schools.py
│   ├── 02_collect_work24_jobs.py
│   ├── 03_collect_neis_subjects.py
│   ├── 04_build_holland_mapping.py
│   ├── 05_build_career_mapping.py
│   ├── 06_build_mbti_job_profile.py
│   └── 07_eda_visualization.py
├── data/raw/               # 수집된 공공데이터
└── docs/charts/            # EDA 시각화 차트
```

---

## 🚀 로컬 실행 방법

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

---

## 📈 기대효과

- **교육 형평성**: 지역/소득에 관계없이 동일한 품질의 AI 진로 추천
- **정보 접근성**: 흩어진 교육 공공데이터를 하나의 서비스로 통합
- **미스매칭 감소**: 학생-학교-진로 간 불일치 사전 예방
- **공공데이터 활용**: 세금으로 구축된 공공데이터의 실질적 활용 모범 사례

---

## 👤 제작자

**A project by Soobeen Oh**

교육공공데이터 AI 활용 대회 출품작
