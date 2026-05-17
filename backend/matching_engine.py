"""
나침반 AI 매칭 엔진
- Holland + MBTI 스펙트럼 기반 진로 추천
- 직업 → 학과 → 교과목 → 학교 연결
- 목표 매칭도 비교
"""

import math
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


class MatchingEngine:
    def __init__(self):
        self.jobs_df = pd.read_csv(DATA_DIR / "work24_jobs.csv")
        self.holland_df = pd.read_csv(DATA_DIR / "holland_job_mapping.csv")
        self.mbti_df = pd.read_csv(DATA_DIR / "mbti_job_profile.csv")
        self.job_major_df = pd.read_csv(DATA_DIR / "job_major_mapping.csv")
        self.major_subject_df = pd.read_csv(DATA_DIR / "major_subject_mapping.csv")
        self.schools_df = pd.read_csv(DATA_DIR / "neis_high_schools.csv")
        self.school_subjects_df = pd.read_csv(DATA_DIR / "neis_school_subjects.csv")

        # 직업 통합 테이블 (Holland + MBTI 합침)
        self.job_profiles = self.holland_df[
            ["jobCd", "jobNm", "jobLrclNm", "holland_R", "holland_I", "holland_A",
             "holland_S", "holland_E", "holland_C", "holland_top3"]
        ].merge(
            self.mbti_df[["jobCd", "mbti_EI", "mbti_SN", "mbti_TF", "mbti_JP"]],
            on="jobCd", how="left"
        ).merge(
            self.jobs_df[["jobCd", "jobSum", "sal", "jobProspect"]],
            on="jobCd", how="left"
        )

    # ===========================
    # 1. 진로 추천 (시나리오 1)
    # ===========================

    def recommend_careers(
        self,
        holland_scores: dict,
        mbti_spectrum: dict,
        top_n: int = 5
    ) -> list[dict]:
        """
        Holland + MBTI 스펙트럼 기반 진로 추천

        Args:
            holland_scores: {"R": 0~100, "I": 0~100, ...}
            mbti_spectrum: {"EI": 0~100, "SN": 0~100, "TF": 0~100, "JP": 0~100}
            top_n: 추천 개수

        Returns:
            추천 직업 리스트 (적합도 점수 포함)
        """
        results = []

        for _, job in self.job_profiles.iterrows():
            # Holland 유사도 (코사인 유사도, 가중치 50%)
            holland_sim = self._holland_similarity(holland_scores, job)

            # MBTI 유사도 (유클리드 거리 기반, 가중치 30%)
            mbti_sim = self._mbti_similarity(mbti_spectrum, job)

            # 최종 점수 (0~100)
            final_score = round(holland_sim * 0.6 + mbti_sim * 0.4, 1)

            results.append({
                "jobCd": job["jobCd"],
                "jobNm": job["jobNm"],
                "jobLrclNm": job.get("jobLrclNm", ""),
                "matchScore": final_score,
                "hollandScore": round(holland_sim, 1),
                "mbtiScore": round(mbti_sim, 1),
                "holland_top3": job.get("holland_top3", ""),
                "jobSum": job.get("jobSum", ""),
                "sal": job.get("sal", ""),
            })

        # 점수 내림차순 정렬
        results.sort(key=lambda x: x["matchScore"], reverse=True)

        # Top N 추천 + 이유 생성
        top_results = results[:top_n]
        for i, r in enumerate(top_results):
            r["rank"] = i + 1
            r["reason"] = self._generate_reason(r, holland_scores, mbti_spectrum)
            r["relatedMajors"] = self._get_related_majors(r["jobCd"])

        return top_results

    def _holland_similarity(self, student_scores: dict, job_row) -> float:
        """Holland 코사인 유사도 (0~100)"""
        student_vec = np.array([
            student_scores.get("R", 0),
            student_scores.get("I", 0),
            student_scores.get("A", 0),
            student_scores.get("S", 0),
            student_scores.get("E", 0),
            student_scores.get("C", 0),
        ], dtype=float)

        job_vec = np.array([
            job_row.get("holland_R", 0),
            job_row.get("holland_I", 0),
            job_row.get("holland_A", 0),
            job_row.get("holland_S", 0),
            job_row.get("holland_E", 0),
            job_row.get("holland_C", 0),
        ], dtype=float)

        # 코사인 유사도
        dot = np.dot(student_vec, job_vec)
        norm_s = np.linalg.norm(student_vec)
        norm_j = np.linalg.norm(job_vec)

        if norm_s == 0 or norm_j == 0:
            return 0

        cosine_sim = dot / (norm_s * norm_j)
        return cosine_sim * 100  # 0~100

    def _mbti_similarity(self, student_mbti: dict, job_row) -> float:
        """MBTI 유클리드 거리 기반 유사도 (0~100)"""
        student_vec = np.array([
            student_mbti.get("EI", 50),
            student_mbti.get("SN", 50),
            student_mbti.get("TF", 50),
            student_mbti.get("JP", 50),
        ], dtype=float)

        job_vec = np.array([
            job_row.get("mbti_EI", 50),
            job_row.get("mbti_SN", 50),
            job_row.get("mbti_TF", 50),
            job_row.get("mbti_JP", 50),
        ], dtype=float)

        # 유클리드 거리 (최대 거리 = sqrt(4 * 100^2) = 200)
        distance = np.linalg.norm(student_vec - job_vec)
        max_distance = 200.0
        similarity = (1 - distance / max_distance) * 100

        return max(0, similarity)

    def _generate_reason(self, result: dict, holland: dict, mbti: dict) -> str:
        """추천 이유 생성"""
        # Holland 상위 유형
        sorted_holland = sorted(holland.items(), key=lambda x: x[1], reverse=True)
        top2 = [h[0] for h in sorted_holland[:2]]

        holland_names = {
            "R": "현실형", "I": "탐구형", "A": "예술형",
            "S": "사회형", "E": "진취형", "C": "관습형"
        }

        # MBTI 특성
        mbti_traits = []
        if mbti.get("EI", 50) <= 35:
            mbti_traits.append("외향적 성향")
        elif mbti.get("EI", 50) >= 65:
            mbti_traits.append("내향적 성향")
        if mbti.get("TF", 50) <= 35:
            mbti_traits.append("논리적 사고")
        elif mbti.get("TF", 50) >= 65:
            mbti_traits.append("공감 능력")

        reason_parts = []
        reason_parts.append(
            f"{holland_names.get(top2[0], '')}({top2[0]})과 "
            f"{holland_names.get(top2[1], '')}({top2[1]}) 유형의 조합이 적합"
        )
        if mbti_traits:
            reason_parts.append(f"{', '.join(mbti_traits)}이 이 직업에 유리")

        return ". ".join(reason_parts) + "합니다."

    def _get_related_majors(self, job_cd: str) -> list[str]:
        """직업에 연결된 학과 목록"""
        majors = self.job_major_df[self.job_major_df["jobCd"] == job_cd]["major"].tolist()
        return list(set(majors))[:5]

    # ===========================
    # 2. 목표 매칭도 비교
    # ===========================

    # 줄임말/약어 → 정식명 매핑
    ABBREVIATIONS = {
        # 대학교
        "서울대": "서울대학교", "연대": "연세대학교", "연세대": "연세대학교",
        "고대": "고려대학교", "고려대": "고려대학교",
        "카이스트": "KAIST", "포텍": "포항공과대학교", "포스텍": "포항공과대학교",
        "성대": "성균관대학교", "성균관대": "성균관대학교",
        "한양대": "한양대학교", "중앙대": "중앙대학교", "경희대": "경희대학교",
        "이대": "이화여자대학교", "이화여대": "이화여자대학교",
        "숙대": "숙명여자대학교", "숙명여대": "숙명여자대학교",
        "서강대": "서강대학교", "건대": "건국대학교", "건국대": "건국대학교",
        "동대": "동국대학교", "동국대": "동국대학교",
        "홍대": "홍익대학교", "홍익대": "홍익대학교",
        "국민대": "국민대학교", "숭실대": "숭실대학교",
        "세종대": "세종대학교", "광운대": "광운대학교",
        "인하대": "인하대학교", "아주대": "아주대학교",
        "부산대": "부산대학교", "경북대": "경북대학교",
        "전남대": "전남대학교", "전북대": "전북대학교",
        "충남대": "충남대학교", "충북대": "충북대학교",
        "강원대": "강원대학교", "제주대": "제주대학교",
        # 학과
        "컴공": "컴퓨터공학", "컴퓨터": "컴퓨터공학",
        "소프트웨어": "소프트웨어", "SW": "소프트웨어",
        "전전": "전기전자공학", "전자": "전자공학", "전기전자": "전기전자공학",
        "기계": "기계공학", "기공": "기계공학",
        "화공": "화학공학", "화학공": "화학공학",
        "건축": "건축학", "토목": "토목공학",
        "생명": "생명공학", "바이오": "생명공학",
        "산공": "산업공학", "산업공": "산업공학",
        "경영": "경영학", "경제": "경제학", "회계": "회계학",
        "법학": "법학", "로스쿨": "법학",
        "의대": "의학", "의예": "의학", "의학": "의학",
        "치대": "치의학", "치의": "치의학",
        "한의대": "한의학", "한의": "한의학",
        "약대": "약학", "약학": "약학",
        "간호": "간호학", "간호대": "간호학",
        "교대": "교육학", "사범": "교육학",
        "심리": "심리학", "심리학": "심리학",
        "국문": "국어국문학", "영문": "영어영문학",
        "수학": "수학", "물리": "물리학", "화학": "화학",
        "디자인": "디자인", "미대": "미술학",
        "체대": "체육학", "체육": "체육학",
        "음대": "음악학", "음악": "음악학",
        "신방": "신문방송학", "미디어": "신문방송학",
        "행정": "행정학", "정외": "정치외교학", "정치": "정치외교학",
        # 직업
        "개발자": "소프트웨어 개발", "프로그래머": "소프트웨어 개발",
        "의사": "의사", "간호사": "간호사", "약사": "약사",
        "변호사": "변호사", "판사": "판사", "검사": "검사",
        "교사": "교사", "선생님": "교사",
        "공무원": "공무원", "경찰": "경찰관", "소방관": "소방관",
        "디자이너": "디자이너", "건축가": "건축가",
        "회계사": "회계사", "세무사": "세무사",
        "기자": "기자", "PD": "방송 PD", "아나운서": "아나운서",
        "요리사": "조리사", "셰프": "조리사",
        "엔지니어": "엔지니어", "연구원": "연구원",
        "데이터": "데이터 분석", "AI": "인공지능",
        # 경영/사업 관련
        "사업가": "기업 대표", "CEO": "기업 대표", "창업가": "기업 대표",
        "대표": "기업 대표", "경영자": "기업 대표", "사장": "기업 대표",
        "스타트업": "기업 대표", "기업인": "기업 대표",
        "마케터": "마케팅", "기획자": "경영 기획", "컨설턴트": "경영 및 진단",
        "펀드매니저": "금융", "애널리스트": "금융", "트레이더": "금융",
        "보험설계사": "보험", "은행원": "금융",
        # 연구/공학 관련
        "과학자": "연구원", "물리학자": "물리", "화학자": "화학",
        "수학자": "수학", "생물학자": "생명과학",
        "천문학자": "천문", "지질학자": "지질",
        "로봇공학자": "로봇", "AI개발자": "인공지능", "AI연구원": "인공지능",
        "데이터분석가": "데이터", "데이터과학자": "데이터",
        "반도체": "반도체", "자동차엔지니어": "자동차",
        "네트워크": "통신", "서버개발자": "소프트웨어", "웹개발자": "소프트웨어",
        "앱개발자": "소프트웨어", "게임개발자": "게임",
        "해커": "정보보안", "보안전문가": "정보보안",
        # 교육 관련
        "교수": "대학 교수", "강사": "강사", "학원선생님": "강사",
        "유치원교사": "유치원", "보육교사": "유치원",
        # 의료 관련
        "수의사": "수의사", "한의사": "한의사", "치과의사": "치과의사",
        "물리치료사": "물리치료", "작업치료사": "작업치료",
        "방사선사": "방사선", "임상병리사": "임상병리",
        "응급구조사": "응급구조", "치위생사": "치위생",
        "심리상담사": "심리상담", "상담사": "심리상담",
        # 법률/행정 관련
        "변리사": "변리사", "노무사": "노무사", "관세사": "관세사",
        "법무사": "법무사", "행정사": "행정사",
        "감정평가사": "감정평가", "공인중개사": "부동산",
        # 예술/방송/스포츠 관련
        "유튜버": "방송", "크리에이터": "방송", "인플루언서": "방송",
        "BJ": "방송", "스트리머": "방송",
        "작가": "작가", "소설가": "소설가", "시인": "작가",
        "웹툰작가": "만화", "만화가": "만화",
        "화가": "화가", "일러스트레이터": "일러스트",
        "사진작가": "사진", "포토그래퍼": "사진",
        "영화감독": "영화감독", "감독": "영화감독",
        "배우": "연기", "탤런트": "연기", "뮤지컬배우": "연기",
        "가수": "가수", "아이돌": "가수", "래퍼": "가수",
        "댄서": "무용", "안무가": "무용", "발레리나": "무용",
        "작곡가": "작곡", "프로듀서": "음악",
        "운동선수": "운동선수", "축구선수": "운동선수", "야구선수": "운동선수",
        "농구선수": "운동선수", "수영선수": "운동선수",
        "프로게이머": "게임", "e스포츠": "게임",
        "체육교사": "체육", "트레이너": "체육", "피트니스": "체육",
        # 항공/운송 관련
        "파일럿": "항공기 조종사", "조종사": "항공기 조종사",
        "승무원": "항공기 객실", "스튜어디스": "항공기 객실",
        "기관사": "철도", "선장": "선박",
        # 군/경찰/소방
        "군인": "군인", "장교": "군인", "부사관": "군인",
        "해군": "군인", "공군": "군인", "육군": "군인",
        "형사": "경찰관", "수사관": "경찰관",
        "119": "소방관", "구급대원": "소방관",
        # 외교/언어 관련
        "외교관": "외교", "통역사": "통역", "번역가": "번역",
        "동시통역사": "통역",
        # 요식/서비스 관련
        "요리사": "조리사", "셰프": "조리사", "쉐프": "조리사",
        "바리스타": "조리", "제빵사": "제빵", "파티시에": "제빵",
        "소믈리에": "조리", "푸드스타일리스트": "조리",
        "미용사": "미용사", "헤어디자이너": "미용사",
        "메이크업아티스트": "메이크업", "네일아티스트": "네일",
        "피부관리사": "피부",
        # 건설/건축 관련
        "인테리어": "인테리어", "시공": "건설", "감리": "건설",
        "토목기사": "토목", "측량사": "측량",
        # 농림/환경 관련
        "농부": "농업", "어부": "어업", "목장": "축산",
        "플로리스트": "화훼", "조경사": "조경",
        "환경운동가": "환경", "기상캐스터": "기상",
        # 고등학교
        "과고": "과학고", "과학고": "과학고",
        "외고": "외국어고", "외국어고": "외국어고",
        "국제고": "국제고", "자사고": "자율형사립고",
        "특목고": "특목고", "특성화고": "특성화고",
        "마이스터고": "마이스터고", "예고": "예술고",
    }

    # 고등학교 약어 → 검색 키워드 매핑
    HS_ABBREVIATIONS = {
        "서울과고": "서울과학고", "경기과고": "경기과학고",
        "한성과고": "한성과학고", "세종과고": "세종과학예술",
        "대전과고": "대전과학고", "대구과고": "대구과학고",
        "인천과고": "인천과학고", "광주과고": "광주과학고",
        "부산과고": "부산과학고", "울산과고": "울산과학고",
        "대원외고": "대원외국어고", "대일외고": "대일외국어고",
        "명덕외고": "명덕외국어고", "이화외고": "이화외국어고",
        "한영외고": "한영외국어고", "서울외고": "서울외국어고",
        "수원외고": "수원외국어고", "고양외고": "고양외국어고",
        "용인외고": "용인외국어고", "김포외고": "김포외국어고",
        "안양외고": "안양외국어고", "과천외고": "과천외국어고",
        "동두천외고": "동두천외국어고", "성남외고": "성남외국어고",
        "인천외고": "인천외국어고", "부산외고": "부산외국어고",
        "대전외고": "대전외국어고", "대구외고": "대구외국어고",
        "서울국제고": "서울국제고", "세종국제고": "세종국제고",
        "청심국제고": "청심국제고", "동탄국제고": "동탄국제고",
        "미림마이스터": "미림마이스터", "수도전기마이스터": "수도전기",
        "한세사이버보안고": "한세사이버", "서울로봇고": "서울로봇고",
        "민사고": "민족사관고", "상산고": "상산고",
        "하나고": "하나고등학교", "용인한국외대부고": "용인한국외국어대학교부설고",
        "외대부고": "외국어대학교부설고", "북일고": "북일고",
        "현대청운고": "현대청운고", "김천고": "김천고",
        "공주사대부고": "공주대학교사범대학부설고",
    }

    def _expand_abbreviation(self, text: str) -> str:
        """줄임말/약어를 정식 명칭으로 확장"""
        if not text:
            return text
        expanded = text.strip()

        # 고등학교 약어 먼저 체크
        for abbr, full in self.HS_ABBREVIATIONS.items():
            if abbr == expanded or abbr in expanded:
                return full

        # 일반 약어 체크
        for abbr, full in self.ABBREVIATIONS.items():
            if abbr == expanded or abbr in expanded:
                expanded = expanded.replace(abbr, full)
                break
        return expanded

    def compare_with_goal(
        self,
        holland_scores: dict,
        mbti_spectrum: dict,
        goal_job: str = None,
        goal_major: str = None,
    ) -> dict:
        """
        학생 목표와 AI 추천 비교

        Returns:
            매칭도 점수 + 판정 + 강점/보완점
        """
        if not goal_job and not goal_major:
            return None

        # 줄임말/약어 확장
        goal_job = self._expand_abbreviation(goal_job) if goal_job else None
        goal_major = self._expand_abbreviation(goal_major) if goal_major else None

        # 목표 직업/학과에 해당하는 직업 찾기
        target_jobs = self.job_profiles[
            self.job_profiles["jobNm"].str.contains(goal_job or "", na=False) |
            self.job_major_df[self.job_major_df["major"].str.contains(goal_major or "", na=False)]["jobCd"].isin(
                self.job_profiles["jobCd"]
            ) if goal_major else self.job_profiles["jobNm"].str.contains(goal_job or "", na=False)
        ]

        if len(target_jobs) == 0:
            # 직접 매칭 안 되면 키워드 검색
            target_jobs = self.job_profiles[
                self.job_profiles["jobNm"].str.contains(goal_job[:2] if goal_job else "", na=False)
            ]

        if len(target_jobs) == 0:
            return {
                "matchScore": 50,
                "verdict": "보통",
                "message": "목표 직업에 대한 상세 데이터가 부족합니다.",
                "strengths": [],
                "improvements": ["목표를 더 구체적으로 입력하면 정확한 비교가 가능합니다."],
            }

        # 가장 유사한 직업으로 매칭도 계산
        best_match = None
        best_score = 0

        for _, job in target_jobs.iterrows():
            h_sim = self._holland_similarity(holland_scores, job)
            m_sim = self._mbti_similarity(mbti_spectrum, job)
            score = h_sim * 0.6 + m_sim * 0.4
            if score > best_score:
                best_score = score
                best_match = job

        match_score = round(best_score, 0)

        # 판정
        if match_score >= 90:
            verdict = "매우 높음"
            message = "목표와 적성이 매우 잘 맞습니다!"
        elif match_score >= 70:
            verdict = "높음"
            message = "좋은 방향입니다. 목표 달성 가능성이 높아요."
        elif match_score >= 50:
            verdict = "보통"
            message = "가능하지만, 다른 대안도 검토해보세요."
        else:
            verdict = "낮음"
            message = "적성과 다소 차이가 있어요. 다른 경로도 살펴볼까요?"

        # 강점/보완점 분석
        strengths, improvements = self._analyze_fit(holland_scores, mbti_spectrum, best_match)

        # 보완점이 없으면 메시지를 긍정적으로만
        if not improvements:
            if match_score >= 90:
                message = "목표와 적성이 완벽하게 일치합니다! 자신감을 가지고 준비하세요."
            elif match_score >= 70:
                message = "적성과 목표가 잘 맞습니다. 꾸준히 준비하면 충분히 달성 가능합니다."

        return {
            "matchScore": int(match_score),
            "verdict": verdict,
            "message": message,
            "strengths": strengths,
            "improvements": improvements,
        }

    def _analyze_fit(self, holland: dict, mbti: dict, job_row) -> tuple:
        """강점과 보완점 분석"""
        strengths = []
        improvements = []

        # Holland 분석
        job_top3 = str(job_row.get("holland_top3", ""))
        student_sorted = sorted(holland.items(), key=lambda x: x[1], reverse=True)
        student_top3 = [h[0] for h in student_sorted[:3]]

        overlap = set(student_top3) & set(job_top3[:3])
        if len(overlap) >= 2:
            strengths.append("흥미 유형이 해당 직업과 높은 일치를 보입니다")
        elif len(overlap) == 0:
            improvements.append("흥미 유형이 다소 다르므로 관련 활동 경험을 늘려보세요")

        # MBTI 분석
        holland_names = {"R": "현실형", "I": "탐구형", "A": "예술형", "S": "사회형", "E": "진취형", "C": "관습형"}

        ei_diff = abs(mbti.get("EI", 50) - job_row.get("mbti_EI", 50))
        if ei_diff <= 10:
            strengths.append("에너지 방향(E/I)이 직업 특성과 잘 맞습니다")
        elif ei_diff >= 25:
            if mbti.get("EI", 50) > job_row.get("mbti_EI", 50):
                improvements.append("이 직업은 대인관계 활동이 많으므로 팀 경험을 늘려보세요")
            else:
                improvements.append("이 직업은 독립적 작업이 많으므로 집중 훈련이 도움됩니다")

        tf_diff = abs(mbti.get("TF", 50) - job_row.get("mbti_TF", 50))
        if tf_diff <= 10:
            strengths.append("판단 방식(T/F)이 직업 요구와 일치합니다")

        return strengths[:3], improvements[:3]

    # ===========================
    # 3. 고등학교 매칭 (시나리오 2)
    # ===========================

    def match_schools(
        self,
        recommended_jobs: list[dict],
        region: str = None,
        gender: str = "",
        top_n: int = 5,
    ) -> list[dict]:
        """
        추천 진로에 맞는 고등학교 매칭

        Args:
            recommended_jobs: 추천 직업 리스트 (recommend_careers 결과)
            region: 거주 지역 (시도 시군구)
            gender: 성별 ("남" 또는 "여")
            top_n: 추천 학교 수
        """
        # 1. 추천 직업들의 관련 교과목 추출
        top_job_codes = [j["jobCd"] for j in recommended_jobs[:3]]
        related_majors = self.job_major_df[
            self.job_major_df["jobCd"].isin(top_job_codes)
        ]["major"].unique()

        required_subjects = self.major_subject_df[
            self.major_subject_df["major"].isin(related_majors)
        ]["required_subject"].unique().tolist()

        if not required_subjects:
            required_subjects = ["수학Ⅰ", "영어Ⅰ"]  # 폴백

        # 2. 학교별 교과목 커버리지 점수 계산
        school_scores = []

        # 지역 필터링 (시군구 단위)
        target_schools = self.schools_df.copy()
        if region:
            # "서울특별시 강남구" → 도로명주소에서 "강남구" 포함 학교 필터
            region_parts = region.split()
            if len(region_parts) >= 2:
                sigungu = region_parts[1]
                target_schools = target_schools[
                    target_schools["ORG_RDNMA"].str.contains(sigungu, na=False)
                ]
            else:
                target_schools = target_schools[
                    target_schools["LCTN_SC_NM"].str.contains(region_parts[0][:2], na=False) |
                    target_schools["ATPT_OFCDC_SC_NM"].str.contains(region_parts[0][:2], na=False)
                ]

        # 시군구 필터 후 학교가 너무 적으면 시/도 전체로 확장
        if len(target_schools) < 10 and region:
            sido = region.split()[0]
            target_schools = self.schools_df[
                self.schools_df["LCTN_SC_NM"].str.contains(sido[:2], na=False) |
                self.schools_df["ATPT_OFCDC_SC_NM"].str.contains(sido[:2], na=False)
            ]

        # 성별 필터: 남학생이면 여학교 제외, 여학생이면 남학교 제외
        if gender == "남":
            target_schools = target_schools[target_schools["COEDU_SC_NM"] != "여"]
        elif gender == "여":
            target_schools = target_schools[target_schools["COEDU_SC_NM"] != "남"]

        for _, school in target_schools.iterrows():
            school_code = str(school["SD_SCHUL_CODE"])

            # 해당 학교의 개설 과목
            school_subjects = self.school_subjects_df[
                self.school_subjects_df["SD_SCHUL_CODE"].astype(str) == school_code
            ]["SUBJECT"].tolist()

            if not school_subjects:
                continue

            # 교과목 커버리지 점수
            covered = sum(1 for s in required_subjects if any(s in ss for ss in school_subjects))
            coverage_score = (covered / len(required_subjects)) * 100 if required_subjects else 0

            # 학교 유형 보너스
            type_bonus = 0
            hs_type = str(school.get("HS_SC_NM", ""))
            if "특목" in hs_type:
                type_bonus = 5
            elif "자율" in hs_type:
                type_bonus = 3

            # 근거리 보너스 (동 정보로 주소 매칭)
            proximity_bonus = 0
            school_address = str(school.get("ORG_RDNMA", ""))
            region_parts = region.split() if region else []
            if len(region_parts) >= 3:
                dong_name = region_parts[2]
                if dong_name in school_address:
                    proximity_bonus = 8
                elif len(region_parts) >= 2 and region_parts[1] in school_address:
                    proximity_bonus = 3
            elif len(region_parts) >= 2:
                if region_parts[1] in school_address:
                    proximity_bonus = 3

            final_score = min(100, coverage_score + type_bonus + proximity_bonus)

            school_scores.append({
                "schoolCode": school_code,
                "name": school["SCHUL_NM"],
                "type": self._classify_school_type(school),
                "matchScore": round(final_score, 0),
                "address": school.get("ORG_RDNMA", ""),
                "homepageUrl": school.get("HMPG_ADRES", ""),
                "region": school.get("LCTN_SC_NM", ""),
                "coveredSubjects": covered,
                "totalRequired": len(required_subjects),
            })

        # 정렬 + 유형 다양성 보장
        school_scores.sort(key=lambda x: x["matchScore"], reverse=True)
        diversified = self._diversify_schools(school_scores, top_n)

        # 추천 이유 생성
        for s in diversified:
            s["reasons"] = self._generate_school_reasons(s, required_subjects)

        return diversified

    def _classify_school_type(self, school_row) -> str:
        """학교 유형 분류"""
        hs_type = str(school_row.get("HS_SC_NM", ""))
        special = str(school_row.get("SPCLY_PURPS_HS_ORD_NM", ""))

        if "특목" in hs_type:
            if "과학" in special:
                return "과학고"
            elif "외국어" in special or "외고" in special:
                return "외국어고"
            elif "국제" in special:
                return "국제고"
            return "특목고"
        elif "특성화" in hs_type:
            return "특성화고"
        elif "자율" in hs_type:
            return "자율형사립고"
        return "일반고"

    def _diversify_schools(self, schools: list, top_n: int) -> list:
        """학교 유형 다양성 보장"""
        result = []
        type_count = {}

        for s in schools:
            t = s["type"]
            if type_count.get(t, 0) < 3:  # 같은 유형 최대 3개
                result.append(s)
                type_count[t] = type_count.get(t, 0) + 1
            if len(result) >= top_n:
                break

        return result

    def _generate_school_reasons(self, school: dict, required_subjects: list) -> list:
        """학교 추천 이유 생성 (차별화된 이유)"""
        reasons = []
        coverage = school["coveredSubjects"]
        total = school["totalRequired"]
        school_type = school["type"]

        # 교과목 커버리지 기반 이유
        if coverage == total:
            reasons.append(f"진로 필수 과목 {total}개 전체 개설")
        elif coverage >= total * 0.8:
            reasons.append(f"진로 필수 과목 {coverage}/{total}개 개설 (커버리지 우수)")
        else:
            reasons.append(f"진로 관련 과목 {coverage}/{total}개 개설")

        # 학교 유형별 차별화 이유
        if school_type == "과학고":
            reasons.append("과학·수학 심화 교육과정으로 이공계 진학에 유리")
        elif school_type == "외국어고":
            reasons.append("외국어 집중 교육으로 글로벌 진로에 적합")
        elif school_type == "특성화고":
            reasons.append("실무 중심 교육과정으로 조기 취업 가능")
        elif school_type == "마이스터고":
            reasons.append("산업체 협약 기반 취업 보장형 교육")
        elif school_type == "자율형사립고":
            reasons.append("다양한 선택과목 운영으로 맞춤형 교육 가능")
        elif school_type == "일반고":
            # 일반고는 주소 기반으로 근접성 강조
            address = school.get("address", "")
            if address:
                # 시군구 추출
                parts = address.split()
                if len(parts) >= 3:
                    reasons.append(f"{parts[1]} {parts[2]} 소재 (거주지 근접)")
                else:
                    reasons.append("거주지 인근 소재")

        # 적합도 기반 추가 이유
        if school["matchScore"] >= 90:
            reasons.append("교육과정이 목표 진로와 매우 높은 연관성")
        elif school["matchScore"] >= 80:
            reasons.append("진로 연계 교과 편성 양호")

        return reasons[:3]

    # ===========================
    # 4. 교육과정 로드맵 (시나리오 3)
    # ===========================

    def generate_roadmap(
        self,
        recommended_jobs: list[dict],
        grade: str = "중3",
    ) -> list[dict]:
        """추천 진로 기반 교육과정 로드맵 생성"""

        # 추천 직업의 관련 교과목 추출
        top_job_codes = [j["jobCd"] for j in recommended_jobs[:3]]
        related_majors = self.job_major_df[
            self.job_major_df["jobCd"].isin(top_job_codes)
        ]["major"].unique()

        all_subjects = self.major_subject_df[
            self.major_subject_df["major"].isin(related_majors)
        ]["required_subject"].unique().tolist()

        # 과목을 학년별로 분배 (난이도 기반)
        grade1_keywords = ["통합", "Ⅰ", "정보", "한국사", "체육", "음악", "미술"]
        grade2_keywords = ["Ⅰ", "확률", "미적분"]
        grade3_keywords = ["Ⅱ", "기하", "공학", "심화"]

        roadmap = [
            {
                "grade": "고1",
                "goal": "기초 다지기",
                "subjects": [s for s in all_subjects if any(k in s for k in grade1_keywords)][:5] or ["통합과학", "수학Ⅰ", "정보", "영어Ⅰ", "한국사"],
                "activities": ["관련 동아리 가입", "진로 탐색 독서", "기초 대회 참가"],
            },
            {
                "grade": "고2",
                "goal": "심화 준비",
                "subjects": [s for s in all_subjects if any(k in s for k in grade2_keywords)][:5] or ["수학Ⅱ", "미적분", "확률과 통계"],
                "activities": ["심화 대회 도전", "관련 분야 소논문", "진로 체험 프로그램"],
            },
            {
                "grade": "고3",
                "goal": "전공 연계",
                "subjects": [s for s in all_subjects if any(k in s for k in grade3_keywords)][:5] or ["관련 전문 과목"],
                "activities": ["포트폴리오 정리", "대학 연계 프로그램", "자기소개서 준비"],
            },
        ]

        return roadmap


