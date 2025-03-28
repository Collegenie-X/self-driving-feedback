import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO, StringIO
import tempfile
import base64
import os

# 한글 폰트 설정 (macOS의 경우 AppleGothic, Windows는 Malgun Gothic 등 사용)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


# PDF 클래스 확장 (필요에 따라 커스텀 가능)
class PDF(FPDF):
    pass


def insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100, img_type="PNG"):
    """
    BytesIO 객체에 저장된 이미지를 임시 파일로 저장한 후, 해당 파일을 PDF에 삽입하고 임시 파일을 삭제하는 함수.
    """
    with tempfile.NamedTemporaryFile(
        delete=False, suffix="." + img_type.lower()
    ) as tmp:
        tmp.write(img_buf.getvalue())
        tmp.flush()
        filename = tmp.name

    pdf.image(filename, x=x, y=y, w=w, h=h, type=img_type)
    os.remove(filename)


def plot_discount_rate_chart(df):
    """
    할인율에 따른 매출 차트를 생성하고 Figure 객체를 반환하는 함수.
    """
    # 할인율 계산
    df["discount_rate"] = (df["price"] - df["discounted_price"]) / df["price"] * 100
    discount_sales = df.groupby("discount_rate")["sold_quantity"].sum()
    discount_revenue = df.groupby("discount_rate")["revenue"].sum()

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_xlabel("할인율 (%)")
    ax1.set_ylabel("판매량", color="blue")
    ax1.plot(
        discount_sales.index,
        discount_sales.values,
        color="blue",
        marker="o",
        label="판매량",
    )

    ax2 = ax1.twinx()
    ax2.set_ylabel("매출", color="red")
    ax2.plot(
        discount_revenue.index,
        discount_revenue.values,
        color="red",
        marker="o",
        label="매출",
    )
    ax1.set_title("할인율에 따른 매출 추이")
    fig.tight_layout()
    return fig


def plot_category_chart(df):
    """
    카테고리별 매출 차트를 생성하고 Figure 객체를 반환하는 함수.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    category_revenue = df.groupby("category")["revenue"].sum()
    category_revenue.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title("카테고리별 매출")
    ax.set_xlabel("카테고리")
    ax.set_ylabel("매출")
    fig.tight_layout()
    return fig


def plot_monthly_chart(df):
    """
    월별 매출 추이 차트를 생성하고 Figure 객체를 반환하는 함수.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    df["month"] = df["purchase_date"].dt.to_period("M")
    monthly_revenue = df.groupby("month")["revenue"].sum()
    monthly_revenue.plot(kind="line", marker="o", color="green", ax=ax)
    ax.set_title("월별 매출 추이")
    ax.set_xlabel("월")
    ax.set_ylabel("매출")
    fig.tight_layout()
    return fig


