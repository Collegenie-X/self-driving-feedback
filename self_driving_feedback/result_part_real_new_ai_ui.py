import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# 컴포넌트 모듈 불러오기
from components.data_loader import load_analysis_stats
from components.prompt_generator import generate_prompt
from components.ai_comment import call_openai
from components.output_parser import parse_output

import json

# 한글 폰트 설정 (Windows: Malgun Gothic, macOS: AppleGothic)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


def open_ai_comment(analysis_stats):

    prompt = generate_prompt(analysis_stats)
    ai_raw_response = call_openai(prompt)

    st.subheader("AI 원본 응답")
    st.json(ai_raw_response)

    ### JSON 파싱 시도

    try:
        parsed_json = json.loads(ai_raw_response)
    except json.JSONDecodeError:
        st.error("JSON 디코딩 실패! AI 응답이 JSON 형식이 아닙니다.")
        parsed_json = {}

    return parsed_json


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

    # 1. 조사 개요
    st.subheader("설문 조사 개요")
    st.divider()
    st.write("- **설문 조사 기간**: 2025.03.14 ~ 2025.03.26 **(12일간)**")

    # CSV 데이터 로드
    data = pd.read_csv("./data/survey_results.csv")
    st.write(f"- **전체 응답자 수**: {len(data)}명")

    st.divider()
    st.subheader("응답자 특성 분석")
    st.divider()

    # 응답자 분포 분석 (연령, 성별, 지역)
    bins = [0, 19, 29, 39, 49, 59, 100]
    labels = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
    data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels, right=False)
    data["gender_str"] = data["gender"].apply(lambda x: "여성" if x else "남성")

    # 연령별 분포
    age_group_counts = (
        data["age_group"].value_counts().rename_axis("연령별").reset_index(name="Count")
    )
    chart_age = (
        alt.Chart(age_group_counts)
        .mark_bar()
        .encode(
            x=alt.X("연령별:N", sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Count:Q"),
            tooltip=["연령별:N", "Count:Q"],
        )
        .properties(width=300, height=250)
    )
    text_age = chart_age.mark_text(dy=-6, fontSize=12).encode(text="Count:Q")

    # 성별 분포 (파이 차트)
    gender_counts = data["gender_str"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]
    total_count = gender_counts["count"].sum()
    pie_chart = (
        alt.Chart(gender_counts)
        .mark_arc(outerRadius=130)
        .encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="gender", type="nominal"),
            tooltip=["gender", "count"],
        )
        .transform_calculate(
            Percent="(round((datum.count / {0})*100)) + '%'".format(total_count)
        )
        .properties(width=350, height=350)
    )
    text_chart = pie_chart.mark_text(
        radius=130, size=16, align="center", baseline="middle", dx=0, dy=15
    ).encode(text=alt.Text("Percent:N"))

    # 지역별 분포
    region_counts = (
        data["region"].value_counts().rename_axis("지역별").reset_index(name="Count")
    )
    chart_region = (
        alt.Chart(region_counts)
        .mark_bar()
        .encode(
            x=alt.X("지역별:N", sort=None, axis=alt.Axis(labelAngle=0)),
            y="Count:Q",
            tooltip=["지역별:N", "Count:Q"],
        )
        .properties(width=300, height=450)
    )
    text_region = chart_region.mark_text(dy=-10, fontSize=12).encode(
        text=alt.Text("Count:Q")
    )

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
    q1_to_q5 = data[["q1", "q2", "q3", "q4", "q5"]].mean()
    categories_drive = ["승차감", "안정성", "소음", "진동", "가속감"]
    values_drive = q1_to_q5.values

    q6_to_q10 = data[["q6", "q7", "q8", "q9", "q10"]].mean()
    categories_emergency = [
        "상황인식",
        "대응속도",
        "커뮤니케이션",
        "장비신뢰성",
        "협력",
    ]
    values_emergency = q6_to_q10.values

    q11_to_q13 = data[["q11", "q12", "q13"]].mean()
    categories_parking = ["주차 편의성", "센서 정확도", "자동 제어"]
    values_parking = q11_to_q13.values

    q14_to_q16 = data[["q14", "q15", "q16"]].mean()
    categories_overall = ["내구성", "힘", "지능"]
    values_overall = q14_to_q16.values

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        fig1, _ = radar_chart(
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
            align="center", baseline="bottom", dy=-5, fontSize=12
        ).encode(text=alt.Text("평균점수:Q", format=".2f"))
        st.altair_chart(
            (chart_emerg + text_emerg).properties(width=300, height=500),
            use_container_width=True,
        )

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
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
            align="center", baseline="bottom", dy=-5, fontSize=12
        ).encode(text=alt.Text("평균점수:Q", format=".2f"))
        st.altair_chart(
            (chart_parking + text_parking).properties(width=300, height=500)
        )
    with row2_col2:
        fig2, _ = radar_chart(
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


    st.title("자율주행 시스템 설문 분석 - AI 코멘트")
    st.write("CSV 파일에서 설문 데이터를 불러와 통계를 내고, AI 코멘트를 생성합니다.")

    # CSV 로드
    df = pd.read_csv("./data/survey_results.csv")

    # 예시: 평균 점수 계산
    drive_mean = df[["q1", "q2", "q3", "q4", "q5"]].mean().mean()
    emergency_mean = df[["q6", "q7", "q8", "q9", "q10"]].mean().mean()
    parking_mean = df[["q11", "q12", "q13"]].mean().mean()
    overall_mean = df[["q14", "q15", "q16"]].mean().mean()

    analysis_stats = {
        "driving_comfort": round(drive_mean, 2),
        "emergency_response": round(emergency_mean, 2),
        "parking_function": round(parking_mean, 2),
        "overall_satisfaction": round(overall_mean, 2),
    }

    st.subheader("설문 통계")
    st.json(analysis_stats)

    # Streamlit 버튼: AI 코멘트 생성
    if st.button("AI 코멘트 생성"):
        st.error("OPEN AI에서 Comment를 처리중입니다........ ")

        #####  OPEN AI를 통해서 comment ################
        # parsed_json = open_ai_comment(analysis_stats)

        parsed_json = {
            "driving_comfort": {
                "summary": "전반적으로 평탄하고 안정감 있는 주행 품질이 만족스럽다는 느낌을 받았습니다.",
                "positive_opinion": "마치 운전자가 직접 조작하는 것처럼 자연스러운 주행이 인상적이었습니다. 또한, 섬세한 조작으로 승차감이 깔끔하게 전달되는 점이 대단했습니다.",
                "negative_opinion": "그러나 조금 더 다양한 주행 상황에 대응할 수 있는 섬세한 주행 조작이 필요하다는 의견도 있습니다.",
            },
            "emergency_response": {
                "summary": "긴급 상황에서도 안정적으로 대처하는 능력이 훌륭합니다.",
                "positive_opinion": "긴급 상황 발생 시 즉각적이고 정확한 대응으로 안전한 운전을 유지했습니다. 이는 신뢰를 높이는 중요한 요소가 되었습니다.",
                "negative_opinion": "그러나 일부 사용자들은 더욱 빠른 대응 속도와 예측 능력이 필요하다는 의견을 내놓았습니다.",
            },
            "parking_function": {
                "summary": "주차 기능은 전반적으로 부드럽고 정확하게 작동했습니다.",
                "positive_opinion": "복잡한 주차 상황에서도 자동 주차 기능이 빛을 발하며 사용자의 스트레스를 줄여주었습니다. 특히, 정밀한 센서와 알고리즘이 잘 조화를 이루었습니다.",
                "negative_opinion": "하지만, 일부 사용자들은 느린 주차 속도에 대한 부정적인 평가를 하였습니다.",
            },
            "overall_satisfaction": {
                "summary": "전체적으로 자율주행 시스템에 대한 만족도는 높았으나, 약간의 개선이 필요합니다.",
                "positive_opinion": "스스로 주행하며 운전자의 부담을 줄이는 점이 매우 만족스러웠습니다. 또한, 안전성과 편의성이 공존하는 시스템이 인상적이었습니다.",
                "negative_opinion": "그러나, 조금 더 빠른 반응 속도와 예상치 못한 상황에 대한 대응 능력의 제고가 필요하다는 의견이 있습니다.",
            },
        }

        if parsed_json:
            st.subheader("AI 코멘트")
            # 항목별 출력
            for section, content in parsed_json.items():
                st.markdown(f"### {section.replace('_',' ').title()}")
                if isinstance(content, dict):
                    st.write("**요약:**", content.get("summary", "정보 없음"))
                    st.success(
                        "**긍정 의견:** " + content.get("positive_opinion", "정보 없음")
                    )
                    st.error(
                        "**부정 의견:** " + content.get("negative_opinion", "정보 없음")
                    )
                else:
                    st.write("응답:", content)
