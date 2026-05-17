"""
워크넷 직업 데이터 기반 Holland 코드 매핑 생성

Holland 6유형과 워크넷 능력/지식 키워드 매핑:
- R(현실형): 기계, 장비, 설치, 조작, 신체적, 건축
- I(탐구형): 논리적 분석, 추리력, 수리력, 연구, 물리, 화학, 생물
- A(예술형): 창의력, 예술, 디자인, 글쓰기, 음악
- S(사회형): 서비스 지향, 가르치기, 상담, 사람 파악, 교육
- E(진취형): 설득, 협상, 인적자원 관리, 판단과 의사결정, 경영
- C(관습형): 사무, 정확성, 범주화, 모니터링, 재정 관리
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

# Holland 유형별 관련 능력/지식 키워드 & 가중치
HOLLAND_KEYWORDS = {
    "R": {
        "abilities": ["장비 선정", "장비의 유지", "설치", "조작 및 통제", "작동 점검",
                      "고장의 발견", "신체적 강인성", "정교한 동작", "움직임 통제"],
        "knowledge": ["기계", "건축 및 설계", "공학과 기술", "식품생산", "운송"],
    },
    "I": {
        "abilities": ["논리적 분석", "추리력", "수리력", "문제 해결", "기술 분석",
                      "기술 설계", "범주화", "학습전략"],
        "knowledge": ["물리", "화학", "생물", "산수와 수학", "컴퓨터와 전자공학"],
    },
    "A": {
        "abilities": ["창의력", "글쓰기", "공간지각력"],
        "knowledge": ["예술", "디자인", "의사소통과 미디어"],
    },
    "S": {
        "abilities": ["서비스 지향", "가르치기", "사람 파악", "듣고 이해하기"],
        "knowledge": ["교육 및 훈련", "상담", "심리", "의료", "사회와 인류"],
    },
    "E": {
        "abilities": ["설득", "협상", "인적자원 관리", "판단과 의사결정", "시간 관리",
                      "모니터링", "재정 관리", "물적자원 관리"],
        "knowledge": ["경영 및 행정", "영업과 마케팅", "경제와 회계", "인사", "법"],
    },
    "C": {
        "abilities": ["읽고 이해하기", "전산", "선택적 집중력", "기억력",
                      "품질관리분석", "행동조정"],
        "knowledge": ["사무", "고객서비스", "안전과 보안", "통신"],
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
        # jobAbilCmpr: 능력 비교 점수 (평균 기준)
        for el in root.findall("jobAbilCmpr"):
            name = el.findtext("jobAblNmCmpr", "").strip()
            score = float(el.findtext("jobAblStatusCmpr", "0"))
            if name:
                abilities[name] = score

        knowledge = {}
        # KnwldgCmpr: 지식 비교 점수
        for el in root.findall("KnwldgCmpr"):
            name = el.findtext("knwldgNmCmpr", "").strip()
            score = float(el.findtext("knwldgStatusCmpr", "0"))
            if name:
                knowledge[name] = score

        return {"abilities": abilities, "knowledge": knowledge}
    except Exception:
        return {"abilities": {}, "knowledge": {}}


def calculate_holland_scores(abilities: dict, knowledge: dict) -> dict:
    """능력/지식 점수를 기반으로 Holland 6유형 점수 계산"""
    holland_scores = {}

    for code, keywords in HOLLAND_KEYWORDS.items():
        score_sum = 0
        count = 0

        # 능력 점수 계산
        for keyword in keywords["abilities"]:
            for ability_name, ability_score in abilities.items():
                if keyword in ability_name:
                    score_sum += ability_score
                    count += 1
                    break

        # 지식 점수 계산
        for keyword in keywords["knowledge"]:
            for knowledge_name, knowledge_score in knowledge.items():
                if keyword in knowledge_name:
                    score_sum += knowledge_score
                    count += 1
                    break

        holland_scores[code] = round(score_sum / count, 2) if count > 0 else 0

    return holland_scores


def get_top3_codes(holland_scores: dict) -> str:
    """상위 3개 Holland 코드 반환"""
    sorted_codes = sorted(holland_scores.items(), key=lambda x: x[1], reverse=True)
    return "".join([c[0] for c in sorted_codes[:3]])


def main():
    print("=" * 50)
    print("Holland 코드 매핑 생성 (워크넷 능력/지식 데이터 기반)")
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

        # Holland 점수 계산
        holland_scores = calculate_holland_scores(abilities, knowledge)
        top3 = get_top3_codes(holland_scores)

        results.append({
            "jobCd": job_cd,
            "jobNm": job_nm,
            "jobLrclNm": row.get("jobLrclNm", ""),
            "holland_R": holland_scores.get("R", 0),
            "holland_I": holland_scores.get("I", 0),
            "holland_A": holland_scores.get("A", 0),
            "holland_S": holland_scores.get("S", 0),
            "holland_E": holland_scores.get("E", 0),
            "holland_C": holland_scores.get("C", 0),
            "holland_top3": top3,
        })

        time.sleep(0.3)

    # 저장
    result_df = pd.DataFrame(results)
    output_path = "data/raw/holland_job_mapping.csv"
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print(f"Holland 매핑 완료!")
    print(f"저장: {output_path}")
    print(f"\nHolland Top3 코드 분포 (상위 10):")
    print(result_df["holland_top3"].value_counts().head(10).to_string())
    print(f"\n샘플:")
    print(result_df[["jobNm", "holland_top3", "holland_R", "holland_I", "holland_A", "holland_S", "holland_E", "holland_C"]].head(5).to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
