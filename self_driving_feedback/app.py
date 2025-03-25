import streamlit as st
from survey_part_map_csv import show_survey
from result_part_real_new import show_result
from pdf_export import make_survey_report_pdf


def display_header(key_value):
    _, col2 = st.columns([7, 2])

    if "pdf_data" not in st.session_state:
        st.session_state["pdf_data"] = None

    with col2:

        left, right = st.columns(2)

        with left:
            if st.button("📄 내보내기", key=f"export_{key_value}"):
                pdf_data = make_survey_report_pdf()
                st.session_state["pdf_data"] = pdf_data  # 세션에 저장

        with right:
            if st.session_state["pdf_data"] is not None:
                st.download_button(
                    label="PDF 다운로드",
                    data=st.session_state["pdf_data"],
                    file_name="test_survey_report.pdf",
                    mime="application/pdf",
                    key=f"download_{key_value}",
                )


def main():
    st.set_page_config(page_title="자율주행 설문/결과", layout="centered")

    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ 탭 메뉴 생성
    tabs = st.tabs(["설문 부분", "결과 부분"])

    with tabs[0]:
        display_header("survey")
        # 설문 부분
        show_survey()

    with tabs[1]:
        display_header("result")
        # 결과 부분
        show_result()


if __name__ == "__main__":
    main()
