import streamlit as st
from my_components import checkbox_scale_single, parse_scale_label


def show_survey():
    st.markdown(
        "<h2 style='text-align: center;'>자율 주행 시스템 만족도 조사</h2>",
        unsafe_allow_html=True,
    )

    # (A) 응답자 정보
    st.subheader("응답자 정보")
    st.divider()

    st.write("**ID를 입력해 주세요.**")

    user_id = st.text_input(
        label="ID를 입력해 주세요.",
        key="user_id",
        placeholder="예: niecut79 (중복 설문을 방지하기 위함입니다.)",
        label_visibility="collapsed",
    )

    # 나이 (숫자 입력) -> 예: 28
    age = st.number_input(
        "나이를 입력하세요",
        min_value=1,
        max_value=65,
        value=31,
        step=1,
        key="age",
    )
    # 성별 -> True/False
    gender_str = st.radio("성별을 선택하세요.", ["남성", "여성"], key="gender")
    gender_val = True if gender_str == "남성" else False

    # 거주 지역
    region = st.selectbox(
        "거주 지역을 선택하세요.",
        ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원", "제주"],
        key="region",
    )

    scale_labels = [
        "매우 불만족(1)",
        "불만족(2)",
        "보통(3)",
        "만족(4)",
        "매우 만족(5)",
    ]

    # (B) 문항별 체크박스 입력 (예: Q1~Q16)
    # 주행 중 느낀점
    st.divider()
    st.subheader("주행 중 느낀점 (승차감 중심)")
    st.divider()

    q1_label = checkbox_scale_single(
        "Q1. 큰 도로나 고속도로 주행 시 안정감이 편안했나요?",
        scale_labels,
        "q1",
    )
    q2_label = checkbox_scale_single(
        "Q2. 커브길 주행 시 흔들림 없이 편하게 느끼셨나요?",
        scale_labels,
        "q2",
    )
    q3_label = checkbox_scale_single(
        "Q3. 좁은 길 주행 시 불안감 없이 안정적으로 느껴졌나요?",
        scale_labels,
        "q3",
    )
    q4_label = checkbox_scale_single(
        "Q4. 출발/멈출 때 급하게 흔들리지 않고 자연스러웠나요?",
        scale_labels,
        "q4",
    )

    st.divider()
    st.subheader("돌발 및 긴급 상황 대처 능력 평가")
    st.divider()

    q5_label = checkbox_scale_single(
        "Q5. 갑자기 보행자나 자전거가 나타났을 때 빠르게 반응하고 잘 멈추거나 피했나요?",
        scale_labels,
        "q5",
    )
    q6_label = checkbox_scale_single(
        "Q6. 예상 못한 앞차의 급정거 같은 긴급 상황에서 믿고 맡길 만큼 시스템이 잘 반응했나요?",
        scale_labels,
        "q6",
    )
    q7_label = checkbox_scale_single(
        "Q7. 신호등이나 교통 표지판을 정확히 보고 잘 따르는 편인가요?",
        scale_labels,
        "q7",
    )
    q8_label = checkbox_scale_single(
        "Q8. 비가 오거나 밤에 어두울 때도 불안감 없이 안정적으로 주행했나요?",
        scale_labels,
        "q8",
    )

    st.divider()
    st.subheader("자동 주차 기능 평가")
    st.divider()

    q9_label = checkbox_scale_single(
        "Q9. 자동 주차할 때 주차 공간을 잘 찾아서 정확히 안내했나요?",
        scale_labels,
        "q9",
    )
    q10_label = checkbox_scale_single(
        "Q10. 자동으로 주차할 때 불안감 없이 편안하게 주차가 잘 되었나요?",
        scale_labels,
        "q10",
    )
    q11_label = checkbox_scale_single(
        "Q11. 주차 중 주변 차량이나 기둥 같은 장애물을 잘 파악하고 안전하게 주차했나요?",
        scale_labels,
        "q11",
    )
    q12_label = checkbox_scale_single(
        "Q12. 주차가 끝난 후 차량이 주차선 안에 바르게 정렬되었나요?",
        scale_labels,
        "q12",
    )

    st.divider()
    st.subheader("전반적인 만족도 & 추천 의사")
    st.divider()

    q13_label = checkbox_scale_single(
        "Q13. 전체적으로 자율주행 차량의 승차감이 마음에 들었나요?",
        scale_labels,
        "q13",
    )
    q14_label = checkbox_scale_single(
        "Q14. 자율주행 차량 조작방법이나 사용법이 쉽고 간단하게 느껴졌나요?",
        scale_labels,
        "q14",
    )
    q15_label = checkbox_scale_single(
        "Q15. 앞으로도 이 자율주행 차량을 다시 이용하고 싶나요?",
        scale_labels,
        "q15",
    )
    q16_label = checkbox_scale_single(
        "Q16. 친구나 가족에게도 자율주행 차량을 추천할 생각이 있나요?",
        scale_labels,
        "q16",
    )

    st.divider()

    # (C) "설문 제출" 버튼 클릭 시 유효성 검사 + dict 생성
    if st.button("설문 제출"):
        # 1) 모든 문항이 선택되었는지 / 나이/성별/지역도 입력됐는지 검사
        # age>0, gender, region != "" (이 부분은 selectbox, radio 등으로 항상 선택하긴 하지만)
        # 각 qX_label != None
        question_labels = [
            q1_label,
            q2_label,
            q3_label,
            q4_label,
            q5_label,
            q6_label,
            q7_label,
            q8_label,
            q9_label,
            q10_label,
            q11_label,
            q12_label,
            q13_label,
            q14_label,
            q15_label,
            q16_label,
        ]

        if len(user_id) < 5:
            st.error("아이디를 5글자 이상 입력하세요.")
            return

        if age < 1:
            st.error("나이를 정확히 입력하세요.")
            return

        if None in question_labels:
            st.error("모든 질문(Q1~Q16)에 대해 체크해주세요.")
            return

        list_description_values = ["매우 불만족", "불만족", "보통", "만족", "매우 마족"]

        # 2) 딕셔너리로 구성
        #  - age: 정수
        #  - gender: Boolean
        #  - region: 문자열
        #  - q1~q16: 정수 (1~5) -> parse_scale_label() 사용
        #  - age: 정수
        #  - gender: Boolean
        #  - region: 문자열
        #  - q1~q16: 설명(description)과 값(value) 포함
        survey_data = {
            "user_id": user_id,
            "age": int(age),
            "gender": gender_val,
            "region": region,
            "q1": {
                "description": "큰 도로나 고속도로 주행 시 안정감이 편안했나요?",
                "value_description": q1_label,
                "value": parse_scale_label(q1_label),
            },
            "q2": {
                "description": "커브길 주행 시 흔들림 없이 편하게 느끼셨나요?",
                "value_description": q2_label,
                "value": parse_scale_label(q2_label),
            },
            "q3": {
                "description": "좁은 길 주행 시 불안감 없이 안정적으로 느껴졌나요?",
                "value_description": q3_label,
                "value": parse_scale_label(q3_label),
            },
            "q4": {
                "description": "출발/멈출 때 급하게 흔들리지 않고 자연스러웠나요?",
                "value_description": q4_label,
                "value": parse_scale_label(q4_label),
            },
            "q5": {
                "description": "갑자기 보행자나 자전거가 나타났을 때 빠르게 반응하고 잘 멈추거나 피했나요?",
                "value_description": q5_label,
                "value": parse_scale_label(q5_label),
            },
            "q6": {
                "description": "예상 못한 앞차의 급정거 같은 긴급 상황에서 믿고 맡길 만큼 시스템이 잘 반응했나요?",
                "value_description": q6_label,
                "value": parse_scale_label(q6_label),
            },
            "q7": {
                "description": "신호등이나 교통 표지판을 정확히 보고 잘 따르는 편인가요?",
                "value_description": q7_label,
                "value": parse_scale_label(q7_label),
            },
            "q8": {
                "description": "비가 오거나 밤에 어두울 때도 불안감 없이 안정적으로 주행했나요?",
                "value_description": q8_label,
                "value": parse_scale_label(q8_label),
            },
            "q9": {
                "description": "자동 주차할 때 주차 공간을 잘 찾아서 정확히 안내했나요?",
                "value_description": q9_label,
                "value": parse_scale_label(q9_label),
            },
            "q10": {
                "description": "자동으로 주차할 때 불안감 없이 편안하게 주차가 잘 되었나요?",
                "value_description": q10_label,
                "value": parse_scale_label(q10_label),
            },
            "q11": {
                "description": "주차 중 주변 차량이나 기둥 같은 장애물을 잘 파악하고 안전하게 주차했나요?",
                "value_description": q11_label,
                "value": parse_scale_label(q11_label),
            },
            "q12": {
                "description": "주차가 끝난 후 차량이 주차선 안에 바르게 정렬되었나요?",
                "value_description": q12_label,
                "value": parse_scale_label(q12_label),
            },
            "q13": {
                "description": "전체적으로 자율주행 차량의 승차감이 마음에 들었나요?",
                "value_description": q13_label,
                "value": parse_scale_label(q13_label),
            },
            "q14": {
                "description": "자율주행 차량 조작방법이나 사용법이 쉽고 간단하게 느껴졌나요?",
                "value_description": q14_label,
                "value": parse_scale_label(q14_label),
            },
            "q15": {
                "description": "앞으로도 이 자율주행 차량을 다시 이용하고 싶나요?",
                "value_description": q15_label,
                "value": parse_scale_label(q15_label),
            },
            "q16": {
                "description": "친구나 가족에게도 자율주행 차량을 추천할 생각이 있나요?",
                "value_description": q16_label,
                "value": parse_scale_label(q16_label),
            },
        }

        st.success("설문이 성공적으로 제출되었습니다.")
        st.write("**[설문 결과 딕셔너리]**", survey_data)

        if st.button("설문 다시 하기 "):

            st.session_state.clear()  # 모든 값 초기화
            st.experimental_rerun()  # 페이지를 새로고침하여 초기화된 상태로 돌아가기
