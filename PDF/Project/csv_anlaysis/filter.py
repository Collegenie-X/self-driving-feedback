import streamlit as st
import pandas as pd


def filter_data(df, selected_column):
    """선택된 열을 기준으로 데이터를 필터링하는 함수"""
    if pd.api.types.is_numeric_dtype(
        df[selected_column]
    ):  # 숫자형 데이터에 대해서만 필터링
        filter_value = st.slider(
            f"{selected_column} 값 필터링",
            min_value=float(df[selected_column].min()),
            max_value=float(df[selected_column].max()),
            value=(float(df[selected_column].min()), float(df[selected_column].max())),
        )
        filtered_df = df[
            (df[selected_column] >= filter_value[0])
            & (df[selected_column] <= filter_value[1])
        ]
    else:
        filtered_df = df  # 문자열 데이터의 경우 필터링하지 않음
    return filtered_df
