# pdf_export.py
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

from fpdf import FPDF
from io import BytesIO
from PIL import Image

import tempfile  # 임시 파일 생성용

# 한글 폰트 설정 (macOS의 경우 AppleGothic, Windows는 Malgun Gothic 등 사용)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


def radar_chart(
    values, categories, color="blue", alpha=0.3, max_radius=5, figsize=(2, 2)
):
    """
    레이더 차트(Matplotlib) 생성 후 (fig, ax) 반환
    """
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": "polar"})
    ax.plot(angles, values, color=color, linewidth=1)
    ax.fill(angles, values, color=color, alpha=alpha)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8)

    if max_radius is not None:
        ax.set_ylim(0, max_radius)

    ax.tick_params(axis="y", labelsize=7)
    return fig, ax


def make_survey_report_pdf() -> BytesIO:
    """
    CSV -> 통계 계산 -> Altair/Matplotlib 차트 -> PDF -> BytesIO
    """

    # (1) CSV 로드
    data = pd.read_csv("./data/survey_results.csv")
    survey_start = "2025.03.14"
    survey_end = "2025.03.26"
    total_respondents = len(data)

    # (2) 지표 계산
    q1_to_q5 = data[["q1", "q2", "q3", "q4", "q5"]].mean()
    drive_mean = round(q1_to_q5.mean(), 2)

    q6_to_q10 = data[["q6", "q7", "q8", "q9", "q10"]].mean()
    emergency_mean = round(q6_to_q10.mean(), 2)

    q11_to_q13 = data[["q11", "q12", "q13"]].mean()
    parking_mean = round(q11_to_q13.mean(), 2)

    q14_to_q16 = data[["q14", "q15", "q16"]].mean()
    overall_mean = round(q14_to_q16.mean(), 2)

    # (3) 텍스트
    survey_summary = f"""
[조사 개요]
- 설문 조사 기간: {survey_start} ~ {survey_end} (12일간)
- 전체 응답자 수: {total_respondents}명

[주요 만족도 지표]
- 주행 승차감 평균: {drive_mean}
- 긴급 상황 대응 평균: {emergency_mean}
- 주차 기능 평균: {parking_mean}
- 전반 만족도 평균: {overall_mean}
"""

    # (4) Altair 차트 3개 -> PNG 임시파일
    bins = [0, 19, 29, 39, 49, 59, 120]
    labels = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
    data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels, right=False)

    age_counts = data["age_group"].value_counts().reset_index()
    age_counts.columns = ["연령별", "Count"]
    chart_age = (
        alt.Chart(age_counts)
        .mark_bar(color="steelblue")
        .encode(
            x=alt.X("연령별:N", sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Count:Q"),
            tooltip=["연령별", "Count"],
        )
        .properties(width=300, height=200, title="연령별 응답자 분포")
    )

    data["gender_str"] = data["gender"].apply(lambda x: "여성" if x else "남성")
    gender_counts = data["gender_str"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]
    total_count = gender_counts["count"].sum()
    chart_gender = (
        alt.Chart(gender_counts)
        .mark_arc(outerRadius=90)
        .encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="gender", type="nominal"),
            tooltip=["gender", "count"],
        )
        .properties(width=200, height=200, title="성별 분포 (%)")
        .transform_calculate(
            Percent=f"(round((datum.count / {total_count})*100)) + '%'"
        )
    )

    region_counts = (
        data["region"].value_counts().rename_axis("지역별").reset_index(name="Count")
    )
    chart_region = (
        alt.Chart(region_counts)
        .mark_bar(color="steelblue")
        .encode(
            x=alt.X(
                "지역별:N",
                sort=None,
                # ⬇︎ x축 라벨 60도 기울이기 + 한글 폰트/크기
                axis=alt.Axis(
                    labelAngle=-60, labelFont="NanumGothic", labelFontSize=12
                ),
            ),
            y=alt.Y(
                "Count:Q",
                axis=alt.Axis(labelFont="NanumGothic", labelFontSize=11),
            ),
            tooltip=["지역별", "Count"],
        )
        # ⬇︎ 차트 가로 너비 1.5배(예: 330) / 높이도 더 크게(예: 300)
        .properties(width=330, height=300, title="지역별 응답자 분포")
    )

    def altair_to_file(chart, suffix=".png"):
        """Altair -> PNG 임시파일 경로 반환"""
        buf = BytesIO()
        chart.save(buf, format="png", scale_factor=2)
        buf.seek(0)

        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(buf.read())
        tmp.flush()
        tmp_name = tmp.name
        tmp.close()
        return tmp_name

    img_age_path = altair_to_file(chart_age)
    img_gender_path = altair_to_file(chart_gender)
    img_region_path = altair_to_file(chart_region)

    # (5) Matplotlib 레이더 -> PNG 임시파일
    categories_drive = ["승차감", "안정성", "소음", "진동", "가속감"]
    fig_drive, _ = radar_chart(
        q1_to_q5.values, categories_drive, color="blue", alpha=0.3
    )
    drive_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig_drive.savefig(drive_tmp, format="png", dpi=100, bbox_inches="tight")
    drive_tmp_name = drive_tmp.name
    drive_tmp.close()

    categories_overall = ["내구성", "힘", "지능"]
    fig_overall, _ = radar_chart(
        q14_to_q16.values, categories_overall, color="green", alpha=0.3
    )
    overall_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig_overall.savefig(overall_tmp, format="png", dpi=100, bbox_inches="tight")
    overall_tmp_name = overall_tmp.name
    overall_tmp.close()

    plt.close(fig_drive)
    plt.close(fig_overall)

    # (6) FPDF 구성
    pdf = FPDF()
    pdf.add_page()
    # 폰트 등록
    pdf.add_font("NanumGothic", "", "NanumGothic.ttf", uni=True)
    pdf.add_font("NanumGothic", "B", "./NanumGothicBold.ttf", uni=True)
    pdf.set_font("NanumGothic", "", 14)

    # 보고서 제목
    pdf.cell(0, 10, txt="자율주행 설문 결과 보고서", ln=1, align="C")

    pdf.set_font("NanumGothic", "", 11)
    pdf.ln(5)
    pdf.multi_cell(0, 7, txt=survey_summary)
    pdf.ln(3)

    # 응답자 특성 분석
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(0, 10, txt="응답자 특성 분석", ln=1)
    pdf.ln(3)
    pdf.set_font("NanumGothic", "", 10)

    x_margin = pdf.get_x()
    y_position = pdf.get_y()

    # (1) 연령별
    pdf.image(img_age_path, x=x_margin, y=y_position, w=60, h=60)
    # (2) 지역별
    pdf.image(img_region_path, x=x_margin + 70, y=y_position, w=60, h=60)

    pdf.ln(65)
    pdf.image(img_gender_path, x=x_margin, w=60, h=60)
    pdf.ln(70)

    # 만족도 분석
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(0, 10, txt="만족도 분석", ln=1)
    pdf.set_font("NanumGothic", "", 10)
    pdf.ln(2)

    x_margin2 = pdf.get_x()
    y_position2 = pdf.get_y()

    pdf.cell(0, 6, txt="주행 승차감 분석(레이더)", ln=1)
    pdf.image(drive_tmp_name, x=x_margin2, y=y_position2 + 8, w=60, h=60)

    pdf.set_y(y_position2 + 8)
    pdf.set_x(x_margin2 + 70)
    pdf.cell(0, 6, txt="전반 만족도 분석(레이더)")
    pdf.image(overall_tmp_name, x=x_margin2 + 70, y=y_position2 + 14, w=60, h=60)
    pdf.ln(75)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer, "F")
    pdf_buffer.seek(0)

    return pdf_buffer


# if __name__ == "__main__":
#     pdf_data = make_survey_report_pdf()
#     with open("test_survey_report.pdf", "wb") as f:
#         f.write(pdf_data.read())
#     print("PDF 생성 완료 -> test_survey_report.pdf")