def plot_region_chart(df):
    """
    지역별 매출 추이 차트를 생성하고 Figure 객체를 반환하는 함수.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    region_revenue = df.groupby("region")["revenue"].sum()
    region_revenue.plot(kind="bar", color="purple", ax=ax)
    ax.set_title("지역별 매출 추이")
    ax.set_xlabel("지역")
    ax.set_ylabel("매출")
    fig.tight_layout()
    return fig


def generate_pdf(df):
    """
    데이터 요약, df.info()와 각 차트를 PDF에 삽입하여 PDF 파일 객체(BytesIO)를 반환하는 함수.
    """
    pdf = PDF()
    pdf.add_page()

    # 한글 폰트 추가 (NanumGothic 예시, 경로 수정)
    pdf.add_font("NanumGothic", "", "./NanumGothic.ttf", uni=True)
    pdf.set_font("NanumGothic", size=12)

    # 1. 보고서 제목
    pdf.cell(0, 10, txt="쇼핑몰 데이터 분석 보고서", ln=True, align="C")
    pdf.ln(10)

    # 2. 데이터 요약 (상위 5개 행)
    pdf.multi_cell(
        0, 10, txt="### 데이터 요약\n" + str(df[["product_name", "revenue"]].head())
    )
    pdf.ln(5)

    # 3. df.info() 내용 추가
    pdf.cell(0, 10, txt="### 데이터 정보", ln=True, align="L")
    info_buf = StringIO()
    df.info(buf=info_buf)
    info_buf.seek(0)
    info_str = info_buf.read()
    pdf.multi_cell(0, 7, txt=info_str)
    pdf.ln(5)

    # 4. 할인율에 따른 매출 차트
    fig1 = plot_discount_rate_chart(df)
    pdf.multi_cell(0, 10, txt="### 할인율에 따른 매출 차트")
    pdf.ln(3)
    # 차트 이미지를 PDF에 삽입 (이미지 크기 조정: w=180, h=100)
    buf1 = BytesIO()
    fig1.savefig(buf1, format="png", bbox_inches="tight")
    plt.close(fig1)
    buf1.seek(0)
    insert_image_from_buffer(pdf, buf1, x=15, y=None, w=180, h=100)
    pdf.ln(105)
    pdf.multi_cell(0, 7, txt="위 차트는 할인율별 판매량과 매출 추이를 나타냅니다.")
    pdf.ln(5)

    # 5. 카테고리별 매출 차트
    fig2 = plot_category_chart(df)
    pdf.multi_cell(0, 10, txt="### 카테고리별 매출 차트")
    pdf.ln(3)
    buf2 = BytesIO()
    fig2.savefig(buf2, format="png", bbox_inches="tight")
    plt.close(fig2)
    buf2.seek(0)
    insert_image_from_buffer(pdf, buf2, x=15, y=None, w=180, h=100)
    pdf.ln(105)
    pdf.multi_cell(0, 7, txt="위 차트는 카테고리별 총 매출을 나타냅니다.")
    pdf.ln(5)

    # 6. 월별 매출 추이 차트
    fig3 = plot_monthly_chart(df)
    pdf.multi_cell(0, 10, txt="### 월별 매출 추이 차트")
    pdf.ln(3)
    buf3 = BytesIO()
    fig3.savefig(buf3, format="png", bbox_inches="tight")
    plt.close(fig3)
    buf3.seek(0)
    insert_image_from_buffer(pdf, buf3, x=15, y=None, w=180, h=100)
    pdf.ln(105)
    pdf.multi_cell(0, 7, txt="위 차트는 월별 매출 변화를 보여줍니다.")
    pdf.ln(5)

    # 7. 지역별 매출 추이 차트
    fig4 = plot_region_chart(df)
    pdf.multi_cell(0, 10, txt="### 지역별 매출 추이 차트")
    pdf.ln(3)
    buf4 = BytesIO()
    fig4.savefig(buf4, format="png", bbox_inches="tight")
    plt.close(fig4)
    buf4.seek(0)
    insert_image_from_buffer(pdf, buf4, x=15, y=None, w=180, h=100)
    pdf.ln(105)
    pdf.multi_cell(0, 7, txt="위 차트는 지역별 매출 분포를 나타냅니다.")
    pdf.ln(5)

    # PDF를 문자열로 반환 후 바이트로 변환
    pdf_str = pdf.output(dest="S")
    pdf_bytes = pdf_str.encode("latin1")
    pdf_output = BytesIO(pdf_bytes)
    pdf_output.seek(0)

    return pdf_output


def get_pdf_base64(pdf_output):
    pdf_base64 = base64.b64encode(pdf_output.read()).decode("utf-8")
    return pdf_base64


def main():
    st.title("메이커 코딩 제품 매출 분석 보고서")

    # CSV 파일 업로드
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # 데이터 전처리
        df["discounted_price"] = df["discounted_price"].fillna(
            df["discounted_price"].mean()
        )
        df["price"] = df["price"].apply(lambda x: 0 if x < 0 else x)
        df = df.drop_duplicates()
        df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
        df = df.dropna(subset=["purchase_date"])

        # 정제된 데이터 미리보기
        st.write("### 정제된 데이터 미리보기", df.head())
        info_buf = StringIO()
        df.info(buf=info_buf)
        info_buf.seek(0)
        st.text(info_buf.read())

        # 차트 미리보기
        st.write("### 할인율에 따른 매출 차트 미리보기")
        fig1 = plot_discount_rate_chart(df)
        st.pyplot(fig1)

        st.write("### 카테고리별 매출 차트 미리보기")
        fig2 = plot_category_chart(df)
        st.pyplot(fig2)

        st.write("### 월별 매출 추이 차트 미리보기")
        fig3 = plot_monthly_chart(df)
        st.pyplot(fig3)

        st.write("### 지역별 매출 추이 차트 미리보기")
        fig4 = plot_region_chart(df)
        st.pyplot(fig4)

        # PDF 다운로드 버튼
        if st.button("보고서 다운로드"):
            pdf_output = generate_pdf(df)
            pdf_base64 = get_pdf_base64(pdf_output)
            # 다시 포인터를 0으로 재설정 (다운로드 버튼에서도 사용)
            pdf_output.seek(0)
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="PDF로 다운로드",
                data=pdf_output,
                file_name="shopping_report.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()
