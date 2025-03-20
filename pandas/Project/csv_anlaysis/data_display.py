import streamlit as st


def display_data_preview(df):
    """업로드된 데이터의 미리보기를 출력하는 함수"""
    st.write("### 데이터 미리보기")
    st.write(df.head())  # 상위 5개 행을 표시


def display_statistics(df):
    """업로드된 데이터의 기술 통계를 출력하는 함수"""
    st.write("### 데이터 통계")
    st.write(df.describe())  # 기술 통계 출력
