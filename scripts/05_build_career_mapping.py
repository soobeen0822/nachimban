"""
직업 → 학과 → 필요 교과목 매핑 테이블 생성

1) 워크넷 'way' 필드에서 관련 학과 키워드 추출
2) 학과 → 고등학교 필요 교과목 매핑 (규칙 기반)
3) 최종: 직업 → 학과 → 교과목 연결 테이블
"""

import re
import pandas as pd

# ============================
# 1. 대학 학과 분류 사전
# ============================

MAJOR_KEYWORDS = {
    # 공학계열
    "컴퓨터공학": ["컴퓨터", "소프트웨어", "전산", "정보통신", "IT"],
    "전자공학": ["전자", "전기전자", "반도체"],
    "기계공학": ["기계", "자동차", "로봇"],
    "화학공학": ["화공", "화학공학", "재료", "신소재"],
    "건축학": ["건축", "건설", "토목"],
    "생명공학": ["생명공학", "바이오", "유전공학"],
    "환경공학": ["환경공학", "환경"],
    "산업공학": ["산업공학", "시스템"],
    "항공우주공학": ["항공", "우주"],
    # 자연과학계열
    "수학": ["수학", "통계"],
    "물리학": ["물리"],
    "화학": ["화학과"],
    "생물학": ["생물", "생명과학"],
    # 의학계열
    "의학": ["의학", "의대", "의사"],
    "간호학": ["간호"],
    "약학": ["약학", "약사"],
    "치의학": ["치의학", "치과"],
    "한의학": ["한의학", "한의사"],
    # 경영/경제계열
    "경영학": ["경영", "비즈니스", "MBA"],
    "경제학": ["경제"],
    "회계학": ["회계", "세무"],
    "무역학": ["무역", "국제통상"],
    "금융학": ["금융", "재무"],
    # 사회과학계열
    "법학": ["법학", "법률", "법과"],
    "행정학": ["행정"],
    "심리학": ["심리"],
    "사회학": ["사회학", "사회복지"],
    "정치외교학": ["정치", "외교"],
    # 인문계열
    "국어국문학": ["국어국문", "국문학", "문예창작"],
    "영어영문학": ["영어영문", "영문학", "영어"],
    "사학": ["역사", "사학"],
    "철학": ["철학"],
    # 교육계열
    "교육학": ["교육학", "교육"],
    "사범대": ["사범", "교사", "교원"],
    # 예체능계열
    "미술학": ["미술", "디자인", "시각"],
    "음악학": ["음악", "작곡", "성악"],
    "체육학": ["체육", "스포츠"],
    "연극영화학": ["연극", "영화", "방송", "연기"],
    # 기타
    "신문방송학": ["신문방송", "언론", "미디어", "커뮤니케이션"],
    "광고홍보학": ["광고", "홍보"],
    "관광학": ["관광", "호텔", "외식"],
    "농학": ["농업", "농학", "원예", "축산"],
    "수산학": ["수산", "해양"],
    "식품영양학": ["식품", "영양", "조리"],
}

# ============================
# 2. 학과 → 고등학교 교과목 매핑
# ============================

