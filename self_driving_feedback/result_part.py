import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


import matplotlib.pyplot as plt

# plt.rcParams["font.family"] = "AppleGothic"  # macOS font that supports Hangul
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows에서 한글을 지원하는 폰트
plt.rcParams["axes.unicode_minus"] = False  # Ensure minus sign is displayed correctly


# 레이더 차트를 그리는 헬퍼 함수 (Matplotlib)
def radar_chart(
    values,
    categories,
    title="레이더 차트",
    color="blue",
    alpha=0.3,
    max_radius=None,  # 레이더 외곽 최대값
    figsize=(4, 4),  # 전체 그림 크기 (인치)
    label_fontsize=8,  # 축 라벨(지표명) 폰트 크기
    title_fontsize=10,  # 차트 제목 폰트 크기
):
    """
    values: 지표별 값 (길이 N의 리스트 or array)
    categories: 지표 라벨 (길이 N의 리스트)
    title: 차트 제목
    color: 레이더 내부 채우기 색상
    alpha: 채우기 투명도
    max_radius: 레이더 반경 최대값 (None이면 데이터 최댓값에 맞춤)
    figsize: (가로, 세로) 형식의 튜플로 전체 그림 크기(인치) 조절
    label_fontsize: 축 라벨(지표명) 폰트 크기
    title_fontsize: 차트 제목 폰트 크기
    """

    # 카테고리 개수
    N = len(categories)

    # 0~2π 범위 각도 생성
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # values도 맨 앞값을 다시 끝에 붙여 닫힌 도형 만듦
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    # 그림/축 생성 (극좌표, polar)
    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": "polar"})

    # 데이터 플롯
    ax.plot(angles, values, color=color, linewidth=2)
    ax.fill(angles, values, color=color, alpha=alpha)

    # 레이더 축 설정
    ax.set_theta_offset(np.pi / 2)  # 시작 각도를 위(90도)로 맞춤
    ax.set_theta_direction(-1)  # 시계 방향으로 각도 증가
    ax.set_xticks(angles[:-1])  # 마지막 각도는 중복이므로 제외
    # 축 라벨 폰트 크기 적용
    ax.set_xticklabels(categories, fontsize=label_fontsize)

    # y축 최대값 설정
    if max_radius is not None:
        ax.set_ylim(0, max_radius)

    # 세부 폰트 크기
    ax.tick_params(axis="y", labelsize=label_fontsize)  # r축(거리축) 폰트 크기

    # 차트 제목 설정 (폰트 크기와 위치)
    # ax.set_title(title, y=1.08, fontsize=title_fontsize)
    #
    return fig, ax


