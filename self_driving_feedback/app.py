import streamlit as st
from survey_part_map_csv import show_survey
from result_part import show_result


def main():
    st.set_page_config(page_title="자율주행 설문/결과", layout="centered")

    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1100px; /* 세미콜론(;) */
            margin: 0 auto;   /* 가운데 정렬 */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ 탭 메뉴 생성
    tabs = st.tabs(["설문 부분", "결과 부분"])

    with tabs[0]:
        # 미리보기, 내보내기 버튼 (위치 조정 가능)

        col1, col2, col3 = st.columns([7, 1, 1])

        with col2:
            st.button("미리보기", key="preview_survey")

        with col3:
            st.button("내보내기", key="export_survey")

        # 설문 부분
        show_survey()

    with tabs[1]:

        col1, col2, col3 = st.columns([7, 1, 1])

        with col2:
            st.button("미리보기", key="preview_result")

        with col3:
            st.button("내보내기", key="export_result")

        # 결과 부분
        show_result()


if __name__ == "__main__":
    main()
