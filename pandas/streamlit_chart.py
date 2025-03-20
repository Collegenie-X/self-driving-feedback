import streamlit as st
import pandas as pd
import numpy as np

st.title("선 그래프 예시")

df = pd.DataFrame(
    {
        "날짜": pd.date_range("2023-01-01", periods=100),
        "매출": np.random.randint(100, 500, 100),
    }
)

st.line_chart(df.set_index("날짜"), use_container_width=True)

st.title("막대 그래프 예시")

data = pd.DataFrame(
    {"상품": ["A", "B", "C", "D"], "판매량": [120, 250, 80, 160]}
).set_index("상품")

st.bar_chart(data, use_container_width=True)


st.title("Altair 선 그래프 예시")

df = pd.DataFrame(
    {
        "Year": ["2020", "2021", "2022", "2023"],
        "Sales": [100, 150, 120, 170],
        "Profit": [30, 40, 35, 45],
    }
).melt("Year", var_name="Type", value_name="Value")

chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(x="Year:O", y="Value:Q", color="Type:N", tooltip=["Year", "Type", "Value"])
    .properties(width=600, height=400, title="연도별 매출 및 이익")
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


# 데이터 생성
df = pd.DataFrame(
    {
        "Year": ["2020", "2021", "2022", "2023"],
        "Sales": [100, 150, 120, 170],
        "Profit": [30, 40, 35, 45],
    }
)

# 데이터 형태 변환
df_melted = df.melt("Year", var_name="Type", value_name="Value")

# Altair 차트 생성 (옵션 사용 예시)
chart = (
    alt.Chart(df_melted)
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:O", title="년도", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Value:Q", title="값"),
        color=alt.Color("Type:N", title="구분"),
        tooltip=["Year", "Type", "Value"],
    )
    .properties(width=600, height=400, title="연도별 판매액과 이익 변화")
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.title("영역 그래프 예시")

df = pd.DataFrame(
    {
        "월": range(1, 13),
        "제품A": np.random.randint(100, 300, 12),
        "제품B": np.random.randint(200, 400, 12),
    }
).set_index("월")

st.area_chart(df, use_container_width=True)


x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y1, label="sin(x)", linestyle="--", marker="o", color="blue")
ax.plot(x, y2, label="cos(x)", linestyle="-", marker="x", color="red")
ax.set_title("Matplotlib 예제")
ax.set_xlabel("X축")
ax.set_ylabel("Y축")
ax.legend()
ax.grid(True)

st.pyplot(fig)
