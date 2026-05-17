"""
직업별 MBTI 스펙트럼 프로필 생성 (워크넷 능력/지식 데이터 기반)

각 직업에 대해 MBTI 4축 연속값 (0~100)을 산출:
- EI: 0=극강E, 100=극강I
- SN: 0=극강S, 100=극강N
- TF: 0=극강T, 100=극강F
- JP: 0=극강J, 100=극강P
"""

import os
import time
import xml.etree.ElementTree as ET
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WORK24_JOB_API_KEY")
BASE_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo212L01.do"

# MBTI 축별 관련 능력/지식 키워드
# 각 축: [첫번째 방향 키워드, 두번째 방향 키워드]
# EI: E방향 능력 vs I방향 능력
MBTI_AXIS_MAPPING = {
    "EI": {
        # E 방향 (낮은 값): 외향적, 대인관계, 설득, 협상
        "E_abilities": ["설득", "협상", "말하기", "인적자원 관리", "가르치기", "서비스 지향"],
        "E_knowledge": ["영업과 마케팅", "인사", "고객서비스"],
        # I 방향 (높은 값): 내향적, 독립적, 분석, 집중
        "I_abilities": ["논리적 분석", "추리력", "선택적 집중력", "기술 분석", "기술 설계", "읽고 이해하기"],
        "I_knowledge": ["물리", "화학", "산수와 수학", "컴퓨터와 전자공학"],
    },
    "SN": {
        # S 방향 (낮은 값): 감각적, 실용적, 구체적, 실무
        "S_abilities": ["정교한 동작", "장비 선정", "장비의 유지", "조작 및 통제", "작동 점검", "품질관리분석"],
        "S_knowledge": ["기계", "건축 및 설계", "식품생산", "운송"],
        # N 방향 (높은 값): 직관적, 추상적, 이론적, 창의적
        "N_abilities": ["창의력", "추리력", "학습전략", "기술 설계", "범주화"],
        "N_knowledge": ["디자인", "예술", "의사소통과 미디어", "철학과 신학"],
    },
    "TF": {
        # T 방향 (낮은 값): 사고적, 논리적, 객관적
        "T_abilities": ["논리적 분석", "수리력", "문제 해결", "판단과 의사결정", "기술 분석"],
        "T_knowledge": ["산수와 수학", "물리", "경제와 회계", "공학과 기술"],
        # F 방향 (높은 값): 감정적, 공감적, 관계 중심
        "F_abilities": ["서비스 지향", "사람 파악", "가르치기", "듣고 이해하기"],
        "F_knowledge": ["상담", "심리", "교육 및 훈련", "사회와 인류"],
    },
    "JP": {
        # J 방향 (낮은 값): 계획적, 체계적, 관리
        "J_abilities": ["시간 관리", "모니터링", "재정 관리", "물적자원 관리", "인적자원 관리"],
        "J_knowledge": ["경영 및 행정", "사무", "안전과 보안", "법"],
        # P 방향 (높은 값): 유연적, 즉흥적, 탐색적
        "P_abilities": ["창의력", "행동조정", "기술 설계", "학습전략"],
        "P_knowledge": ["예술", "디자인", "의사소통과 미디어"],
    },
}