# 테스트
if __name__ == "__main__":
    engine = MatchingEngine()

    # 테스트: 탐구형 + 내향적 + 사고형 학생
    test_holland = {"R": 40, "I": 85, "A": 30, "S": 35, "E": 25, "C": 60}
    test_mbti = {"EI": 70, "SN": 35, "TF": 30, "JP": 40}

    print("=" * 50)
    print("테스트: 탐구형(I) + 내향적 + 사고형(T) 학생")
    print("=" * 50)

    # 진로 추천
    careers = engine.recommend_careers(test_holland, test_mbti, top_n=5)
    print("\n🎯 추천 진로 Top 5:")
    for c in careers:
        print(f"  {c['rank']}. {c['jobNm']} (적합도: {c['matchScore']}%)")
        print(f"     이유: {c['reason']}")
        print(f"     관련학과: {', '.join(c['relatedMajors'])}")
        print()

    # 목표 비교
    comparison = engine.compare_with_goal(test_holland, test_mbti, goal_job="소프트웨어")
    if comparison:
        print(f"🎯 목표 매칭도: {comparison['matchScore']}% ({comparison['verdict']})")
        print(f"   {comparison['message']}")

    # 학교 매칭
    schools = engine.match_schools(careers, region="서울", top_n=5)
    print(f"\n🏫 추천 학교 (서울):")
    for s in schools:
        print(f"  {s['name']} ({s['type']}) - 적합도 {s['matchScore']}%")
        print(f"    이유: {', '.join(s['reasons'])}")
        print()

    # 로드맵
    roadmap = engine.generate_roadmap(careers)
    print("📚 교육과정 로드맵:")
    for r in roadmap:
        print(f"  {r['grade']} ({r['goal']}): {', '.join(r['subjects'][:4])}")
