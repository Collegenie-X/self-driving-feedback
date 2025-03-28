import streamlit as st
import pandas as pd


def file_uploader():
    """사용자가 CSV 파일을 업로드하는 함수"""
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        return None