MAJOR_TO_SUBJECTS = {
    # 공학계열
    "컴퓨터공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "확률과 통계", "정보", "물리학Ⅰ"],
    "전자공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "물리학Ⅰ", "물리학Ⅱ", "정보"],
    "기계공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "기하", "물리학Ⅰ", "물리학Ⅱ", "공학일반"],
    "화학공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "화학Ⅰ", "화학Ⅱ", "물리학Ⅰ"],
    "건축학": ["수학Ⅰ", "수학Ⅱ", "미적분", "물리학Ⅰ", "미술", "기하"],
    "생명공학": ["생명과학Ⅰ", "생명과학Ⅱ", "화학Ⅰ", "수학Ⅰ", "수학Ⅱ"],
    "환경공학": ["화학Ⅰ", "생명과학Ⅰ", "지구과학Ⅰ", "수학Ⅰ"],
    "산업공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "확률과 통계", "정보"],
    "항공우주공학": ["수학Ⅰ", "수학Ⅱ", "미적분", "기하", "물리학Ⅰ", "물리학Ⅱ"],
    # 자연과학계열
    "수학": ["수학Ⅰ", "수학Ⅱ", "미적분", "기하", "확률과 통계"],
    "물리학": ["물리학Ⅰ", "물리학Ⅱ", "수학Ⅰ", "수학Ⅱ", "미적분"],
    "화학": ["화학Ⅰ", "화학Ⅱ", "수학Ⅰ", "수학Ⅱ", "물리학Ⅰ"],
    "생물학": ["생명과학Ⅰ", "생명과학Ⅱ", "화학Ⅰ", "수학Ⅰ"],
    # 의학계열
    "의학": ["생명과학Ⅰ", "생명과학Ⅱ", "화학Ⅰ", "화학Ⅱ", "물리학Ⅰ", "수학Ⅰ", "수학Ⅱ"],
    "간호학": ["생명과학Ⅰ", "화학Ⅰ", "수학Ⅰ", "영어Ⅰ"],
    "약학": ["화학Ⅰ", "화학Ⅱ", "생명과학Ⅰ", "수학Ⅰ", "수학Ⅱ", "미적분"],
    "치의학": ["생명과학Ⅰ", "화학Ⅰ", "물리학Ⅰ", "수학Ⅰ"],
    "한의학": ["생명과학Ⅰ", "화학Ⅰ", "수학Ⅰ", "한문"],
    # 경영/경제계열
    "경영학": ["수학Ⅰ", "수학Ⅱ", "확률과 통계", "영어Ⅰ", "사회·문화"],
    "경제학": ["수학Ⅰ", "수학Ⅱ", "미적분", "확률과 통계", "경제"],
    "회계학": ["수학Ⅰ", "확률과 통계", "경제", "영어Ⅰ"],
    "무역학": ["영어Ⅰ", "영어Ⅱ", "경제", "사회·문화"],
    "금융학": ["수학Ⅰ", "수학Ⅱ", "확률과 통계", "경제"],
    # 사회과학계열
    "법학": ["사회·문화", "정치와 법", "생활과 윤리", "한국사", "영어Ⅰ"],
    "행정학": ["사회·문화", "정치와 법", "한국사", "경제"],
    "심리학": ["생명과학Ⅰ", "사회·문화", "수학Ⅰ", "확률과 통계"],
    "사회학": ["사회·문화", "생활과 윤리", "한국사"],
    "정치외교학": ["정치와 법", "세계사", "영어Ⅰ", "사회·문화"],
    # 인문계열
    "국어국문학": ["문학", "독서", "언어와 매체", "한국사"],
    "영어영문학": ["영어Ⅰ", "영어Ⅱ", "영어 회화", "문학"],
    "사학": ["한국사", "세계사", "동아시아사", "사회·문화"],
    "철학": ["생활과 윤리", "윤리와 사상", "논리학"],
    # 교육계열
    "교육학": ["사회·문화", "심리학", "영어Ⅰ", "수학Ⅰ"],
    "사범대": ["해당 전공 교과", "교육학", "영어Ⅰ"],
    # 예체능계열
    "미술학": ["미술", "미술 창작", "미술 감상과 비평"],
    "음악학": ["음악", "음악 연주", "음악 감상과 비평"],
    "체육학": ["체육", "스포츠 생활", "운동과 건강"],
    "연극영화학": ["연극", "영화", "문학", "미술"],
    # 기타
    "신문방송학": ["사회·문화", "영어Ⅰ", "문학", "정보"],
    "광고홍보학": ["사회·문화", "영어Ⅰ", "미술", "심리학"],
    "관광학": ["영어Ⅰ", "영어Ⅱ", "사회·문화", "세계지리"],
    "농학": ["생명과학Ⅰ", "화학Ⅰ", "지구과학Ⅰ"],
    "수산학": ["생명과학Ⅰ", "지구과학Ⅰ", "화학Ⅰ"],
    "식품영양학": ["화학Ⅰ", "생명과학Ⅰ", "수학Ⅰ"],
}


