import streamlit as st
import base64


def show_title(img_url, title):
    """
    로컬 이미지 파일을 base64로 변환하여
    중앙 정렬 + 특정 스타일로 표시하는 함수
    """

    def get_base64(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # img_url => 로컬 이미지 경로 (예: "images/autonomous_car.png")
    img_base64 = get_base64(img_url)

    st.markdown(
        f"""
        <style>
            .my-img {{
                margin-top:5px;
            }}
            p.title-text {{
                font-weight:bold;
                font-size: 28px;
                margin-left: 5px;
                margin-bottom:-20px;
            }}
        </style>

        <div align="left" style="margin-top:20px; display:flex; ">
            <img class="my-img" 
                 src="data:image/png;base64,{img_base64}" 
                 alt="로컬 이미지"
                 width=30
                 height=30>
            <p class="title-text">{title}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
