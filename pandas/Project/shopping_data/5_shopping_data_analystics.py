import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

plt.rcParams["font.family"] = "AppleGothic"  # macOS font that supports Hangul
# plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows에서 한글을 지원하는 폰트
plt.rcParams["axes.unicode_minus"] = False  # Ensure minus sign is displayed correctly


# 앱 제목
st.title("메이커 코딩 제품 매출 분석")

# 파일 업로드
df = pd.read_csv("./shopping_mall_data.csv")

# 결측치 처리: 할인된 가격의 결측치를 평균값으로 대체
# df["discounted_price"].fillna(df["discounted_price"].mean(), inplace=True)
df["discounted_price"] = df["discounted_price"].fillna(df["discounted_price"].mean())


# 이상치 처리: 가격이 음수인 경우 0으로 변경
df["price"] = df["price"].apply(lambda x: 0 if x < 0 else x)

# 중복 데이터 처리: 중복된 행 제거
df.drop_duplicates(inplace=True)

# 날짜 포맷 변환: datetime으로 변환
df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")

# 결측치가 있는 날짜 행 삭제
df.dropna(subset=["purchase_date"], inplace=True)

# 결과 확인
st.write("### 정제된 데이터", df.head())

df_info = io.StringIO()
df.info(buf=df_info)
df_info.seek(0)  # Go to the beginning of the StringIO object

# Display the DataFrame info in Streamlit
st.text(df_info.getvalue())


# 1. 할인율에 따른 매출 분석
df["discount_rate"] = (df["price"] - df["discounted_price"]) / df["price"] * 100
discount_sales = df.groupby("discount_rate")["sold_quantity"].sum()
discount_revenue = df.groupby("discount_rate")["revenue"].sum()

# 시각화
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel("Discount Rate (%)")
ax1.set_ylabel("Revenue", color="tab:blue")
ax1.plot(
    discount_sales.index,
    discount_sales.values,
    color="tab:blue",
    label="Price",
    marker="o",
)

ax2 = ax1.twinx()
ax2.set_ylabel("Revenue", color="tab:red")
ax2.plot(
    discount_revenue.index,
    discount_revenue.values,
    color="tab:red",
    label="Revenue",
    marker="o",
)

fig.tight_layout()
st.pyplot(fig)

# 2. 제품 카테고리별 매출
category_revenue = df.groupby("category")["revenue"].sum()

# 시각화
plt.figure(figsize=(10, 6))
category_revenue.plot(kind="bar", color="skyblue")
plt.title("Category Revenue")
plt.xlabel("Category")
plt.ylabel("Revenue")
st.pyplot(plt)


# 월별 매출 추이
df["month"] = df["purchase_date"].dt.to_period("M")
monthly_revenue = df.groupby("month")["revenue"].sum()

# 시각화
plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind="line", marker="o", color="green")
plt.title("월별 매출 추이")
plt.xlabel("월")
plt.ylabel("매출")
st.pyplot(plt)

# 지역별 매출
region_revenue = df.groupby("region")["revenue"].sum()

# 시각화
plt.figure(figsize=(10, 6))
region_revenue.plot(kind="bar", color="purple")
plt.title("지역별 매출 추이")
plt.xlabel("지역")
plt.ylabel("매출")
st.pyplot(plt)


# PDF 생성 함수
from fpdf import FPDF
from io import BytesIO


# PDF 생성 함수
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()

    # 한글 폰트 추가 (예: NanumGothic)
    pdf.add_font("NanumGothic", "", "./NanumGothic.ttf", uni=True)
    pdf.set_font("NanumGothic", size=12)

    pdf.cell(200, 10, txt="쇼핑몰 데이터 분석 보고서", ln=True, align="C")
    pdf.ln(10)

    # 데이터 요약 추가
    pdf.multi_cell(
        0, 10, txt="제품별 매출:\n" + str(df[["product_name", "revenue"]].head())
    )

    # 데이터 정보 추가 (df.info()는 문자열로 바로 반환되지 않으므로 주의)
    pdf.ln(10)
    pdf.cell(200, 10, txt="데이터 정보:", ln=True, align="L")
    # df.info()는 파일 객체에 출력되므로 별도로 처리해야 함
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    pdf.multi_cell(0, 10, txt=info_str)

    # PDF 내용을 문자열로 반환받기 (dest='S' 옵션)
    pdf_str = pdf.output(dest="S")
    # FPDF는 기본적으로 latin1 인코딩을 사용하므로 해당 인코딩으로 바이트로 변환
    pdf_bytes = pdf_str.encode("latin1")
    pdf_output = BytesIO(pdf_bytes)
    pdf_output.seek(0)

    return pdf_output


# PDF 다운로드
if st.button("보고서 다운로드"):
    pdf_data = generate_pdf(df)
    st.download_button(
        "PDF로 다운로드",
        pdf_data,
        file_name="shopping_report.pdf",
        mime="application/pdf",
    )
