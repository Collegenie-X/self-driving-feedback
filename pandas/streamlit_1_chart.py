import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 한글 폰트 설정 (Ubuntu 서버 등에서 나눔 폰트 설치 필요)
rcParams["font.family"] = "AppleGothic"
rcParams["axes.unicode_minus"] = False

st.title("📊 다양한 차트 시각화 (Streamlit)")

# 사이드바 메뉴로 차트 선택
chart_menu = st.sidebar.selectbox(
    "차트 유형을 선택하세요",
    ["선 그래프", "막대 그래프", "영역 그래프", "히스토그램", "산점도"],
)

# 공통 데이터 생성
x = np.arange(0, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

# 1. 선 그래프
if chart_menu == "선 그래프":
    st.subheader("🔹 선 그래프")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y1, label="sin(x)", marker="o")
    ax.plot(x, y2, label="cos(x)", marker="x")
    ax.set_title("sin(x) 및 cos(x) 선 그래프")
    ax.set_xlabel("X축")
    ax.set_ylabel("Y축")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# 2. 막대 그래프
elif chart_menu == "막대 그래프":
    st.subheader("🔸 막대 그래프")

    data = pd.DataFrame({"Category": ["A", "B", "C", "D"], "Value": [23, 45, 56, 78]})
    st.bar_chart(data.set_index("Category"))

    st.write("Matplotlib로 표현한 막대 그래프")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(data["Category"], data["Value"], color="skyblue")
    ax.set_title("카테고리별 값 비교")
    ax.set_xlabel("카테고리")
    ax.set_ylabel("값")
    ax.grid(axis="y")

    st.pyplot(fig)

# 3. 영역 그래프
elif chart_menu == "영역 그래프":
    st.subheader("🔺 영역 그래프")

    df_area = pd.DataFrame({"sin(x)": y1, "cos(x)": y2}, index=x)
    st.area_chart(df_area)

# 4. 히스토그램
elif chart_menu == "히스토그램":
    st.subheader("📈 히스토그램")

    data = np.random.randn(1000)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(data, bins=30, color="purple", alpha=0.7)
    ax.set_title("정규 분포 히스토그램")
    ax.set_xlabel("값")
    ax.set_ylabel("빈도")
    ax.grid(True)

    st.pyplot(fig)

# 5. 산점도
elif chart_menu == "산점도":
    st.subheader("⚫ 산점도")

    df_scatter = pd.DataFrame(
        {
            "X값": np.random.rand(100),
            "Y값": np.random.rand(100),
            "크기": np.random.rand(100) * 200,
            "색상": np.random.rand(100),
        }
    )

    scatter_chart = (
        alt.Chart(df_scatter)
        .mark_circle()
        .encode(
            x="X값",
            y="Y값",
            size="크기",
            color="색상",
            tooltip=["X값", "Y값", "크기"],
        )
        .properties(title="산점도 시각화")
        .interactive()
    )

    st.altair_chart(scatter_chart, use_container_width=True)