def extract_majors_from_text(text: str) -> list[str]:
    """텍스트에서 관련 학과를 추출"""
    if not text or pd.isna(text):
        return []

    found_majors = []
    for major_name, keywords in MAJOR_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_majors.append(major_name)
                break

    return found_majors


def main():
    print("=" * 50)
    print("직업 → 학과 → 교과목 매핑 테이블 생성")
    print("=" * 50)

    # 직업 데이터 로드
    jobs_df = pd.read_csv("data/raw/work24_jobs.csv")
    holland_df = pd.read_csv("data/raw/holland_job_mapping.csv")

    # Holland 코드 병합
    jobs_df = jobs_df.merge(
        holland_df[["jobCd", "holland_top3", "holland_R", "holland_I", "holland_A",
                    "holland_S", "holland_E", "holland_C"]],
        on="jobCd",
        how="left"
    )

    # 1. 직업-학과 매핑 추출
    print("\n1. 직업별 관련 학과 추출 중...")
    job_major_records = []

    for _, row in jobs_df.iterrows():
        text = f"{row.get('way', '')} {row.get('jobSum', '')}"
        majors = extract_majors_from_text(text)

        if not majors:
            # way 필드에 학과 정보 없으면 대분류로 기본 매핑
            lrcl = row.get("jobLrclNm", "")
            if "공학" in lrcl or "연구" in lrcl:
                majors = ["컴퓨터공학", "전자공학", "기계공학"]
            elif "경영" in lrcl or "금융" in lrcl:
                majors = ["경영학", "경제학"]
            elif "교육" in lrcl or "사회복지" in lrcl:
                majors = ["교육학", "사회학"]
            elif "보건" in lrcl or "의료" in lrcl:
                majors = ["의학", "간호학"]
            elif "예술" in lrcl or "디자인" in lrcl:
                majors = ["미술학", "연극영화학"]
            else:
                majors = ["경영학"]  # 기본 폴백

        for major in majors:
            job_major_records.append({
                "jobCd": row["jobCd"],
                "jobNm": row["jobNm"],
                "jobLrclNm": row.get("jobLrclNm", ""),
                "holland_top3": row.get("holland_top3", ""),
                "major": major,
            })

    job_major_df = pd.DataFrame(job_major_records)
    print(f"  직업-학과 매핑: {len(job_major_df)}개 레코드")

    # 2. 학과-교과목 매핑 테이블 생성
    print("\n2. 학과-교과목 매핑 테이블 생성...")
    major_subject_records = []
    for major, subjects in MAJOR_TO_SUBJECTS.items():
        for subj in subjects:
            major_subject_records.append({
                "major": major,
                "required_subject": subj,
            })

    major_subject_df = pd.DataFrame(major_subject_records)
    print(f"  학과-교과목 매핑: {len(major_subject_df)}개 레코드")

    # 3. 최종 통합: 직업 → 학과 → 교과목
    print("\n3. 통합 매핑 생성...")
    full_mapping = job_major_df.merge(major_subject_df, on="major", how="left")
    print(f"  최종 매핑: {len(full_mapping)}개 레코드")

    # 저장
    job_major_df.to_csv("data/raw/job_major_mapping.csv", index=False, encoding="utf-8-sig")
    major_subject_df.to_csv("data/raw/major_subject_mapping.csv", index=False, encoding="utf-8-sig")
    full_mapping.to_csv("data/raw/full_career_mapping.csv", index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print("저장 완료:")
    print(f"  data/raw/job_major_mapping.csv ({len(job_major_df)}행)")
    print(f"  data/raw/major_subject_mapping.csv ({len(major_subject_df)}행)")
    print(f"  data/raw/full_career_mapping.csv ({len(full_mapping)}행)")
    print(f"\n학과별 직업 수 Top 10:")
    print(job_major_df["major"].value_counts().head(10).to_string())
    print(f"\n샘플 (소프트웨어 개발자):")
    sample = full_mapping[full_mapping["jobNm"].str.contains("소프트웨어|컴퓨터|프로그래머", na=False)].head(10)
    if len(sample) > 0:
        print(sample[["jobNm", "major", "required_subject"]].to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
