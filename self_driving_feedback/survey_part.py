import streamlit as st
from my_components import checkbox_scale


def show_survey():
    with st.container():
        st.markdown("<h2 style='text-align: center;'>자율 주행 시스템 만족도 조사</h2>", unsafe_allow_html=True)
        
        # 응답자 정보 제목
        st.subheader("응답자 정보", anchor="A")
        
        # 아이디 입력
        user_id = st.text_input("ID를 입력해 주세요.", key="user_id", placeholder="예: 사용자123", label_visibility="collapsed")
        
        # 나이 선택
        age = st.selectbox(
            "나이를 골라주세요.", 
            ["10대", "20대", "30대", "40대 이상"], 
            key="age"
        )

        # 성별 선택
        gender = st.radio("성별을 선택하세요.", ["남성", "여성"], key="gender")

        # 거주 지역 선택
        region = st.selectbox(
            "거주 지역을 선택하세요.",
            ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"],
            key="region",
        )

        # 컨테이너에 스타일 추가 (너비 조정)
       
    st.divider()

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