def show_result():

    st.markdown(
        """
            <style> 
            .st-emotion-cache-1104ytp li {
                color: #e67e22; 
                }
                
            .st-emotion-cache-1104ytp strong{
                color: #34495e;   
               }
            
            </style> 
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h2 style='text-align: center;'>자율 주행 시스템 만족도 분석 결과 </h2>",
        unsafe_allow_html=True,
    )

    # (1) 조사 개요
    st.subheader("설문 조사 개요")
    st.divider()
    st.write("- **설문 조사 기간**: 2025.03.14 ~ 2025.03.26 **(12일간)**")
    st.write("- **전체 응답자 수**: 120명")

    st.divider()
    st.subheader("응답자 특성 분석")
    st.divider()

    # 임의 데이터 생성
    np.random.seed(42)
    # 나이 (20~60 사이 정규분포)
    ages = np.random.normal(loc=38, scale=8, size=120).astype(int)
    ages = np.clip(ages, 20, 60)

    # 지역 분포
    regions = np.random.choice(
        ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"],
        size=120,
        p=[0.25, 0.25, 0.1, 0.15, 0.2, 0.05],
    )

    # 성별 분포
    genders = np.random.choice(["남성", "여성"], size=120, p=[0.53, 0.47])

    # 만족도 (1~5)
    scores = np.random.randint(1, 6, size=120)

    # ─────────────────────────────────
    # 1행: 나이 분포 / 지역 분포
    # ─────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.write("**나이별 응답자 분포 (평균 , 표준편차)**")
        df_age = pd.DataFrame(ages, columns=["나이"])
        # 나이를 그룹화(예: 20~60 각각 카운트)
        age_counts = df_age["나이"].value_counts().sort_index()
        # st.bar_chart는 index=X축, value=Y축으로 쓰기 위해 시리즈->데이터프레임 변환
        st.bar_chart(age_counts)

        df_gender = pd.DataFrame(genders, columns=["성별"])
        gender_counts = df_gender["성별"].value_counts().reset_index()
        gender_counts.columns = ["성별", "Count"]

        # Altair 파이차트
        pie_chart = (
            alt.Chart(gender_counts)
            .mark_arc(outerRadius=140)
            .encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="성별", type="nominal"),
                tooltip=["성별", "Count"],
            )
            .properties(width=400, height=400, title="성별 분포 (%)")
        )

        text_chart = (
            alt.Chart(gender_counts)
            .mark_text(radius=160, size=12, fontWeight="bold", color="white")
            .encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                text=alt.Text(field="Count", type="quantitative", format=",.0f"),
            )
        )

        # 두 차트 합치기
        final_chart = pie_chart + text_chart

        # 차트 표시
        st.altair_chart(final_chart, use_container_width=True)

    with col2:
        st.write("**지역별 응답자 분포 (%)**")
        df_region = pd.DataFrame(regions, columns=["지역"])
        region_counts = df_region["지역"].value_counts()
        region_counts = region_counts.sort_values(ascending=True)  # 수평축 정렬(선택)
        st.bar_chart(region_counts)

    st.divider()
    st.subheader("만족도 분석 강화")
    st.divider()

    # 레이아웃: 2행 구성
    # ───────── 1행: (주행 승차감 분석, 긴급 상황 대응 분석) ─────────
    row1_col1, row1_col2 = st.columns(2)

    # [1-1] 주행 승차감 분석 (레이더 차트)
    with row1_col1:
        categories = ["Comfort", "Stability", "Noise", "Vibration", "Acceleration"]
        values = np.random.randint(1, 11, size=len(categories))

        fig1, ax1 = radar_chart(
            values=values,
            categories=categories,
            title="주행 승차감",
            color="blue",
            alpha=0.3,
            max_radius=11,  # 0~10 범위로 고정
            figsize=(2, 2),  # 그림 크기(가로4, 세로4 인치)
            label_fontsize=4,  # 축 라벨 폰트 사이즈
            title_fontsize=9,  # 제목 폰트 사이즈
        )
        st.write("**주행 승차감 분석**")
        st.pyplot(fig1)

    # [1-2] 긴급 상황 대응 분석 (막대 차트: st.bar_chart 사용)
    with row1_col2:
        st.write("**긴급 상황 대응 분석**")
        # 예: 요일(day) & 주말여부(weekend)에 따른 점수 생성
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        np.random.seed(42)
        data_list = []
        for day in days:
            for weekend in [False, True]:
                score = np.random.randint(5, 31)  # 5~30 사이
                data_list.append((day, weekend, score))

        df_emergency = pd.DataFrame(data_list, columns=["day", "weekend", "score"])

        # "긴급상황 대응 점수"를 st.bar_chart로 표시하기 위해 pivot
        # 예: index=day, columns=weekend(참/거짓), values=score
        pivot_df = df_emergency.pivot(index="day", columns="weekend", values="score")
        # weekend = False/True -> "False/True" 컬럼명으로 변환됨
        pivot_df = pivot_df.reindex(index=days)  # 요일 순서 정렬

        st.bar_chart(pivot_df)

    # ───────── 2행: (주차 기능 분석, 전반 만족도 추천) ─────────
    row2_col1, row2_col2 = st.columns(2)

    # [2-1] 주차 기능 분석 (막대 차트: st.bar_chart)
    with row2_col1:
        st.write("**주차 기능 분석**")
        # 예: 동일 df에서 '주차 기능 점수' 가정하여 랜덤 생성
        days2 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        park_scores = np.random.randint(0, 21, size=len(days2))  # 0~20 사이
        df_park = pd.DataFrame({"day": days2, "park_score": park_scores}).set_index(
            "day"
        )
        st.bar_chart(df_park)

    # [2-2] 전반 만족도 추천 (레이더 차트)
    with row2_col2:
        categories2 = ["내구성", "힘", "속도", "지능", "에너지"]
        values2 = np.random.randint(1, 11, size=len(categories2))

        fig2, ax2 = radar_chart(
            values=values2,
            categories=categories2,
            title="전반 만족도",
            color="green",
            alpha=0.3,
            max_radius=11,
            figsize=(2, 2),
            label_fontsize=4,
            title_fontsize=9,
        )
        st.write("**전반 만족도 추천**")
        st.pyplot(fig2)

    # (4) 보고서 코멘트
    comment = st.text_area("AI 분석 코멘트 ")
