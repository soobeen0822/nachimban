"""
나이스(NEIS) API - 고등학교별 개설 교과목 수집
시간표 API에서 학교별 고유 과목명을 추출
"""

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEIS_API_KEY")
TIMETABLE_URL = "https://open.neis.go.kr/hub/hisTimetable"

# 최근 1주간 시간표에서 과목 추출 (2025년 4월 기준)
QUERY_FROM = "20250407"
QUERY_TO = "20250411"


def fetch_school_subjects(atpt_code: str, school_code: str) -> list[str]:
    """한 학교의 개설 과목 목록 추출 (1주 시간표 기반)"""
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 1000,  # 1주 시간표 전부
        "ATPT_OFCDC_SC_CODE": atpt_code,
        "SD_SCHUL_CODE": school_code,
        "TI_FROM_YMD": QUERY_FROM,
        "TI_TO_YMD": QUERY_TO,
    }
    try:
        resp = requests.get(TIMETABLE_URL, params=params, timeout=10)
        data = resp.json()

        if "hisTimetable" not in data:
            return []

        rows = data["hisTimetable"][1]["row"]
        subjects = set()
        for r in rows:
            subj = r.get("ITRT_CNTNT", "").strip()
            if subj and subj not in ("", "입학식", "졸업식", "자습", "방학"):
                subjects.add(subj)
        return sorted(subjects)

    except Exception as e:
        return []


def main():
    print("=" * 50)
    print("나이스 API - 고등학교별 개설 교과목 수집")
    print(f"조회 기간: {QUERY_FROM} ~ {QUERY_TO}")
    print("=" * 50)

    # 학교 목록 로드
    schools_df = pd.read_csv("data/raw/neis_high_schools.csv")
    print(f"총 {len(schools_df)}개 학교 대상")

    all_records = []
    success_count = 0
    empty_count = 0

    for i, row in schools_df.iterrows():
        if i % 100 == 0:
            print(f"진행: {i}/{len(schools_df)} (성공: {success_count}, 빈 데이터: {empty_count})")

        atpt_code = row["ATPT_OFCDC_SC_CODE"]
        school_code = str(row["SD_SCHUL_CODE"])
        school_name = row["SCHUL_NM"]

        subjects = fetch_school_subjects(atpt_code, school_code)

        if subjects:
            success_count += 1
            for subj in subjects:
                all_records.append({
                    "ATPT_OFCDC_SC_CODE": atpt_code,
                    "SD_SCHUL_CODE": school_code,
                    "SCHUL_NM": school_name,
                    "SUBJECT": subj,
                })
        else:
            empty_count += 1

        # API 부하 방지 (초당 약 3~4건)
        time.sleep(0.25)

    # 저장
    df = pd.DataFrame(all_records)
    output_path = "data/raw/neis_school_subjects.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # 학교별 과목 수 요약도 저장
    if len(df) > 0:
        summary = df.groupby(["SD_SCHUL_CODE", "SCHUL_NM"]).agg(
            subject_count=("SUBJECT", "count"),
            subjects=("SUBJECT", lambda x: "|".join(x))
        ).reset_index()
        summary.to_csv("data/raw/neis_school_subjects_summary.csv", index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print(f"수집 완료!")
    print(f"성공: {success_count}개 학교 / 빈 데이터: {empty_count}개")
    print(f"총 {len(df)}개 레코드 (학교-과목 쌍)")
    print(f"저장: {output_path}")
    if len(df) > 0:
        print(f"\n가장 많이 개설된 과목 Top 15:")
        print(df["SUBJECT"].value_counts().head(15).to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
