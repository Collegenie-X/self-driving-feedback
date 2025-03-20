import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 기준: Malgun Gothic)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


# 레이더 차트 (Matplotlib)
def radar_chart(
    values,
    categories,
    color="blue",
    alpha=0.3,
    max_radius=None,
    figsize=(1.2, 1.2),
    label_fontsize=4,
):
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": "polar"})
    ax.plot(angles, values, color=color, linewidth=1)
    ax.fill(angles, values, color=color, alpha=alpha)
    ax.set_theta_offset(np.pi / 3)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=label_fontsize)

    if max_radius is not None:
        ax.set_ylim(0, max_radius)

    ax.tick_params(axis="y", labelsize=label_fontsize)
    return fig, ax


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

    # CSV 불러오기 (로컬 혹은 웹경로 수정)
    data = pd.read_csv("./data/survey_results.csv")
    st.write(f"- **전체 응답자 수**: {len(data)}명")

    st.divider()
    st.subheader("응답자 특성 분석")
    st.divider()

    # 나이대 컬럼 생성
    bins = [0, 19, 29, 39, 49, 59, 100]
    labels = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
    data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels, right=False)

    # 성별 문자열화
    data["gender_str"] = data["gender"].apply(lambda x: "여성" if x else "남성")

    # --- 레이아웃(2개 컬럼) ---

    # (1) 나이대별 응답자 분포
    bins = [0, 19, 29, 39, 49, 59, 100]
    labels = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
    data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels, right=False)

    age_group_counts = (
        data["age_group"].value_counts().rename_axis("연령별").reset_index(name="Count")
    )

    chart_age = (
        alt.Chart(age_group_counts)
        .mark_bar()
        .encode(
            x=alt.X("연령별:N", sort=None, axis=alt.Axis(labelAngle=0)),  # 레이블 수평
            y=alt.Y("Count:Q"),
            tooltip=["연령별:N", "Count:Q"],
        )
        .properties(width=300, height=250)  # 차트 크기 축소
    )

    text_age = chart_age.mark_text(dy=-6, fontSize=12).encode(text="Count:Q")

    # (2) 성별 분포 (Pie Chart)
    # gender: True/False -> 여성/남성 변환
    data["gender_str"] = data["gender"].apply(lambda x: "여성" if x else "남성")
    gender_counts = data["gender_str"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]
    total_count = gender_counts["count"].sum()

    pie_chart = (
        alt.Chart(gender_counts)
        .mark_arc(outerRadius=130)  # 파이 반경
        .encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="gender", type="nominal"),
            tooltip=["gender", "count"],
        )
        # 퍼센트 계산 (문자열 형태로 만들면서 % 기호까지 붙이기)
        .transform_calculate(
            Percent="(round((datum.count / {0})*100)) + '%'".format(total_count)
        )
        .properties(width=350, height=350)
    )

    # 텍스트(레이블) 설정
    text_chart = pie_chart.mark_text(
        radius=130,  # 파이보다 약간 바깥
        size=16,
        align="center",
        baseline="middle",
        dx=0,
        dy=15,
    ).encode(
        # transform_calculate에서 만든 Percent는 문자열이므로 type='nominal'로 매핑
        text=alt.Text("Percent:N")
    )

    # (3) 지역별 응답자 분포
    region_counts = (
        data["region"].value_counts().rename_axis("지역별").reset_index(name="Count")
    )

    chart_region = (
        alt.Chart(region_counts)
        .mark_bar()
        .encode(
            x=alt.X("지역별:N", sort=None, axis=alt.Axis(labelAngle=0)),  # 라벨 수평
            y="Count:Q",
            tooltip=["지역별:N", "Count:Q"],
        )
        .properties(width=300, height=450)
    )

    text_region = chart_region.mark_text(dy=-10, fontSize=12).encode(
        text=alt.Text("Count:Q")
    )

    # Streamlit 레이아웃
    col1, col2 = st.columns(2)
    with col1:
        st.write("**연령별 응답자 분포**")
        st.altair_chart(chart_age + text_age, use_container_width=True)

        st.write("**성별 분포 (%)**")
        st.altair_chart(pie_chart + text_chart, use_container_width=True)

    with col2:
        st.write("**지역별 응답자 분포**")
        st.altair_chart(chart_region + text_region, use_container_width=True)

    st.divider()
    st.subheader("만족도 분석 강화")
    st.divider()

    # 영역별 평균 계산
    # 1) 주행 승차감: q1~q5
    q1_to_q5 = data[["q1", "q2", "q3", "q4", "q5"]].mean()
    categories_drive = ["승차감", "안정성", "소음", "진동", "가속감"]
    values_drive = q1_to_q5.values

    # 2) 긴급 상황 대응: q6~q10
    q6_to_q10 = data[["q6", "q7", "q8", "q9", "q10"]].mean()
    categories_emergency = [
        "상황인식",
        "대응속도",
        "커뮤니케이션",
        "장비신뢰성",
        "협력",
    ]
    values_emergency = q6_to_q10.values

    # 3) 주차 기능: q11~q13
    q11_to_q13 = data[["q11", "q12", "q13"]].mean()
    categories_parking = ["주차 편의성", "센서 정확도", "자동 제어"]
    values_parking = q11_to_q13.values

    # 4) 전반 만족도: q14~q16
    q14_to_q16 = data[["q14", "q15", "q16"]].mean()
    categories_overall = ["내구성", "힘", "지능"]
    values_overall = q14_to_q16.values

    # 레이더 차트 및 Altair 막대차트 (2행 구성)
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # 주행 승차감 (레이더 차트)
        fig1, ax1 = radar_chart(
            values=values_drive,
            categories=categories_drive,
            color="blue",
            alpha=0.3,
            max_radius=5,
            label_fontsize=4,
        )
        st.write("**주행 승차감 분석**")
        st.pyplot(fig1)

    with row1_col2:
        # 긴급 상황 대응 분석 (막대 차트 + 평균값 표시)
        st.write("**긴급 상황 대응 분석**")
        df_emergency = pd.DataFrame(
            {"영역": categories_emergency, "평균점수": values_emergency}
        )
        chart_emerg = (
            alt.Chart(df_emergency)
            .mark_bar()
            .encode(
                x=alt.X("영역:N", sort=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("평균점수:Q", scale=alt.Scale(domain=[0, 5])),
                tooltip=["영역:N", "평균점수:Q"],
            )
        )

        text_emerg = chart_emerg.mark_text(
            align="center",
            baseline="bottom",
            dy=-5,  # y값 표시 위치를 조금 더 위로
            fontSize=12,
        ).encode(text=alt.Text("평균점수:Q", format=".2f"))

        st.altair_chart(
            (chart_emerg + text_emerg).properties(width=300, height=500),
            use_container_width=True,
        )

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        # 주차 기능 분석
        st.write("**주차 기능 분석**")
        df_parking = pd.DataFrame(
            {"영역": categories_parking, "평균점수": values_parking}
        )
        chart_parking = (
            alt.Chart(df_parking)
            .mark_bar()
            .encode(
                x=alt.X("영역:N", sort=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("평균점수:Q", scale=alt.Scale(domain=[0, 5])),
                tooltip=["영역:N", "평균점수:Q"],
            )
        )

        text_parking = chart_parking.mark_text(
            align="center",
            baseline="bottom",
            dy=-5,  # y값 표시 위치를 조금 더 위로
            fontSize=12,
        ).encode(text=alt.Text("평균점수:Q", format=".2f"))

        st.altair_chart(
            (chart_parking + text_parking).properties(width=300, height=500)
        )

    with row2_col2:
        # 전반 만족도 (레이더 차트)
        fig2, ax2 = radar_chart(
            values=values_overall,
            categories=categories_overall,
            color="green",
            alpha=0.3,
            max_radius=5,
            label_fontsize=4,
        )
        st.write("**전반 만족도 분석**")
        st.pyplot(fig2)

    st.divider()
    st.subheader("보고서 코멘트")
    comment = st.text_area("AI 분석 코멘트 ")


# 이 함수만 직접 호출하면 Streamlit 앱에서 결과 확인 가능
# if __name__ == "__main__":
#     show_result()
