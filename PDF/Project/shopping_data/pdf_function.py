import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
from io import BytesIO
import tempfile
import base64
import os

plt.rcParams["font.family"] = "AppleGothic"  # macOS 폰트 (또는 NanumGothic 등)
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지



class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("NanumGothic", "", "./NanumGothic.ttf", uni=True)
        self.set_font("NanumGothic", "", 12)



def insert_image_from_buffer(
    pdf, img_buf, x=None, y=None, w=180, h=100, img_type="PNG"
):
    """
    BytesIO 객체 → 임시 파일로 저장 후 PDF에 이미지 삽입.
    x, y, w, h를 적절히 조정해서 레이아웃을 맞춘다.
    """
    with tempfile.NamedTemporaryFile(
        delete=False, suffix="." + img_type.lower()
    ) as tmp:
        tmp.write(img_buf.getvalue())
        tmp.flush()
        filename = tmp.name

    # PDF에 이미지 삽입
    pdf.image(filename, x=x, y=y, w=w, h=h, type=img_type)
    os.remove(filename)  # 임시 파일 삭제


def get_pdf_base64(pdf_output):
    pdf_base64 = base64.b64encode(pdf_output.read()).decode("utf-8")
    return pdf_base64


def generate_pdf_with_charts(
    df,
    include_sales_trends,
    include_discount_revenue,
    include_margin_analysis,
    include_top_products,
    include_monthly_comparison,
):
    pdf = PDF()
    pdf.add_page()
    

    # 폰트 추가 (NanumGothic 예시)
    # 보고서 제목
    pdf.cell(0, 10, txt="쇼핑몰 데이터 분석 보고서", ln=True, align="C")
    pdf.ln(5)

    # [1] 매출 추이
    if include_sales_trends:
        pdf.multi_cell(0, 7, txt="### 매출 추이 (월별, 시간별, 일별)")
        pdf.ln(3)

        # 월별 매출 예시
        df["month"] = df["purchase_date"].dt.to_period("M")
        monthly_revenue = df.groupby("month")["revenue"].sum()

        # 차트 생성
        fig, ax = plt.subplots(figsize=(5, 3))
        monthly_revenue.plot(kind="line", marker="o", color="blue", ax=ax)
        ax.set_title("월별 매출 추이")
        ax.set_xlabel("월")
        ax.set_ylabel("매출")

        # 차트를 PNG로 저장
        img_buf = BytesIO()
        plt.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        # 이미지 삽입 (w=180, h=100 예시 → 실제 레이아웃에 맞춰 조정)
        insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100)
        # 이미지 높이(100) + 약간의 여백(5)만큼 줄바꿈
        pdf.ln(105)

        pdf.multi_cell(0, 7, txt="위 차트는 월별 매출 추이를 나타냅니다.")
        pdf.ln(5)

    # [2] 할인율에 따른 매출
    if include_discount_revenue:
        pdf.multi_cell(0, 7, txt="### 할인율에 따른 매출 추이")
        pdf.ln(3)

        df["discount_rate"] = (df["price"] - df["discounted_price"]) / df["price"] * 100
        discount_revenue = df.groupby("discount_rate")["revenue"].sum()

        fig, ax = plt.subplots(figsize=(5, 3))
        discount_revenue.plot(kind="line", marker="o", color="green", ax=ax)
        ax.set_title("할인율에 따른 매출 추이")
        ax.set_xlabel("할인율(%)")
        ax.set_ylabel("매출")

        img_buf = BytesIO()
        plt.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100)
        pdf.ln(105)

        pdf.multi_cell(0, 7, txt="위 차트는 할인율에 따른 매출 추이를 나타냅니다.")
        pdf.ln(5)

    # [3] 마진율 분석
    if include_margin_analysis:
        pdf.multi_cell(0, 7, txt="### 마진율 분석")
        pdf.ln(3)

        df["profit_margin"] = (
            (df["discounted_price"] - df["material_cost"])
            / df["discounted_price"]
            * 100
        )
        profit_data = df.groupby("product_name")["profit_margin"].mean()

        fig, ax = plt.subplots(figsize=(5, 3))
        profit_data.plot(kind="bar", color="lightgreen", ax=ax)
        ax.set_title("제품별 마진율")
        ax.set_xlabel("제품명")
        ax.set_ylabel("마진율(%)")

        img_buf = BytesIO()
        plt.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100)
        pdf.ln(105)

        pdf.multi_cell(0, 7, txt="위 차트는 제품별 마진율을 나타냅니다.")
        pdf.ln(5)

    # [4] 상위 3개 제품 매출
    if include_top_products:
        pdf.multi_cell(0, 7, txt="### 상위 3개 제품 매출 및 마진율")
        pdf.ln(3)

        top_3_products = (
            df.groupby("product_name")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
        )

        fig, ax = plt.subplots(figsize=(5, 3))
        top_3_products.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("상위 3개 제품 매출")
        ax.set_xlabel("제품명")
        ax.set_ylabel("매출")

        img_buf = BytesIO()
        plt.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100)
        pdf.ln(105)

        pdf.multi_cell(0, 7, txt="위 차트는 상위 3개 제품의 매출을 나타냅니다.")
        pdf.ln(5)

    # [5] 월별 손익 분기점 비교
    if include_monthly_comparison:
        pdf.multi_cell(0, 7, txt="### 월별 손익 분기점 비교")
        pdf.ln(3)

        fixed_cost = 1000000
        df["bep"] = fixed_cost / (df["price"] - df["material_cost"])
        monthly_bep = df.groupby("month")["bep"].mean()

        fig, ax = plt.subplots(figsize=(5, 3))
        monthly_bep.plot(kind="line", marker="o", color="red", ax=ax)
        ax.set_title("월별 손익 분기점(BEP) 추이")
        ax.set_xlabel("월")
        ax.set_ylabel("BEP")

        img_buf = BytesIO()
        plt.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        insert_image_from_buffer(pdf, img_buf, x=15, y=None, w=180, h=100)
        pdf.ln(105)

        pdf.multi_cell(0, 7, txt="위 차트는 월별 손익 분기점(BEP)을 나타냅니다.")
        pdf.ln(5)

    # PDF를 문자열로 반환 후 바이트 변환
    pdf_bytes = pdf.output(dest="S")  
    pdf_output = BytesIO(pdf_bytes)  
    pdf_output.seek(0)


    return pdf_output
