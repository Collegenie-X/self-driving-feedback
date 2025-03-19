import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import re

# 한글 폰트 설정 (macOS: AppleGothic, Windows: Malgun Gothic)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


# 헬퍼 함수: 레이더 차트 (Matplotlib)
def radar_chart(
    values,
    categories,
    title="레이더 차트",
    color="blue",
    alpha=0.3,
    max_radius=None,
    figsize=(4, 4),
    label_fontsize=8,
    title_fontsize=10,
):
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": "polar"})
    ax.plot(angles, values, color=color, linewidth=2)
    ax.fill(angles, values, color=color, alpha=alpha)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=label_fontsize)
    if max_radius is not None:
        ax.set_ylim(0, max_radius)
    ax.tick_params(axis="y", labelsize=label_fontsize)
    ax.set_title(title, y=1.08, fontsize=title_fontsize)
    return fig, ax


# 헬퍼 함수: 설문 결과를 읽고 데이터 처리 후 차트 표시
def show_result():
    st.markdown(
        """
        <style> 
        .st-emotion-cache-1104ytp li { color: #e67e22; }
        .st-emotion-cache-1104ytp strong { color: #34495e; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center;'>자율 주행 시스템 만족도 분석 결과</h2>",
        unsafe_allow_html=True,
    )

    # (1) 조사 개요
    st.subheader("설문 조사 개요")
    st.divider()
    st.write("- **설문 조사 기간**: 2025.03.14 ~ 2025.03.26 **(12일간)**")
    # 실제 응답자 수: CSV 파일의 행 개수
    data = pd.read_csv("./data/survey_results.csv")
    st.write(f"- **전체 응답자 수**: {len(data)}명")

    st.divider()
    st.subheader("응답자 특성 분석")
    st.divider()

    # --- 응답자 특성: 나이, 성별, 지역 ---
    # 나이 분포
    col1, col2 = st.columns(2)
    with col1:
        st.write("**나이별 응답자 분포 (평균, 표준편차)**")
        # df_age = data[["age"]]
        # age_counts = df_age["age"].value_counts().sort_index()
        #  st.bar_chart(age_counts)

        bins = [0, 19, 29, 39, 49, 59, 100]  # 나이 구간 (0~19, 20~29, 30~39, ...)
        labels = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]  # 나이대 레이블
        data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels, right=False)

        # 나이대별 응답자 수 계산
        age_group_counts = data["age_group"].value_counts().sort_index()

        # 나이대별 응답자 분포 시각화 (히스토그램)
        st.write("**나이대별 응답자 분포**")
        st.bar_chart(age_group_counts)

    # 성별 분포: csv의 gender 컬럼은 boolean 값이므로 변환
    # False: 남성, True: 여성
    data["gender_str"] = data["gender"].apply(lambda x: "여성" if x else "남성")
    with col1:
        st.write("**성별 분포 (%)**")
        gender_counts = data["gender_str"].value_counts().reset_index()
        gender_counts.columns = ["성별", "Count"]
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
        st.altair_chart(pie_chart + text_chart, use_container_width=True)

    # 지역 분포
    with col2:
        st.write("**지역별 응답자 분포 (%)**")
        df_region = data[["region"]]
        region_counts = df_region["region"].value_counts().sort_values(ascending=True)
        st.bar_chart(region_counts)

    st.divider()
    st.subheader("만족도 분석 강화")
    st.divider()

    # --- 만족도 분석: 각 영역별 평균 점수 계산 ---
    # 주행 승차감 분석: q1 ~ q5
    q1_to_q5 = data[["q1", "q2", "q3", "q4", "q5"]].mean()
    # 영역에 맞는 라벨 (필요에 따라 수정)
    categories_drive = ["승차감", "안정성", "소음", "진동", "가속감"]
    values_drive = q1_to_q5.values

    # 긴급 상황 대응 분석: q6 ~ q10
    q6_to_q10 = data[["q6", "q7", "q8", "q9", "q10"]].mean()
    categories_emergency = [
        "상황인식",
        "대응속도",
        "커뮤니케이션",
        "장비신뢰성",
        "협력",
    ]
    values_emergency = q6_to_q10.values

    # 주차 기능 분석: q11 ~ q13
    q11_to_q13 = data[["q11", "q12", "q13"]].mean()
    categories_parking = ["주차 편의성", "센서 정확도", "자동 제어"]
    values_parking = q11_to_q13.values

    # 전반 만족도 추천: q14 ~ q16
    q14_to_q16 = data[["q14", "q15", "q16"]].mean()
    categories_overall = ["내구성", "힘", "지능"]
    values_overall = q14_to_q16.values

    # 레이아웃: 2행 구성
    # 1행: 주행 승차감 분석(레이더 차트) 및 긴급 상황 대응 분석(막대 차트)
    row1_col1, row1_col2 = st.columns(2)

    # [1-1] 주행 승차감 분석 (레이더 차트)
    with row1_col1:
        fig1, ax1 = radar_chart(
            values=values_drive,
            categories=categories_drive,
            title="주행 승차감",
            color="blue",
            alpha=0.3,
            max_radius=5,  # 설문 점수가 1~5로 가정
            figsize=(3, 3),
            label_fontsize=8,
            title_fontsize=12,
        )
        st.write("**주행 승차감 분석**")
        st.pyplot(fig1)

    # [1-2] 긴급 상황 대응 분석 (막대 차트)
    with row1_col2:
        st.write("**긴급 상황 대응 분석**")
        df_emergency = pd.DataFrame(
            {"영역": categories_emergency, "평균점수": values_emergency}
        )
        st.bar_chart(df_emergency.set_index("영역"))

    # 2행: 주차 기능 분석(막대 차트) 및 전반 만족도 추천(레이더 차트)
    row2_col1, row2_col2 = st.columns(2)

    # [2-1] 주차 기능 분석 (막대 차트)
    with row2_col1:
        st.write("**주차 기능 분석**")
        df_parking = pd.DataFrame(
            {"영역": categories_parking, "평균점수": values_parking}
        )
        st.bar_chart(df_parking.set_index("영역"))

    # [2-2] 전반 만족도 추천 (레이더 차트)
    with row2_col2:
        fig2, ax2 = radar_chart(
            values=values_overall,
            categories=categories_overall,
            title="전반 만족도",
            color="green",
            alpha=0.3,
            max_radius=5,
            figsize=(3, 3),
            label_fontsize=8,
            title_fontsize=12,
        )
        st.write("**전반 만족도 추천**")
        st.pyplot(fig2)

    # (4) 보고서 코멘트
    comment = st.text_area("AI 분석 코멘트 ")


# # 실제 앱 실행 시 show_result() 호출
# if __name__ == "__main__":
#     show_result()
