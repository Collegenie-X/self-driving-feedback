import streamlit as st
from my_components import checkbox_scale


def show_survey():
    with st.container():
        st.markdown(
            "<h2 style='text-align: center;'>자율 주행 시스템 만족도 조사</h2>",
            unsafe_allow_html=True,
        )

        # 응답자 정보 제목
        st.subheader("응답자 정보")
        st.divider()

        # 아이디 입력
        user_id = st.text_input(
            "ID를 입력해 주세요.",
            key="user_id",
            placeholder="예: 사용자123",
            label_visibility="collapsed",
        )

        # 나이 선택
        age = st.selectbox(
            "나이를 골라주세요.", ["10대", "20대", "30대", "40대 이상"], key="age"
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

        scale_labels = [
            "매우 불만족(1)",
            "불만족(2)",
            "보통(3)",
            "만족(4)",
            "매우 만족(5)",
        ]
        st.divider()
        st.subheader("주행 중 느낀점 (승차감 중심)")
        st.divider()

        with st.container():

            q1 = checkbox_scale(
                "Q1. 큰 도로나 고속도로 주행 시 안정감이 편안했나요?",
                scale_labels,
                "q1",
            )
            q2 = checkbox_scale(
                "Q2. 커브길 주행 시 흔들림 없이 편하게 느끼셨나요?", scale_labels, "q2"
            )
            q3 = checkbox_scale(
                "Q3. 좁은 길 주행 시 불안감 없이 안정적으로 느껴졌나요?",
                scale_labels,
                "q3",
            )
            q4 = checkbox_scale(
                "Q4. 출발/멈출 때 급하게 흔들리지 않고 자연스러웠나요?",
                scale_labels,
                "q4",
            )

        # (C) 추가로 돌발상황 대응, 자동주차 기능 등 문항을 이어서 작성하면 됨

        st.write("")
        st.divider()

        st.subheader("돌발 및 긴급 상황 대처 능력 평가")
        st.divider()

        with st.container():

            q5 = checkbox_scale(
                "Q1 갑자기 보행자나 자전거가 나타났을 때 빠르게 반응하고 잘 멈추거나 피했나요?",
                scale_labels,
                "q5",
            )
            q6 = checkbox_scale(
                "Q2. 예상 못한 앞차의 급정거 같은 긴급 상황에서 믿고 맡길 만큼 시스템이 잘 반응했나요?",
                scale_labels,
                "q6",
            )
            q7 = checkbox_scale(
                "Q3.  신호등이나 교통 표지판을 정확히 보고 잘 따르는 편인가요?",
                scale_labels,
                "q7",
            )
            q8 = checkbox_scale(
                "Q4.  비가 오거나 밤에 어두울 때도 불안감 없이 안정적으로 주행했나요?",
                scale_labels,
                "q8",
            )

        # (C) 추가로 돌발상황 대응, 자동주차 기능 등 문항을 이어서 작성하면 됨

        st.write("")
        st.divider()

        st.subheader("자동 주차 기능 평가")
        st.divider()

        with st.container():

            q9 = checkbox_scale(
                "Q1 자동 주차할 때 주차 공간을 잘 찾아서 정확히 안내했나요?",
                scale_labels,
                "q9",
            )
            q10 = checkbox_scale(
                "Q2. 자동으로 주차할 때 불안감 없이 편안하게 주차가 잘 되었나요?",
                scale_labels,
                "q10",
            )
            q11 = checkbox_scale(
                "Q3.  주차 중 주변 차량이나 기둥 같은 장애물을 잘 파악하고 안전하게 주차했나요?",
                scale_labels,
                "q11",
            )
            q12 = checkbox_scale(
                "Q4.  주차가 끝난 후 차량이 주차선 안에 바르게 정렬되었나요?",
                scale_labels,
                "q12",
            )

        # (C) 추가로 돌발상황 대응, 자동주차 기능 등 문항을 이어서 작성하면 됨

        st.write("")
        st.divider()
        st.subheader("전반적인 만족도 & 추천 의사")
        st.divider()

        with st.container():

            q13 = checkbox_scale(
                "Q1 전체적으로 자율주행 차량의 승차감이 마음에 들었나요?",
                scale_labels,
                "q13",
            )
            q14 = checkbox_scale(
                "Q2. 자율주행 차량 조작방법이나 사용법이 쉽고 간단하게 느껴졌나요?",
                scale_labels,
                "q14",
            )
            q15 = checkbox_scale(
                "Q3.  앞으로도 이 자율주행 차량을 다시 이용하고 싶나요?",
                scale_labels,
                "q15",
            )
            q16 = checkbox_scale(
                "Q4.  친구나 가족에게도 자율주행 차량을 추천할 생각이 있나요?",
                scale_labels,
                "q16",
            )

        # (C) 추가로 돌발상황 대응, 자동주차 기능 등 문항을 이어서 작성하면 됨

        st.write("")
        st.divider()
        # (D) 설문 제출 버튼
        _, col2 = st.columns([8, 1])

        if col2.button("설문 제출"):
            st.success("설문이 성공적으로 제출되었습니다.")
            # 실제로는 q1, q2 등 데이터 저장 로직(CSV/DB 등) 구현 가능
            # ex) st.session_state['survey_data'] = {...}
