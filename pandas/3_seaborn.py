import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

st.title("1.산점도")
# 데이터 생성
data = pd.DataFrame({"Sales": [100, 150, 120, 170], "Profit": [30, 40, 35, 45]})

# Seaborn 산점도
fig, ax = plt.subplots()
sns.scatterplot(x="Sales", y="Profit", data=data, ax=ax)
st.pyplot(fig)


st.title("2. 히트맵")
# 데이터 생성
data = pd.DataFrame(np.random.rand(10, 12), columns=[f"Var{i}" for i in range(1, 13)])

# Seaborn 히트맵
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(data, cmap="YlGnBu", annot=True, ax=ax)
st.pyplot(fig)


st.title("3. 박스 플롯")
# 데이터 생성
data = pd.DataFrame(
    {"Category": ["A", "B", "A", "B", "A", "B"], "Value": [10, 20, 30, 40, 50, 60]}
)

# Seaborn 박스 플롯
fig, ax = plt.subplots()
sns.boxplot(x="Category", y="Value", data=data, ax=ax)
st.pyplot(fig)


st.title("4. 카운트 플롯 그래프")

# 데이터 생성
data = pd.DataFrame({"Category": ["A", "B", "A", "B", "A", "B", "B", "B"]})

# Seaborn 카운트 플롯
fig, ax = plt.subplots()
sns.countplot(x="Category", data=data, ax=ax)
st.pyplot(fig)


st.title("5. 페어플롯 (Pair Plot)")
# 데이터 생성
data = pd.DataFrame(
    {
        "Sales": [100, 150, 120, 170],
        "Profit": [30, 40, 35, 45],
        "Growth": [10, 15, 20, 25],
    }
)

# Seaborn 페어플롯
sns.pairplot(data)
st.pyplot(plt)


st.title("6. 선 그래프 (lineplot)")
# 데이터 생성
data = pd.DataFrame({"Year": [2020, 2021, 2022, 2023], "Sales": [100, 150, 120, 170]})

# Seaborn 선 그래프
fig, ax = plt.subplots()
sns.lineplot(x="Year", y="Sales", data=data, ax=ax)
st.pyplot(fig)


st.title("7. 바이올린 플롯 (violinplot) ")
data = pd.DataFrame(
    {"Category": ["A", "B", "A", "B", "A", "B"], "Value": [10, 20, 30, 40, 50, 60]}
)

# Seaborn 바이올린 플롯
fig, ax = plt.subplots()
sns.violinplot(x="Category", y="Value", data=data, ax=ax)
st.pyplot(fig)


st.title("8. 막대 그래프 (barplot)")

# 데이터 생성
data = pd.DataFrame({"Product": ["A", "B", "C", "D"], "Sales": [100, 200, 150, 250]})

# Seaborn 막대 그래프
fig, ax = plt.subplots()
sns.barplot(x="Product", y="Sales", data=data, ax=ax)
st.pyplot(fig)


st.title("9.분포 플롯 (Dist Plot)")
# 데이터 생성
data = pd.Series(np.random.randn(1000))

# Seaborn 분포 플롯
fig, ax = plt.subplots()
sns.distplot(data, ax=ax)
st.pyplot(fig)

st.title("10. 스위머 그래프 (Swarm Plot)")

# 데이터 생성
data = pd.DataFrame(
    {"Category": ["A", "B", "A", "B", "A", "B"], "Value": [10, 20, 40, 40, 50, 90]}
)

# Seaborn 스위머 그래프
fig, ax = plt.subplots()
sns.swarmplot(x="Category", y="Value", data=data, ax=ax)
st.pyplot(fig)

st.write("\n\n")
st.title("-----------------------------------------------")
st.write("\n\n")

st.title("1.다중 그래프 (Subplot)")

# 데이터 생성
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 여러 그래프를 그리기 위한 Subplot
fig, axs = plt.subplots(2, 1, figsize=(10, 6))

# 첫 번째 그래프: Sine Curve
axs[0].plot(x, y1, label="Sine")
axs[0].set_title("Sine Function")
axs[0].legend()

# 두 번째 그래프: Cosine Curve
axs[1].plot(x, y2, label="Cosine", color="r")
axs[1].set_title("Cosine Function")
axs[1].legend()

# 그래프 출력
st.pyplot(fig)


st.title("2.복잡한 히트맵 (heatmap)")
# 데이터 생성
data = np.random.rand(10, 12)
df = pd.DataFrame(data, columns=[f"Var{i}" for i in range(1, 13)])

# 히트맵 그리기
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df, cmap="YlGnBu", annot=True, ax=ax)
st.pyplot(fig)


st.title("3. heatmap 상관관계 매트릭스")

# 데이터 생성
data = pd.DataFrame(
    {
        "Sales": [100, 150, 120, 170, 130],
        "Profit": [30, 40, 35, 45, 50],
        "Advertising": [10, 15, 13, 18, 12],
        "Growth": [5, 10, 8, 12, 7],
    }
)

# 상관관계 매트릭스 생성
corr_matrix = data.corr()

# Seaborn을 사용해 상관관계 매트릭스 시각화
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, vmin=-1, vmax=1)

# 그래프 출력
st.pyplot(fig)


st.title("4.복합형 그래프 (Dual-axis Plot)")

# 데이터 생성
x = np.arange(2020, 2025)
sales = np.array([100, 150, 120, 170, 130])
profit = np.array([30, 40, 35, 45, 50])

# 복합형 그래프 (Dual-axis plot)
fig, ax1 = plt.subplots(figsize=(10, 6))

# 첫 번째 y축: Sales
ax1.plot(x, sales, color="b", label="Sales")
ax1.set_xlabel("Year")
ax1.set_ylabel("Sales", color="b")
ax1.tick_params(axis="y", labelcolor="b")

# 두 번째 y축: Profit
ax2 = ax1.twinx()
ax2.plot(x, profit, color="r", label="Profit")
ax2.set_ylabel("Profit", color="r")
ax2.tick_params(axis="y", labelcolor="r")

# 그래프 제목과 출력
plt.title("Sales and Profit Over Time")
st.pyplot(fig)


st.title("5. 복합형 산점도와 선 그래프 (Scatter + Line Plot)")
# 데이터 생성
x = np.arange(2020, 2025)
sales = np.array([100, 150, 120, 170, 130])
profit = np.array([30, 40, 35, 45, 50])

# 산점도와 선 그래프 결합
fig, ax = plt.subplots(figsize=(10, 6))

# 산점도
ax.scatter(x, sales, color="b", label="Sales", zorder=5)

# 선 그래프
ax.plot(x, profit, color="r", label="Profit", linestyle="--", zorder=2)

# 그래프 레이블 설정
ax.set_xlabel("Year")
ax.set_ylabel("Value")
ax.set_title("Sales vs Profit")
ax.legend()

# 그래프 출력
st.pyplot(fig)

st.title("7.서브 플롯으로 다중 카테고리 비교")
# 데이터 생성
categories = ["A", "B", "C", "D"]
values1 = [100, 200, 150, 250]
values2 = [50, 80, 60, 90]

# 서브 플롯을 사용하여 카테고리 비교
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# 첫 번째 플롯: 막대 그래프
axs[0].bar(categories, values1, color="b")
axs[0].set_title("Category Comparison 1")

# 두 번째 플롯: 막대 그래프
axs[1].bar(categories, values2, color="r")
axs[1].set_title("Category Comparison 2")

# 그래프 출력
st.pyplot(fig)
