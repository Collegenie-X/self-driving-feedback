import streamlit as st
from survey_part_map import show_survey
from result_part import show_result


def display_header(key_value):
    _, col2 = st.columns([7, 1])

    with col2:
        st.button("내보내기", key=f"export_{key_value}")


def main():
    st.set_page_config(page_title="자율주행 설문/결과", layout="centered")

    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1200px; /* 세미콜론(;) */
            margin: 0 auto;   /* 가운데 정렬 */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ 탭 메뉴 생성
    tabs = st.tabs(["설문 부분", "결과 부분"])

    with tabs[0]:  ## 설문 부분
        display_header("survey")
        show_survey()

    with tabs[1]:  ## 결과 부분
        display_header("result")
        show_result()


if __name__ == "__main__":
    main()
