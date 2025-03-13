import streamlit as st
from survey_part import show_survey
from result_part import show_result


def main():
    st.set_page_config(page_title="자율주행 설문/결과", layout="wide")

    menu = st.sidebar.selectbox("메뉴 선택", ["설문 부분", "결과 부분"])

    if menu == "설문 부분":
        show_survey()
    else:  # "결과 부분"
        show_result()


if __name__ == "__main__":
    main()
