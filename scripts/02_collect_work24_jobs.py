"""
워크넷(work24) API - 직업정보 수집
API: 직업사전 목록 + 상세 (개요, 능력/지식)
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


def fetch_job_list() -> list[dict]:
    """전체 직업 목록 조회"""
    params = {
        "authKey": API_KEY,
        "returnType": "XML",
        "target": "JOBCD",
    }
    resp = requests.get(BASE_URL, params=params, timeout=15)
    root = ET.fromstring(resp.text)

    jobs = []
    for job_el in root.findall("jobList"):
        jobs.append({
            "jobCd": job_el.findtext("jobCd", ""),
            "jobNm": job_el.findtext("jobNm", ""),
            "jobClcd": job_el.findtext("jobClcd", ""),
            "jobClcdNM": job_el.findtext("jobClcdNM", ""),
        })
    return jobs


def fetch_job_summary(job_cd: str) -> dict:
    """직업 개요 조회 (dtlGb=1)"""
    params = {
        "authKey": API_KEY,
        "returnType": "XML",
        "target": "JOBDTL",
        "jobGb": "1",
        "dtlGb": "1",
        "jobCd": job_cd,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        root = ET.fromstring(resp.text)
        return {
            "jobLrclNm": root.findtext("jobLrclNm", ""),  # 대분류
            "jobMdclNm": root.findtext("jobMdclNm", ""),  # 중분류
            "jobSmclNm": root.findtext("jobSmclNm", ""),  # 소분류
            "jobSum": root.findtext("jobSum", ""),          # 직업 개요
            "way": root.findtext("way", ""),                # 되는 방법
        }
    except Exception as e:
        print(f"  개요 에러 ({job_cd}): {e}")
        return {}


def fetch_job_salary(job_cd: str) -> dict:
    """직업 임금/전망 조회 (dtlGb=4)"""
    params = {
        "authKey": API_KEY,
        "returnType": "XML",
        "target": "JOBDTL",
        "jobGb": "1",
        "dtlGb": "4",
        "jobCd": job_cd,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        root = ET.fromstring(resp.text)
        return {
            "sal": root.findtext("sal", ""),                # 임금 정보
            "jobSatis": root.findtext("jobSatis", ""),      # 직업 만족도
            "jobProspect": root.findtext("jobProspect", "")[:200] if root.findtext("jobProspect") else "",  # 전망 (앞 200자)
        }
    except Exception as e:
        print(f"  임금 에러 ({job_cd}): {e}")
        return {}


def main():
    print("=" * 50)
    print("워크넷 API - 직업정보 수집 시작")
    print("=" * 50)

    # 1. 직업 목록 가져오기
    print("직업 목록 조회 중...")
    jobs = fetch_job_list()
    print(f"총 {len(jobs)}개 직업 확인")

    # 2. 각 직업의 상세정보 수집
    all_data = []
    for i, job in enumerate(jobs):
        if i % 50 == 0:
            print(f"진행 중: {i}/{len(jobs)}...")

        # 개요
        summary = fetch_job_summary(job["jobCd"])
        # 임금/전망
        salary = fetch_job_salary(job["jobCd"])

        row = {**job, **summary, **salary}
        all_data.append(row)

        time.sleep(0.3)  # API 부하 방지

    # 3. DataFrame 저장
    df = pd.DataFrame(all_data)
    output_path = "data/raw/work24_jobs.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print(f"수집 완료!")
    print(f"총 {len(df)}개 직업 수집")
    print(f"저장 위치: {output_path}")
    print(f"컬럼: {list(df.columns)}")
    print(f"\n대분류별 분포:")
    if "jobLrclNm" in df.columns:
        print(df["jobLrclNm"].value_counts().head(10).to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
