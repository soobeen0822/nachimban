"""
나이스(NEIS) API - 전국 고등학교 기본정보 수집
API: 교육부_나이스 교육정보 개방 포털_초중등_학교기본정보
"""

import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEIS_API_KEY")
BASE_URL = "https://open.neis.go.kr/hub/schoolInfo"

# 시도교육청 코드 (17개)
ATPT_CODES = {
    "B10": "서울특별시교육청",
    "C10": "부산광역시교육청",
    "D10": "대구광역시교육청",
    "E10": "인천광역시교육청",
    "F10": "광주광역시교육청",
    "G10": "대전광역시교육청",
    "H10": "울산광역시교육청",
    "I10": "세종특별자치시교육청",
    "J10": "경기도교육청",
    "K10": "강원특별자치도교육청",
    "M10": "충청북도교육청",
    "N10": "충청남도교육청",
    "P10": "전북특별자치도교육청",
    "Q10": "전라남도교육청",
    "R10": "경상북도교육청",
    "S10": "경상남도교육청",
    "T10": "제주특별자치도교육청",
}


def fetch_schools(atpt_code: str, page: int = 1, size: int = 100) -> dict:
    """나이스 API로 고등학교 목록 조회"""
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": page,
        "pSize": size,
        "ATPT_OFCDC_SC_CODE": atpt_code,
        "SCHUL_KND_SC_NM": "고등학교",
    }
    resp = requests.get(BASE_URL, params=params, timeout=10)
    return resp.json()


def collect_all_schools():
    """전국 고등학교 전체 수집"""
    all_schools = []

    for code, name in ATPT_CODES.items():
        print(f"수집 중: {name} ({code})...")
        page = 1

        while True:
            try:
                data = fetch_schools(code, page=page, size=100)

                # 응답 구조 확인
                if "schoolInfo" not in data:
                    # 데이터 없음 또는 에러
                    if "RESULT" in data:
                        print(f"  → {data['RESULT']['MESSAGE']}")
                    break

                rows = data["schoolInfo"][1]["row"]
                all_schools.extend(rows)
                print(f"  → 페이지 {page}: {len(rows)}건 수집")

                # 총 건수 확인
                total = data["schoolInfo"][0]["head"][0]["list_total_count"]
                if page * 100 >= total:
                    break

                page += 1
                time.sleep(0.3)  # API 부하 방지

            except Exception as e:
                print(f"  → 에러: {e}")
                break

        time.sleep(0.5)

    return all_schools


def main():
    print("=" * 50)
    print("나이스 API - 전국 고등학교 기본정보 수집 시작")
    print("=" * 50)

    schools = collect_all_schools()

    if not schools:
        print("수집된 데이터가 없습니다. API 키를 확인하세요.")
        return

    # DataFrame 변환
    df = pd.DataFrame(schools)

    # 필요한 컬럼만 선택
    columns_to_keep = [
        "ATPT_OFCDC_SC_CODE",  # 시도교육청코드
        "ATPT_OFCDC_SC_NM",    # 시도교육청명
        "SD_SCHUL_CODE",       # 학교코드
        "SCHUL_NM",            # 학교명
        "ENG_SCHUL_NM",        # 영문학교명
        "SCHUL_KND_SC_NM",     # 학교종류명
        "HS_SC_NM",            # 고등학교구분명 (일반고, 특목고, 특성화고 등)
        "HS_GNRL_BUSNS_SC_NM", # 고등학교 일반/전문 구분
        "SPCLY_PURPS_HS_ORD_NM",  # 특수목적고 계열명
        "ENE_BFE_SEHF_SC_NM",  # 전후기 구분
        "LCTN_SC_NM",          # 소재지
        "ORG_RDNMA",           # 도로명주소
        "ORG_TELNO",           # 전화번호
        "HMPG_ADRES",          # 홈페이지주소
        "FOND_SC_NM",          # 설립구분 (공립/사립)
        "COEDU_SC_NM",         # 남녀공학구분
        "FOND_YMD",            # 설립일
    ]

    # 존재하는 컬럼만 필터
    available_cols = [c for c in columns_to_keep if c in df.columns]
    df = df[available_cols]

    # 저장
    output_path = "data/raw/neis_high_schools.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 50}")
    print(f"수집 완료!")
    print(f"총 {len(df)}개 고등학교 수집")
    print(f"저장 위치: {output_path}")
    print(f"컬럼: {list(df.columns)}")
    print(f"\n학교 유형별 분포:")
    if "HS_SC_NM" in df.columns:
        print(df["HS_SC_NM"].value_counts().to_string())
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
