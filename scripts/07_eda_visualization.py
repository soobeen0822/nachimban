"""
나침반 (NACHIMBAN) - 공공데이터 EDA 시각화
대회 보고서용 인사이트 차트 생성
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("docs/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 데이터 로드
schools_df = pd.read_csv(DATA_DIR / "neis_high_schools.csv")
subjects_df = pd.read_csv(DATA_DIR / "neis_school_subjects.csv")
jobs_df = pd.read_csv(DATA_DIR / "work24_jobs.csv")
holland_df = pd.read_csv(DATA_DIR / "holland_job_mapping.csv")
mbti_df = pd.read_csv(DATA_DIR / "mbti_job_profile.csv")

print("=" * 50)
print("EDA 시각화 생성 시작")
print("=" * 50)


# ============================
# 차트 1: 전국 고등학교 유형별 분포
# ============================
def chart1_school_types():
    fig, ax = plt.subplots(figsize=(8, 5))
    type_counts = schools_df['HS_SC_NM'].value_counts()
    colors = ['#3b82f6', '#f59e0b', '#8b5cf6', '#10b981']
    bars = ax.bar(type_counts.index, type_counts.values, color=colors)
    
    for bar, val in zip(bars, type_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f'{val}개', ha='center', fontsize=11, fontweight='bold')
    
    ax.set_title('전국 고등학교 유형별 분포', fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel('학교 수')
    ax.set_xlabel('')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_school_types.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 1: 고등학교 유형별 분포")


# ============================
# 차트 2: 지역별 고등학교 수
# ============================
def chart2_schools_by_region():
    fig, ax = plt.subplots(figsize=(10, 6))
    region_counts = schools_df['ATPT_OFCDC_SC_NM'].value_counts().sort_values(ascending=True)
    region_short = region_counts.index.str.replace('교육청', '').str.replace('특별시', '').str.replace('광역시', '').str.replace('특별자치시', '').str.replace('특별자치도', '').str.replace('도', '')
    
    bars = ax.barh(range(len(region_counts)), region_counts.values, color='#3b82f6', alpha=0.8)
    ax.set_yticks(range(len(region_counts)))
    ax.set_yticklabels(region_short, fontsize=9)
    
    for bar, val in zip(bars, region_counts.values):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                f'{val}', va='center', fontsize=9)
    
    ax.set_title('시도별 고등학교 수', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('학교 수')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_schools_by_region.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 2: 지역별 고등학교 수")


# ============================
# 차트 3: 직업 대분류별 분포 + 평균 임금
# ============================
def chart3_jobs_by_category():
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_counts = jobs_df['jobLrclNm'].value_counts().sort_values(ascending=True)
    
    colors = plt.cm.Set3(range(len(cat_counts)))
    bars = ax.barh(range(len(cat_counts)), cat_counts.values, color=colors)
    ax.set_yticks(range(len(cat_counts)))
    ax.set_yticklabels(cat_counts.index, fontsize=9)
    
    for bar, val in zip(bars, cat_counts.values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val}개', va='center', fontsize=9)
    
    ax.set_title('직업 대분류별 직업 수 (워크넷 462개 직업)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('직업 수')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_jobs_by_category.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 3: 직업 대분류별 분포")


# ============================
# 차트 4: Holland 유형별 직업 분포
# ============================
def chart4_holland_distribution():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 각 직업의 1순위 Holland 코드 추출
    top1_codes = holland_df['holland_top3'].str[0]
    code_counts = top1_codes.value_counts()
    
    holland_labels = {'R': '현실형(R)', 'I': '탐구형(I)', 'A': '예술형(A)',
                      'S': '사회형(S)', 'E': '진취형(E)', 'C': '관습형(C)'}
    holland_colors = {'R': '#ef4444', 'I': '#3b82f6', 'A': '#a855f7',
                      'S': '#10b981', 'E': '#f59e0b', 'C': '#6b7280'}
    
    labels = [holland_labels.get(c, c) for c in code_counts.index]
    colors = [holland_colors.get(c, '#999') for c in code_counts.index]
    
    wedges, texts, autotexts = ax.pie(
        code_counts.values, labels=labels, colors=colors,
        autopct='%1.0f%%', startangle=90, textprops={'fontsize': 10}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    ax.set_title('Holland 1순위 유형별 직업 분포', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_holland_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 4: Holland 유형별 분포")


# ============================
# 차트 5: 직업 대분류별 MBTI 스펙트럼 평균
# ============================
def chart5_mbti_by_category():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('직업 대분류별 MBTI 스펙트럼 평균 (워크넷 공공데이터 기반)', 
                 fontsize=13, fontweight='bold', y=0.98)
    
    merged = mbti_df.merge(jobs_df[['jobCd', 'jobLrclNm']], on='jobCd', how='left', suffixes=('', '_y'))
    avg = merged.groupby('jobLrclNm')[['mbti_EI', 'mbti_SN', 'mbti_TF', 'mbti_JP']].mean()
    
    axis_info = [
        ('mbti_EI', 'E (외향)', 'I (내향)', 'E-I축 (에너지 방향)'),
        ('mbti_SN', 'S (감각)', 'N (직관)', 'S-N축 (인식 기능)'),
        ('mbti_TF', 'T (사고)', 'F (감정)', 'T-F축 (판단 기능)'),
        ('mbti_JP', 'J (판단)', 'P (인식)', 'J-P축 (생활 양식)'),
    ]
    
    for idx, (col, left, right, title) in enumerate(axis_info):
        ax = axes[idx//2][idx%2]
        sorted_avg = avg[col].sort_values()
        colors = ['#3b82f6' if v >= 50 else '#ef4444' for v in sorted_avg.values]
        
        ax.barh(range(len(sorted_avg)), sorted_avg.values - 50, left=50, color=colors, alpha=0.7)
        ax.set_yticks(range(len(sorted_avg)))
        short_labels = [s[:8] for s in sorted_avg.index]
        ax.set_yticklabels(short_labels, fontsize=7)
        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlim(35, 65)
        ax.set_xlabel(f'← {left}  |  {right} →', fontsize=9)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_mbti_by_category.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 5: 대분류별 MBTI 스펙트럼")


# ============================
# 차트 6: 학교별 개설 과목 수 분포
# ============================
def chart6_subject_count():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    subject_counts = subjects_df.groupby('SD_SCHUL_CODE')['SUBJECT'].nunique()
    
    ax.hist(subject_counts.values, bins=30, color='#3b82f6', alpha=0.8, edgecolor='white')
    ax.axvline(subject_counts.mean(), color='#ef4444', linestyle='--', linewidth=2,
               label=f'평균: {subject_counts.mean():.0f}개')
    
    ax.set_title('고등학교별 개설 과목 수 분포', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('개설 과목 수')
    ax.set_ylabel('학교 수')
    ax.legend(fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_subject_count_dist.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 6: 학교별 개설 과목 수 분포")


# ============================
# 차트 7: 가장 많이 개설된 과목 Top 20
# ============================
def chart7_popular_subjects():
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 과목 이름 정리 (뒤에 A, B, 1 등 제거하여 그룹핑)
    top_subjects = subjects_df['SUBJECT'].value_counts().head(20).sort_values(ascending=True)
    
    ax.barh(range(len(top_subjects)), top_subjects.values, color='#10b981', alpha=0.8)
    ax.set_yticks(range(len(top_subjects)))
    ax.set_yticklabels(top_subjects.index, fontsize=9)
    
    for i, val in enumerate(top_subjects.values):
        ax.text(val + 10, i, f'{val}교', va='center', fontsize=8)
    
    ax.set_title('전국 고등학교에서 가장 많이 개설된 과목 Top 20', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('개설 학교 수')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_popular_subjects.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 차트 7: 인기 개설 과목 Top 20")


# 실행
if __name__ == "__main__":
    chart1_school_types()
    chart2_schools_by_region()
    chart3_jobs_by_category()
    chart4_holland_distribution()
    chart5_mbti_by_category()
    chart6_subject_count()
    chart7_popular_subjects()
    
    print(f"\n{'=' * 50}")
    print(f"전체 차트 생성 완료!")
    print(f"저장 위치: {OUTPUT_DIR}/")
    print(f"{'=' * 50}")
