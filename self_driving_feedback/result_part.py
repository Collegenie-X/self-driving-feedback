import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def show_result():
    st.markdown("<h2 style='text-align:center;'> 자율 주행 시스템 만족도 분석 결과 </h2>", unsafe_allow_html=True)

    # (1) 조사 개요
    st.subheader("설문 조사 개요")
    st.write("- **설문 조사 기간**: 2025.03.14 ~ 2025.03.26 (12일간)")
    st.write("- **전체 응답자 수**: 120명")

    st.write("---")

    # (2) 응답자 특성 분석 (간단 예시)
    st.subheader("응답자 특성 분석")
    np.random.seed(42)
    ages = np.random.randint(20, 70, size=120)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(ages, bins=10, color="#4C66F5", alpha=0.7)
    ax.set_title("나이 분포")
    st.pyplot(fig)

    st.write("---")

    # (3) 만족도 분석 (예시)
    st.subheader("만족도 분석")
    # 예: 랜덤 데이터(1~5) 50개
    random_scores = np.random.randint(1, 6, size=50)
    df_score = pd.DataFrame(random_scores, columns=["Score"])
    st.bar_chart(df_score)

    # (4) 보고서 코멘트
    st.subheader("보고서 코멘트")
    comment = st.text_area("분석자가 남기는 코멘트:")
    if st.button("코멘트 저장"):
        st.success("코멘트가 저장되었습니다.")