def fetch_job_abilities(job_cd: str) -> dict:
    """직업의 능력/지식 점수 조회 (dtlGb=5)"""
    params = {
        "authKey": API_KEY,
        "returnType": "XML",
        "target": "JOBDTL",
        "jobGb": "1",
        "dtlGb": "5",
        "jobCd": job_cd,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        root = ET.fromstring(resp.text)

        abilities = {}
        for el in root.findall("jobAbilCmpr"):
            name = el.findtext("jobAblNmCmpr", "").strip()
            score = float(el.findtext("jobAblStatusCmpr", "0"))
            if name:
                abilities[name] = score

        knowledge = {}
        for el in root.findall("KnwldgCmpr"):
            name = el.findtext("knwldgNmCmpr", "").strip()
            score = float(el.findtext("knwldgStatusCmpr", "0"))
            if name:
                knowledge[name] = score

        return {"abilities": abilities, "knowledge": knowledge}
    except Exception:
        return {"abilities": {}, "knowledge": {}}


def get_keyword_score(abilities: dict, knowledge: dict, keywords_abilities: list, keywords_knowledge: list) -> float:
    """키워드 리스트에 해당하는 평균 점수 계산 (0~5 스케일)"""
    scores = []

    for keyword in keywords_abilities:
        for name, score in abilities.items():
            if keyword in name:
                scores.append(score)
                break

    for keyword in keywords_knowledge:
        for name, score in knowledge.items():
            if keyword in name:
                scores.append(score)
                break

    return sum(scores) / len(scores) if scores else 2.5  # 기본값 중간


def calculate_mbti_profile(abilities: dict, knowledge: dict) -> dict:
    """능력/지식 데이터로 MBTI 4축 연속값 (0~100) 계산"""
    profile = {}

    for axis, mapping in MBTI_AXIS_MAPPING.items():
        first_letter = axis[0]  # E, S, T, J
        second_letter = axis[1]  # I, N, F, P

        # 첫번째 방향 점수 (E, S, T, J)
        first_score = get_keyword_score(
            abilities, knowledge,
            mapping[f"{first_letter}_abilities"],
            mapping[f"{first_letter}_knowledge"]
        )

        # 두번째 방향 점수 (I, N, F, P)
        second_score = get_keyword_score(
            abilities, knowledge,
            mapping[f"{second_letter}_abilities"],
            mapping[f"{second_letter}_knowledge"]
        )

        # 0~100 변환: 첫번째 방향이 강하면 0에 가깝고, 두번째 방향이 강하면 100에 가까움
        total = first_score + second_score
        if total > 0:
            ratio = second_score / total  # 0~1
            value = round(ratio * 100)
        else:
            value = 50  # 중간값

        profile[axis] = max(0, min(100, value))  # 0~100 클램핑

    return profile


def main():
    print("=" * 50)
    print("직업별 MBTI 스펙트럼 프로필 생성")
    print("(워크넷 능력/지식 데이터 기반)")
    print("=" * 50)

    # 직업 목록 로드
    jobs_df = pd.read_csv("data/raw/work24_jobs.csv")
    print(f"총 {len(jobs_df)}개 직업 처리")

    results = []

    for i, row in jobs_df.iterrows():
        if i % 50 == 0:
            print(f"진행: {i}/{len(jobs_df)}...")

        job_cd = row["jobCd"]
        job_nm = row["jobNm"]

        # API에서 능력/지식 데이터 조회
        data = fetch_job_abilities(job_cd)
        abilities = data["abilities"]
        knowledge = data["knowledge"]

        # MBTI 프로필 계산
        mbti_profile = calculate_mbti_profile(abilities, knowledge)

        results.append({
            "jobCd": job_cd,
            "jobNm": job_nm,
            "jobLrclNm": row.get("jobLrclNm", ""),
            "mbti_EI": mbti_profile["EI"],
            "mbti_SN": mbti_profile["SN"],
            "mbti_TF": mbti_profile["TF"],
            "mbti_JP": mbti_profile["JP"],
        })

        time.sleep(0.3)

    # 저장
    result_df = pd.DataFrame(results)
    output_path = "data/raw/mbti_job_profile.csv"
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # 분석 출력
    print(f"\n{'=' * 50}")
    print(f"MBTI 직업 프로필 생성 완료!")
    print(f"저장: {output_path}")
    print(f"\n각 축 통계:")
    for axis in ["mbti_EI", "mbti_SN", "mbti_TF", "mbti_JP"]:
        print(f"  {axis}: 평균={result_df[axis].mean():.1f}, 최소={result_df[axis].min()}, 최대={result_df[axis].max()}")

    print(f"\n샘플 (직업별 MBTI 프로필):")
    sample_jobs = ["소프트웨어 개발자", "간호사", "초등학교 교사", "건축가", "경영 컨설턴트"]
    for job_name in sample_jobs:
        match = result_df[result_df["jobNm"].str.contains(job_name, na=False)]
        if len(match) > 0:
            r = match.iloc[0]
            print(f"  {r['jobNm']}: EI={r['mbti_EI']}, SN={r['mbti_SN']}, TF={r['mbti_TF']}, JP={r['mbti_JP']}")

    print(f"\n직업 대분류별 평균 MBTI:")
    avg = result_df.groupby("jobLrclNm")[["mbti_EI", "mbti_SN", "mbti_TF", "mbti_JP"]].mean().round(1)
    print(avg.to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
