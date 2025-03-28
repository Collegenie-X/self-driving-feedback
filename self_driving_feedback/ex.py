import streamlit as st
import base64


def get_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


img_base64 = get_base64("local_image.png")

st.markdown(
    f"""
    <style>
        .my-img {{
            border-radius: 20px;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        }}
    </style>

    <div align="center">
        <img class="my-img" src="data:image/png;base64,{img_base64}" alt="로컬 이미지">
    </div>
""",
    unsafe_allow_html=True,
)
