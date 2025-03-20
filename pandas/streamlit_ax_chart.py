import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 6))

# 선 그래프
ax.plot(x, y1, label="sin(x)", linestyle="--", marker="o", color="blue")
ax.plot(x, y2, label="cos(x)", linestyle="-", marker="x", color="red")

# 차트 옵션들
ax.set_title("사인 & 코사인 그래프", fontsize=16, fontweight="bold")
ax.set_xlabel("X축", fontsize=14)
ax.set_ylabel("Y축", fontsize=14)
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
ax.legend(loc="upper right", fontsize=12)

# 눈금 설정 및 회전
ax.set_xticks(np.arange(0, 11, 1))
ax.tick_params(axis="x", rotation=45)

# 주석 추가
ax.annotate(
    "sin(x) 최대",
    xy=(np.pi / 2, 1),
    xytext=(np.pi / 2, 1.2),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
)

# 배경색
ax.set_facecolor("#f5f5f5")

# Streamlit 출력
st.pyplot(fig)


st.title("📈 선 그래프 - 예시 1")

# 데이터 생성
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 차트 생성
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(x, y1, label="sin(x)", color="blue", linestyle="--", marker="o", linewidth=2)
ax.plot(x, y2, label="cos(x)", color="red", linestyle="-", marker="x", linewidth=2)

# 차트 옵션
ax.set_title("사인과 코사인 함수 비교", fontsize=16, fontweight="bold")
ax.set_xlabel("X 값", fontsize=14)
ax.set_ylabel("Y 값", fontsize=14)
ax.legend(loc="upper right")
ax.grid(True, linestyle=":", linewidth=0.7, alpha=0.8)

# 눈금 회전 및 범위 설정
ax.set_xticks(np.arange(0, 11, 1))
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# Streamlit 출력
st.pyplot(fig)


st.title("📈 선 그래프 - 예시 2")

x = np.linspace(0, 10, 100)
y1 = np.sin(x)

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(x, y1, label="sin(x)", color="purple", marker="d", linewidth=2)

# 주석 추가
ax.annotate(
    "최대값",
    xy=(np.pi / 2, 1),
    xytext=(np.pi / 2, 1.2),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=12,
)

# 배경색, 격자 스타일
ax.set_facecolor("#f0f0f0")
ax.grid(True, linestyle="--", alpha=0.5)

ax.set_title("sin(x) 함수와 주석 표시", fontsize=16)
ax.set_xlabel("X")
ax.set_ylabel("sin(x)")
ax.legend()

st.pyplot(fig)


st.title("📊 막대 그래프 - 예시 1")

categories = ["A", "B", "C", "D"]
values = [23, 45, 56, 78]

fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(categories, values, color="skyblue", edgecolor="black")

ax.set_title("카테고리별 값", fontsize=16)
ax.set_xlabel("카테고리", fontsize=14)
ax.set_ylabel("값", fontsize=14)
ax.grid(True, axis="y", linestyle="--", alpha=0.7)

# 각 막대 위에 값 표시
for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        fontsize=10,
    )

st.pyplot(fig)


st.title("📊 막대 그래프 - 예시 2 (수평 그래프)")

categories = ["Apple", "Banana", "Cherry", "Date"]
values = [50, 30, 40, 20]

fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.barh(categories, values, color=["red", "yellow", "pink", "brown"])

ax.set_title("과일 판매량", fontsize=16)
ax.set_xlabel("판매 수량", fontsize=14)
ax.set_ylabel("과일 종류", fontsize=14)
ax.grid(True, axis="x", linestyle=":", alpha=0.7)

# 값 표시
for bar in bars:
    width = bar.get_width()
    ax.annotate(
        f"{width}",
        xy=(width, bar.get_y() + bar.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
    )

st.pyplot(fig)


st.title("🟢 영역 그래프 - 예시 1")

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 6))

ax.fill_between(x, y1, color="blue", alpha=0.3, label="sin(x)")
ax.fill_between(x, y2, color="red", alpha=0.3, label="cos(x)")

ax.set_title("sin(x) & cos(x) 영역 그래프", fontsize=16)
ax.set_xlabel("X축")
ax.set_ylabel("Y축")
ax.legend()
ax.grid(True)

st.pyplot(fig)


st.title("🟢 영역 그래프 - 예시 2 (누적 그래프)")

x = np.linspace(0, 10, 100)
y1 = np.abs(np.sin(x))
y2 = np.abs(np.cos(x))

fig, ax = plt.subplots(figsize=(10, 6))

ax.stackplot(x, y1, y2, labels=["sin(x)", "cos(x)"], colors=["skyblue", "lightgreen"])

ax.set_title("누적 영역 그래프", fontsize=16)
ax.set_xlabel("X")
ax.set_ylabel("값")
ax.legend(loc="upper right")
ax.grid(True, linestyle="--")

st.pyplot(fig)


st.title("📊 히스토그램 - 예시 1")

data = np.random.randn(1000)

fig, ax = plt.subplots(figsize=(8, 6))

ax.hist(data, bins=30, color="purple", alpha=0.7, density=True)
ax.set_title("정규분포 히스토그램", fontsize=16)
ax.set_xlabel("값")
ax.set_ylabel("밀도")
ax.grid(True)

st.pyplot(fig)


st.title("📊 히스토그램 - 예시 2 (다중 데이터)")

data1 = np.random.randn(1000)
data2 = np.random.randn(1000) + 2  # 이동한 정규분포

fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(data1, bins=30, alpha=0.5, label="데이터1")
ax.hist(data2, bins=30, alpha=0.5, label="데이터2")
ax.set_title("두 데이터 분포 비교", fontsize=16)
ax.set_xlabel("값")
ax.set_ylabel("빈도")
ax.legend()
ax.grid(True)

st.pyplot(fig)


st.title("⚫ 산점도 - 예시 1")

x = np.random.rand(100)
y = np.random.rand(100)
sizes = np.random.rand(100) * 500
colors = np.random.rand(100)

fig, ax = plt.subplots(figsize=(8, 6))

scatter = ax.scatter(x, y, s=sizes, c=colors, cmap="viridis", alpha=0.7)
ax.set_title("랜덤 산점도")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)

fig.colorbar(scatter)

st.pyplot(fig)


st.title("⚫ 산점도 - 예시 2 (그룹별)")

np.random.seed(0)
group1_x = np.random.rand(50)
group1_y = np.random.rand(50)

group2_x = np.random.rand(50)
group2_y = np.random.rand(50)

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(group1_x, group1_y, color="blue", label="Group 1", alpha=0.6)
ax.scatter(group2_x, group2_y, color="red", label="Group 2", alpha=0.6)

ax.set_title("그룹별 산점도")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
ax.grid(True)

st.pyplot(fig)
