"""
나침반 (NACHIMBAN) - 대회 제출용 PPT 생성
규격: A4, 최대 15매, 12pt 이상, 식별정보 미기재
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

OUTPUT_PATH = Path("docs/나침반_NACHIMBAN_제출자료.pptx")
CHART_DIR = Path("docs/charts")

# A4 크기 (가로)
SLIDE_WIDTH = Cm(29.7)
SLIDE_HEIGHT = Cm(21.0)

# 색상
BLUE = RGBColor(0x25, 0x63, 0xEB)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
GREEN = RGBColor(0x10, 0xB9, 0x81)


def add_title_slide(prs):
    """슬라이드 1: 표지"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 빈 레이아웃
    
    # 배경
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xEF, 0xF6, 0xFF)
    
    # 서비스명
    txBox = slide.shapes.add_textbox(Cm(3), Cm(5), Cm(24), Cm(3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "🧭 나침반 (NACHIMBAN)"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = DARK
    p.alignment = PP_ALIGN.CENTER
    
    # 부제
    p2 = tf.add_paragraph()
    p2.text = "AI 기반 교육 공공데이터 활용 고등학교 진로 매칭 서비스"
    p2.font.size = Pt(16)
    p2.font.color.rgb = GRAY
    p2.alignment = PP_ALIGN.CENTER
    
    # 약어 설명
    p3 = tf.add_paragraph()
    p3.text = ""
    p4 = tf.add_paragraph()
    p4.text = "Navigating Academic Careers through Holistic Intelligence\nwith Mined puBlic data And Networks"
    p4.font.size = Pt(12)
    p4.font.color.rgb = GRAY
    p4.alignment = PP_ALIGN.CENTER
    
    # 하단 정보
    txBox2 = slide.shapes.add_textbox(Cm(3), Cm(16), Cm(24), Cm(3))
    tf2 = txBox2.text_frame
    p5 = tf2.paragraphs[0]
    p5.text = "교육공공데이터 AI 활용 대회 | AI 활용 아이디어 기획 분야"
    p5.font.size = Pt(12)
    p5.font.color.rgb = GRAY
    p5.alignment = PP_ALIGN.CENTER
    
    p6 = tf2.add_paragraph()
    p6.text = "서비스 URL: https://nachimban-nine.vercel.app"
    p6.font.size = Pt(12)
    p6.font.color.rgb = BLUE
    p6.alignment = PP_ALIGN.CENTER


def add_data_slide(prs):
    """슬라이드 2: 활용 데이터 정보 (첫 번째 페이지 필수)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 제목
    txBox = slide.shapes.add_textbox(Cm(2), Cm(1), Cm(26), Cm(2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "활용 교육 공공데이터"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK
    
    # 데이터 테이블 내용
    content = """
■ 데이터 1: 전국 고등학교 기본정보 (2,407개 학교)
  • 출처: 나이스(NEIS) 교육정보 개방 포털 (https://open.neis.go.kr)
  • API: schoolInfo | 라이선스: 공공누리 제1유형
  • 내용: 학교명, 유형(일반고/특목고/특성화고), 주소, 홈페이지, 설립구분, 남녀공학구분

■ 데이터 2: 고등학교별 개설 교과목 (2,307개 학교, 161,317건)
  • 출처: 나이스(NEIS) 교육정보 개방 포털 (https://open.neis.go.kr)
  • API: hisTimetable | 라이선스: 공공누리 제1유형
  • 내용: 학교별 실제 개설 교과목명 (2025년 4월 기준)

■ 데이터 3: 직업 상세정보 및 능력/지식 점수 (462개 직업)
  • 출처: 워크넷 work24 OpenAPI (https://www.work24.go.kr)
  • API: callOpenApiSvcInfo212L01 | 라이선스: 공공누리 제1유형
  • 내용: 직업명, 직업개요, 임금, 전망, 필요 능력 35개 항목 점수, 필요 지식 30개 항목 점수
"""
    txBox2 = slide.shapes.add_textbox(Cm(2), Cm(3.5), Cm(26), Cm(15))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for line in content.strip().split('\n'):
        p = tf2.add_paragraph()
        p.text = line.strip()
        if line.startswith('■'):
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = BLUE
        else:
            p.font.size = Pt(12)
            p.font.color.rgb = DARK


def add_text_slide(prs, title, bullets, subtitle=None):
    """텍스트 슬라이드 생성 헬퍼"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 제목
    txBox = slide.shapes.add_textbox(Cm(2), Cm(1), Cm(26), Cm(2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK
    
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = GRAY
    
    # 본문
    txBox2 = slide.shapes.add_textbox(Cm(2), Cm(4), Cm(26), Cm(15))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for bullet in bullets:
        p = tf2.add_paragraph()
        p.text = bullet
        if bullet.startswith('▶') or bullet.startswith('■'):
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = BLUE
        elif bullet.startswith('  '):
            p.font.size = Pt(12)
            p.font.color.rgb = DARK
        else:
            p.font.size = Pt(13)
            p.font.color.rgb = DARK
        p.space_after = Pt(4)
    
    return slide


def add_image_slide(prs, title, image_path, caption=None):
    """이미지 슬라이드 생성 헬퍼"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 제목
    txBox = slide.shapes.add_textbox(Cm(2), Cm(0.5), Cm(26), Cm(2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = DARK
    
    # 이미지
    if Path(image_path).exists():
        slide.shapes.add_picture(str(image_path), Cm(3), Cm(3), Cm(24), Cm(14))
    
    # 캡션
    if caption:
        txBox2 = slide.shapes.add_textbox(Cm(2), Cm(18), Cm(26), Cm(2))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = caption
        p2.font.size = Pt(12)
        p2.font.color.rgb = GRAY
        p2.alignment = PP_ALIGN.CENTER
    
    return slide


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    
    # ===== 슬라이드 1: 표지 =====
    add_title_slide(prs)
    
    # ===== 슬라이드 2: 활용 데이터 (필수) =====
    add_data_slide(prs)
    
    # ===== 슬라이드 3: 문제 정의 =====
    add_text_slide(prs, "1. 문제 정의", [
        "▶ 현재 진로 교육의 문제점",
        "",
        "• 전국 2,407개 고등학교 정보가 여러 기관에 산재 → 통합 비교 불가",
        "• 기존 MBTI: 16유형 분류로 경계값 학생 개인차 미반영",
        "• 진로 선택이 데이터가 아닌 주변 평판에 의존",
        "• 진로상담 인프라 부족 지역의 교육 격차",
        "",
        "▶ 해결 목표",
        "",
        "• 교육 공공데이터를 AI로 통합 분석",
        "• 누구나 무료로 이용 가능한 맞춤형 진로 매칭 서비스 구현",
        "• MBTI 연속 스펙트럼(256가지+)으로 정밀한 개인차 반영",
    ])
    
    # ===== 슬라이드 4: 서비스 개요 =====
    add_text_slide(prs, "2. 서비스 개요", [
        "▶ 핵심 아이디어: Holland 검사 + MBTI 연속 스펙트럼 + 공공데이터 AI 매칭",
        "",
        "■ MBTI 연속 스펙트럼",
        "  • 기존 16유형 → 4축 × 0~100 연속값 (256가지+ 조합)",
        "  • 각 축: 강한E / 약한E / 약한I / 강한I (4단계)",
        "  • 직업에도 MBTI 4축 연속값을 부여 → 유클리드 거리로 정밀 매칭",
        "",
        "■ 이중 매칭 구조",
        "  • Holland(RIASEC) → 직업군 1차 필터 (코사인 유사도, 가중치 60%)",
        "  • MBTI 스펙트럼 → 직업군 내 세부 매칭 (유클리드 거리, 가중치 40%)",
        "  • 공공데이터 → 실제 학과/학교 연결",
    ])
    
    # ===== 슬라이드 5: AI 활용 과정 =====
    add_text_slide(prs, "3. AI 활용 과정", [
        "▶ 데이터 전처리",
        "  • 나이스 API → 전국 고등학교 기본정보 + 개설 교과목 수집",
        "  • 워크넷 API → 462개 직업별 능력(35개) / 지식(30개) 점수 수집",
        "",
        "▶ AI 모델링",
        "  • 워크넷 능력 점수 → Holland RIASEC 6축 점수 산출 (키워드 매핑)",
        "  • 워크넷 능력 점수 → MBTI 4축 연속값 산출 (양방향 비율 계산)",
        "  • 산출 공식: 축 값 = 두번째방향평균 / (첫번째 + 두번째) × 100",
        "",
        "▶ 추론/매칭 절차",
        "  • Step 1: 학생 Holland + MBTI → 직업 유사도 계산 → Top 5 추천",
        "  • Step 2: 추천 직업 → 관련 학과 → 필수 교과목 추출",
        "  • Step 3: 교과목 개설 학교 필터 + 성별/거주지 기반 매칭",
        "  • Step 4: 교육과정 로드맵 생성 (고1→고2→고3)",
    ])
    
    # ===== 슬라이드 6: 사용자 플로우 =====
    add_text_slide(prs, "4. 서비스 사용자 플로우", [
        "▶ 입력 단계",
        "  [Step 1] 목표 입력 (선택) - 희망 학교/대학/학과/직업 (자동완성, 건너뛰기 가능)",
        "  [Step 2] Holland 흥미 검사 - 18문항, 5점 척도 → RIASEC 6축 점수",
        "  [Step 3] MBTI 스펙트럼 검사 - 32문항, 7점 척도 → 4축 연속값(0~100)",
        "  [Step 4] 추가 정보 - 성별, 거주지(시도/시군구/동), 학년",
        "",
        "▶ 결과 대시보드",
        "  • 종합 의견 (핵심 요약)",
        "  • 프로필 시각화 (Holland 레이더 차트 + MBTI 스펙트럼 바)",
        "  • 목표 매칭도 비교 (입력한 경우, 0~100% 판정)",
        "  • AI 추천 진로 Top 5 (직업 설명 + 적합도 + 추천 이유 + 관련 학과)",
        "  • 추천 고등학교 3~10개 (유형별 정보 차등, 더보기 지원)",
        "  • 교육과정 로드맵 (고1~고3 학년별 교과 + 비교과)",
    ])
    
    # ===== 슬라이드 7: 데이터 분석 1 - 학교 =====
    add_image_slide(prs, "5-1. 데이터 분석: 전국 고등학교 유형별 분포",
                    CHART_DIR / "01_school_types.png",
                    "전국 2,407개 고등학교 | 일반고 68.3%, 특성화고 20.4%, 특목고 6.6%, 자율고 4.7%")
    
    # ===== 슬라이드 8: 데이터 분석 2 - 지역 =====
    add_image_slide(prs, "5-2. 데이터 분석: 시도별 고등학교 수",
                    CHART_DIR / "02_schools_by_region.png",
                    "경기도(505개) > 서울(319개) > 경남(195개) 순 | 지역별 교육 인프라 격차 확인")
    
    # ===== 슬라이드 9: 데이터 분석 3 - Holland =====
    add_image_slide(prs, "5-3. 데이터 분석: Holland 유형별 직업 분포",
                    CHART_DIR / "04_holland_distribution.png",
                    "현실형(R) 37%로 가장 많음 | 워크넷 462개 직업 능력 데이터 기반 산출")
    
    # ===== 슬라이드 10: 데이터 분석 4 - MBTI =====
    add_image_slide(prs, "5-4. 데이터 분석: 직업 대분류별 MBTI 스펙트럼",
                    CHART_DIR / "05_mbti_by_category.png",
                    "연구직: I+T 성향 | 교육직: E+F 성향 | 예술직: N+P 성향 | 공공데이터 기반 패턴 확인")
    
    # ===== 슬라이드 11: 데이터 분석 5 - 교과목 =====
    add_image_slide(prs, "5-5. 데이터 분석: 가장 많이 개설된 과목 Top 20",
                    CHART_DIR / "07_popular_subjects.png",
                    "한국사·영어Ⅰ·수학Ⅰ이 대부분 학교에 개설 | 물리학Ⅱ·공학일반 등은 소수 학교만 개설")
    
    # ===== 슬라이드 12: 기대효과 =====
    add_text_slide(prs, "6. 기대효과 및 사회적 가치", [
        "▶ 기대효과",
        "  • 학생: 데이터 기반 객관적 진로 탐색, 적합 학교 발견",
        "  • 학부모: 자녀 특성에 맞는 교육 선택 근거 제공",
        "  • 교사: 진로지도 보조 자료, 학생별 맞춤 상담 근거",
        "  • 정책: 지역별 교육 인프라 격차 데이터 기반 파악",
        "",
        "▶ 사회적 가치",
        "  • 교육 형평성: 농어촌·소외 지역에도 동일 품질의 AI 추천",
        "  • 정보 접근성: 산재된 공공데이터를 하나의 서비스로 통합",
        "  • 개인 맞춤화: 256가지+ MBTI 조합으로 획일적 진로지도 탈피",
        "  • 공공데이터 활용: 세금으로 구축된 데이터의 실질적 활용 모범 사례",
        "  • 의사결정 지원: 감이 아닌 데이터 기반 진로 선택 문화 조성",
    ])
    
    # ===== 슬라이드 13: 기술 아키텍처 =====
    add_text_slide(prs, "7. 기술 아키텍처", [
        "▶ 시스템 구성",
        "  • Frontend: React + TypeScript + Tailwind CSS + Recharts (Vercel 배포)",
        "  • Backend: Python FastAPI + AI 매칭 엔진 (Render 배포)",
        "  • 데이터: 나이스 + 워크넷 공공데이터 (CSV, REST API)",
        "",
        "▶ AI 매칭 엔진",
        "  • Holland 매칭: 코사인 유사도 (학생 6축 벡터 ↔ 직업 6축 벡터)",
        "  • MBTI 매칭: 유클리드 거리 (학생 4축 ↔ 직업 4축, 0~100 연속값)",
        "  • 학교 매칭: 교과목 커버리지 + 학교유형 보너스 + 근접도 보너스",
        "",
        "▶ 매칭 가중치",
        "  • 진로 추천 = Holland(60%) + MBTI(40%)",
        "  • 학교 추천 = 교과목 커버리지 + 유형(+5) + 동일 동(+8) / 동일 구(+3)",
    ])
    
    # ===== 슬라이드 14: 향후 계획 =====
    add_text_slide(prs, "8. 향후 발전 방향", [
        "▶ 데이터 확장",
        "  • 커리어넷 API 연동 (승인 대기 중) → 학과-직업 매핑 정확도 향상",
        "  • 졸업생 진로 현황 데이터 반영 → 학교 추천 근거 강화",
        "  • 대학 입시 전형 데이터 연계",
        "",
        "▶ 기능 고도화",
        "  • 사용자 피드백 학습 → 추천 모델 지속 개선",
        "  • 모바일 앱 개발 → 접근성 확대",
        "  • 학부모/교사용 대시보드 → 교육 현장 활용도 제고",
        "",
        "▶ 서비스 확장",
        "  • 중학생 → 고등학교 선택 (현재)",
        "  • 고등학생 → 대학/학과 선택 (확장 예정)",
        "  • 대학생 → 취업/진로 매칭 (장기 목표)",
    ])
    
    # ===== 슬라이드 15: 생성형 AI 활용 정보 =====
    add_text_slide(prs, "부록: 생성형 AI 활용 정보", [
        "▶ 활용 도구",
        "  • Claude (Anthropic) - Kiro IDE 환경에서 활용",
        "",
        "▶ 활용 내용",
        "  • 프로젝트 기획 및 구조 설계 지원",
        "  • 공공데이터 API 수집 스크립트 작성",
        "  • Holland/MBTI 매핑 알고리즘 설계 및 구현",
        "  • Frontend/Backend 코드 작성",
        "  • EDA 시각화 스크립트 작성",
        "  • 보고서 및 발표자료 초안 작성",
        "",
        "▶ 추가 산출물",
        "  • 전체 소스코드: https://github.com/soobeen0822/nachimban",
        "  • 라이브 서비스: https://nachimban-nine.vercel.app",
    ], subtitle="(대회 규정에 따라 생성형 AI 활용 사항을 기재합니다)")
    
    # 저장
    prs.save(str(OUTPUT_PATH))
    print(f"PPT 생성 완료: {OUTPUT_PATH}")
    print(f"총 {len(prs.slides)}페이지 (표지 포함)")


if __name__ == "__main__":
    main()
