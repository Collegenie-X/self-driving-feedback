import streamlit as st


def download_filtered_data(filtered_df):
    """분석된 데이터를 CSV 파일로 다운로드하는 함수"""
    st.write("### 분석된 데이터 다운로드")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "CSV 파일로 다운로드",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv",
    )
