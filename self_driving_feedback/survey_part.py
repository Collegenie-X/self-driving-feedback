import streamlit as st
from my_components import checkbox_scale


def show_survey():
    st.title("자율 주행 시스템 만족도 조사")

    # (A) 응답자 정보
    st.subheader("응답자 정보")
    user_id = st.text_input("ID를 입력해 주세요.", key="user_id")
    gender = st.radio("성별을 골라주세요.", ["남성", "여성"], key="gender")
    age = st.selectbox(
        "나이를 골라주세요.", ["10대", "20대", "30대", "40대 이상"], key="age"
    )
    region = st.selectbox(
        "거주 지역을 선택하세요.",
        ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"],
        key="region",
    )

    st.write("---")

    # (B) 주행 중 느낀 점 (승차감 중심) - 예시 2문항
    st.subheader("주행 중 느낀점 (승차감 중심)")
    q1 = checkbox_scale(
        "Q1. 고속도로 주행 시 안정감(1~5)", [1, 2, 3, 4, 5], key_prefix="q1"
    )
    q2 = checkbox_scale(
        "Q2. 커브길 주행 시 안정감(1~5)", [1, 2, 3, 4, 5], key_prefix="q2"
    )

    st.write("---")
    # (C) 추가로 돌발상황 대응, 자동주차 기능 등 문항을 이어서 작성하면 됨

    # (D) 설문 제출 버튼
    if st.button("설문 제출"):
        st.success("설문이 성공적으로 제출되었습니다.")
        # 실제로는 q1, q2 등 데이터 저장 로직(CSV/DB 등) 구현 가능
        # ex) st.session_state['survey_data'] = {...}
