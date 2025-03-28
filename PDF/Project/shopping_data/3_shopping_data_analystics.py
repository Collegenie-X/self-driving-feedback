import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# 앱 제목
st.title("메이커 코딩 제품 매출 분석")

# 파일 업로드
df = pd.read_csv("./shopping_mall_data.csv")

# 결측치 처리: 할인된 가격의 결측치를 평균값으로 대체
df["discounted_price"].fillna(df["discounted_price"].mean(), inplace=True)

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
