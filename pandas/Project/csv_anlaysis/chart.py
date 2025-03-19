import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 한글 폰트 설정 (matplotlib)
matplotlib.rcParams["font.family"] = "AppleGothic"  # Mac 사용 시
# Windows의 경우 아래 코드 사용
# matplotlib.rcParams['font.family'] = 'Malgun Gothic'

# 그래프에서 한글 깨짐 방지 (matplotlib)
matplotlib.rcParams["axes.unicode_minus"] = False


def plot_histogram(df, selected_column):
    """선택된 열에 대한 히스토그램을 시각화하는 함수"""
    st.write("### 선택된 열에 대한 차트 시각화")
    fig, ax = plt.subplots()
    sns.histplot(df[selected_column], kde=True, ax=ax)
    ax.set_title(f"{selected_column}의 히스토그램")  # 한글 제목 지원
    st.pyplot(fig)


def plot_bar_chart(df, bar_column):
    """다른 열에 대한 막대 차트를 시각화하는 함수"""
    st.write("### 다른 열에 대한 막대 차트")
    bar_fig, bar_ax = plt.subplots()
    sns.countplot(x=bar_column, data=df, ax=bar_ax)
    bar_ax.set_title(f"{bar_column}에 대한 막대 차트")  # 한글 제목 지원
    st.pyplot(bar_fig)
