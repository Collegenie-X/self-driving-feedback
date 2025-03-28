import streamlit as st
import base64







def show_title(img_url, title) : 

    def get_base64(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()


    st.markdown(
        f"""
        <style>
            .my-img {{
                border-radius: 20px;
                box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
            }}
        </style>

        <div align="center">
            <img class="my-img" src="data:image/png;base64,{get_base64(img_url)}" alt="로컬 이미지">
            <p style="font-size:16px;">{title}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
