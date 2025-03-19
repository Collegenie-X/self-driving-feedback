import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 생성
data = pd.DataFrame({"Year": [2020, 2021, 2022, 2023], "Sales": [100, 150, 120, 170]})

st.title("1.Matplotlib로 선 그래프 그리기")
# Matplotlib로 선 그래프 그리기
fig, ax = plt.subplots()
ax.plot(data["Year"], data["Sales"], marker="o")
st.pyplot(fig)


st.title("2.Matplotlib로 막대 그래프 그리기")
# 데이터 생성
data = pd.DataFrame({"Product": ["A", "B", "C", "D"], "Sales": [100, 200, 150, 250]})

# Matplotlib로 막대 그래프 그리기
fig, ax = plt.subplots()
ax.bar(data["Product"], data["Sales"])
st.pyplot(fig)


st.title("3.Matplotlib로 히스토그램 그리기")
# 데이터 생성
data = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5])

# 히스토그램 그리기
fig, ax = plt.subplots()
ax.hist(data, bins=5)
st.pyplot(fig)


st.title("4.Matplotlib로 산점도 그리기")
# 데이터 생성
data = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50]})

# 산점도 그리기
fig, ax = plt.subplots()
ax.scatter(data["X"], data["Y"])
st.pyplot(fig)


st.title("5.박스 플롯 (Box Plot)")
# 데이터 생성
data = pd.DataFrame(
    {"Category": ["A", "B", "A", "B", "A", "B"], "Value": [10, 20, 30, 40, 50, 60]}
)

# 박스 플롯 그리기
fig, ax = plt.subplots()
ax.boxplot(
    [data[data["Category"] == "A"]["Value"], data[data["Category"] == "B"]["Value"]]
)
st.pyplot(fig)


st.title("6.파이 차트(Pie)")
# 데이터 생성
data = pd.Series([10, 20, 30, 40])

# 파이 차트 그리기
fig, ax = plt.subplots()
ax.pie(data, labels=["A", "B", "C", "D"], autopct="%1.1f%%")
st.pyplot(fig)


st.title("7. 선 그래프 그리기(멀티)")
# 데이터 생성
data = pd.DataFrame(
    {
        "Year": [2020, 2021, 2022, 2023],
        "Sales": [100, 150, 120, 170],
        "Profit": [30, 50, 40, 60],
    }
)

# 선 그래프 그리기
fig, ax = plt.subplots()
ax.plot(data["Year"], data["Sales"], label="Sales")
ax.plot(data["Year"], data["Profit"], label="Profit")
ax.legend()
st.pyplot(fig)

import numpy as np

st.title("8. 밀도 그래프 (Density Plot)")
# 데이터 생성
data = pd.Series(np.random.randn(1000))

# 밀도 그래프 그리기
fig, ax = plt.subplots()
ax.hist(data, bins=30, density=True)
st.pyplot(fig)


st.title("9. 스택형 선 그래프")

# 데이터 생성
data = pd.DataFrame(
    {
        "Year": [2020, 2021, 2022, 2023],
        "Sales": [100, 150, 120, 170],
        "Profit": [30, 40, 35, 45],
    }
)

# 스택형 선 그래프
fig, ax = plt.subplots()
ax.stackplot(data["Year"], data["Sales"], data["Profit"], labels=["Sales", "Profit"])
ax.legend(loc="upper left")
st.pyplot(fig)
