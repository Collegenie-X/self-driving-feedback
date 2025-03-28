###### product_id: 제품 고유 ID
###### product_name: 제품명 (메이커 코딩 제품 10개)
###### category: 제품 카테고리 (예: 교육 키트, 소프트웨어 등)
###### price: 제품 가격
###### discounted_price: 할인된 가격
###### sold_quantity: 판매된 수량
###### rating: 제품 평점
###### purchase_date: 구매 날짜
###### region: 구매 지역 (서울, 부산 등)
###### material_cost: 재료비 원가 (가격의 40%)
###### revenue: 매출 (판매량 * 가격)
###### discount_rate: 할인율 (할인된 가격 / 원래 가격)


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO
import io

from Streamlit.Project.shopping_data.pdf_function import generate_pdf_with_charts, get_pdf_base64


plt.rcParams["font.family"] = "AppleGothic"  # macOS font that supports Hangul
# plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows에서 한글을 지원하는 폰트
plt.rcParams["axes.unicode_minus"] = False  # Ensure minus sign is displayed correctly


# 앱 제목
st.title("메이커 코딩 제품 매출 분석")


# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 파일 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터프레임 미리보기
    st.write("### 데이터 미리보기", df.head())

    # 데이터 정보 (info)
    st.write("### 데이터 정보 (info())")
    df_info = io.StringIO()
    df.info(buf=df_info)
    df_info.seek(0)  # Go to the beginning of the StringIO object

    # Display the DataFrame info in Streamlit
    st.text(df_info.getvalue())

    # 통계 요약 정보 (describe)
    st.write("### 통계적 요약 (describe())")
    st.write(df.describe())

    # 결측치 확인
    st.write("### 결측치 현황")
    st.write(df.isnull().sum())

    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")

    # 결측치를 평균값으로 대체 (예: discounted_price)
    df["discounted_price"].fillna(df["discounted_price"].mean(), inplace=True)

    # 결측치를 앞의 값으로 채우기 (예: sold_quantity)
    df["sold_quantity"].fillna(method="ffill", inplace=True)

    # 결측치를 특정 상수로 채우기 (예: rating)
    df["rating"].fillna(3.5, inplace=True)

    #########  이상치 처리 ################
    # 가격이 음수인 경우, 0으로 교체
    df["price"] = df["price"].apply(lambda x: 0 if x < 0 else x)

    # 판매량이 0인 경우, 최빈값으로 교체 (예: 'sold_quantity')
    sold_quantity_mode = df["sold_quantity"].mode()[0]
    df["sold_quantity"] = df["sold_quantity"].replace(0, sold_quantity_mode)

    st.write("### 결측치 처리 후 데이터 미리보기")
    st.write(df.head())

    # 월별 매출 추이
    df["month"] = df["purchase_date"].dt.to_period("M")
    monthly_revenue = df.groupby("month")["revenue"].sum()

    # Streamlit 내장 차트로 시각화 (선 차트)
    st.write("### 월별 매출 추이")
    st.line_chart(monthly_revenue)

    # 지역별 매출
    region_revenue = df.groupby("region")["revenue"].sum()

    # Streamlit 내장 차트로 시각화 (막대 차트)
    st.write("### 지역별 매출 추이")
    st.bar_chart(region_revenue)

    # # 시각화
    # plt.figure(figsize=(10, 6))
    # monthly_revenue.plot(kind="line", marker="o", color="green")
    # plt.title("월별 매출 추이")
    # plt.xlabel("월")
    # plt.ylabel("매출")
    # st.pyplot(plt)

    # # 지역별 매출
    # region_revenue = df.groupby("region")["revenue"].sum()

    # # 시각화
    # plt.figure(figsize=(10, 6))
    # region_revenue.plot(kind="bar", color="purple")
    # plt.title("지역별 매출 추이")
    # plt.xlabel("지역")
    # plt.ylabel("매출")
    # st.pyplot(plt)

    # 재료비 원가와 손익 분기점 계산
    df["material_cost"] = df["price"] * 0.4
    df["profit_margin"] = (
        (df["discounted_price"] - df["material_cost"]) / df["discounted_price"] * 100
    )

    # 손익 분기점 계산 (고정비용 / (판매가격 - 재료비))
    fixed_cost = 10000000  # 예시 고정비용 (원)
    df["bep"] = fixed_cost / (df["price"] - df["material_cost"])

    # 손익 분기점에서 NaN 또는 Inf 값 제거
    df["bep"].replace([np.inf, -np.inf], np.nan, inplace=True)  # Inf 값은 NaN으로 처리
    df.dropna(subset=["bep"], inplace=True)  # NaN 값을 가진 행 삭제

    # 시각화 (마진율 vs 손익 분기점)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # X축을 제품 이름으로 설정 (인덱스 사용)
    ax1.set_xlabel("제품")
    ax1.set_ylabel("마진율 (%)", color="tab:blue")
    ax1.plot(
        df["product_name"],
        df["profit_margin"],
        color="tab:blue",
        label="마진율",
        marker="o",
    )

    # Y축이 다른 데이터 (손익 분기점)을 위해 twinx 사용
    ax2 = ax1.twinx()
    ax2.set_ylabel("손익 분기점 (BEP)", color="tab:red")
    ax2.plot(
        df["product_name"], df["bep"], color="tab:red", label="손익 분기점", marker="o"
    )

    # 제품 이름이 겹치지 않도록 X축 레이블 회전
    plt.xticks(rotation=45, ha="right")

    # 겹치지 않도록 마진율과 BEP의 범위를 조정
    ax1.set_ylim(0, 100)  # 마진율 범위 (0~100%)
    ax2.set_ylim(0, max(df["bep"]) * 1.1)  # BEP 값 범위 (max값 계산 후 10% 여유 추가)

    fig.tight_layout()  # 레이아웃 자동 조정
    st.pyplot(fig)

    st.write(df.head(20))

    # 중복된 제품 이름에 대해 판매량 합산
    df_product_name = (
        df.groupby("product_name")
        .agg(
            {
                "sold_quantity": "sum",
                "revenue": "sum",
                "price": "mean",
                "discounted_price": "mean",
                "material_cost": "mean",
                "rating": "mean",
            }
        )
        .reset_index()
    )

    # 시각화: 판매량 합산 히스토그램
    st.write("### 제품별 판매량 합산 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["sold_quantity"])

    # 시각화: 매출 합산 히스토그램
    st.write("### 제품별 매출 합산 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["revenue"])

    # 시각화: 가격 평균 히스토그램
    st.write("### 제품별 평균 가격 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["price"])

    # 시각화: 할인된 가격 평균 히스토그램
    st.write("### 제품별 평균 할인된 가격 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["discounted_price"])

    # 시각화: 재료비 평균 히스토그램
    st.write("### 제품별 평균 재료비 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["material_cost"])

    # 시각화: 제품 평점 평균 히스토그램
    st.write("### 제품별 평균 평점 히스토그램")
    st.bar_chart(df_product_name.set_index("product_name")["rating"])

    st.write("### 중복 처리 후 데이터 미리보기")
    st.write(df_product_name)

    # 1. 가격이 100 이상인 제품만 필터링
    filtered_data = df[df["price"] >= 100]

    # 2. 카테고리별 매출 집계
    category_revenue = df.groupby("category")["revenue"].sum()

    # 3. 제품별 매출 추이
    product_revenue = df.groupby("product_name")["revenue"].sum()

    # 시각화: 카테고리별 매출 (Streamlit 내장 차트)
    st.write("### 카테고리별 매출")
    st.bar_chart(category_revenue)

    # 시각화: 제품별 매출 (Streamlit 내장 차트)
    st.write("### 제품별 매출")
    st.bar_chart(product_revenue)

    # 보고서 제목 및 사용자 선택
    st.title("쇼핑몰 매출 분석 보고서")
    st.write("다음 항목을 보고서에 포함시킬 수 있습니다:")

    # 항목 선택 (checkbox로 사용자가 선택)
    include_sales_trends = st.checkbox("매출 추이 (월별, 시간별, 일별)", True)
    include_discount_revenue = st.checkbox("할인율에 따른 매출 추이", True)
    include_margin_analysis = st.checkbox("마진율 분석", True)
    include_top_products = st.checkbox("상위 3개 제품 매출 및 마진율", True)
    include_monthly_comparison = st.checkbox("월별 손익 분기점 비교", True)

    # PDF 다운로드 버튼
    if st.button("보고서 생성"):
        # PDF 생성
        pdf_output = generate_pdf_with_charts(
            df,
            include_sales_trends,
            include_discount_revenue,
            include_margin_analysis,
            include_top_products,
            include_monthly_comparison,
        )

        # PDF 미리 보기
        pdf_base64 = get_pdf_base64(pdf_output)

        # Streamlit에 PDF 미리 보기
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>',
            unsafe_allow_html=True,
        )

        # 다운로드 버튼
        st.download_button(
            label="PDF로 다운로드",
            data=pdf_output,
            file_name="shopping_report.pdf",
            mime="application/pdf",
        )
