import streamlit as st
import pandas as pd
from my_components import checkbox_scale_single, parse_scale_label


def show_survey():
    st.markdown(
        "<h2 style='text-align: center;'>자율 주행 시스템 만족도 조사</h2>",
        unsafe_allow_html=True,
    )

    # (A) 응답자 정보
    st.subheader("응답자 정보")
    st.divider()

    st.write("ID를 입력해 주세요.")
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
        max_value=100,
        value=25,
        step=1,
        key="age",
    )
    # 성별 -> True/False
    gender_str = st.radio("성별을 선택하세요.", ["남성", "여성"], key="gender")
    gender_val = True if gender_str == "남성" else False

    # 거주 지역
    region = st.selectbox(
        "거주 지역을 선택하세요.",
        ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"],
        key="region",
    )

    scale_labels = [
        "매우 불만족(1)",
        "불만족(2)",
        "보통(3)",
        "만족(4)",
        "매우 만족(5)",
    ]

    # 문항별 그룹을 리스트로 정의
    question_groups = [
        {
            "sub_title": "주행 중 느낀점 (승차감 중심)",
            "question_list": [
                ("Q1. 큰 도로나 고속도로 주행 시 안정감이 편안했나요?", "q1"),
                ("Q2. 커브길 주행 시 흔들림 없이 편하게 느끼셨나요?", "q2"),
                ("Q3. 좁은 길 주행 시 불안감 없이 안정적으로 느껴졌나요?", "q3"),
                ("Q4. 출발/멈출 때 급하게 흔들리지 않고 자연스러웠나요?", "q4"),
            ],
        },
        {
            "sub_title": "돌발 및 긴급 상황 대처 능력 평가",
            "question_list": [
                (
                    "Q5. 갑자기 보행자나 자전거가 나타났을 때 빠르게 반응하고 잘 멈추거나 피했나요?",
                    "q5",
                ),
                (
                    "Q6. 예상 못한 앞차의 급정거 같은 긴급 상황에서 믿고 맡길 만큼 시스템이 잘 반응했나요?",
                    "q6",
                ),
                ("Q7. 신호등이나 교통 표지판을 정확히 보고 잘 따르는 편인가요?", "q7"),
                (
                    "Q8. 비가 오거나 밤에 어두울 때도 불안감 없이 안정적으로 주행했나요?",
                    "q8",
                ),
            ],
        },
        {
            "sub_title": "자동 주차 기능 평가",
            "question_list": [
                ("Q9. 자동 주차할 때 주차 공간을 잘 찾아서 정확히 안내했나요?", "q9"),
                (
                    "Q10. 자동으로 주차할 때 불안감 없이 편안하게 주차가 잘 되었나요?",
                    "q10",
                ),
                (
                    "Q11. 주차 중 주변 차량이나 기둥 같은 장애물을 잘 파악하고 안전하게 주차했나요?",
                    "q11",
                ),
                ("Q12. 주차가 끝난 후 차량이 주차선 안에 바르게 정렬되었나요?", "q12"),
            ],
        },
        {
            "sub_title": "전반적인 만족도 & 추천 의사",
            "question_list": [
                ("Q13. 전체적으로 자율주행 차량의 승차감이 마음에 들었나요?", "q13"),
                (
                    "Q14. 자율주행 차량 조작방법이나 사용법이 쉽고 간단하게 느껴졌나요?",
                    "q14",
                ),
                ("Q15. 앞으로도 이 자율주행 차량을 다시 이용하고 싶나요?", "q15"),
                ("Q16. 친구나 가족에게도 자율주행 차량을 추천할 생각이 있나요?", "q16"),
            ],
        },
    ]

    # map을 사용하여 문항별 체크박스 입력
    responses = {}
    for group in question_groups:
        st.divider()
        st.subheader(group["sub_title"])
        st.divider()

        # 각 문항에 대해 checkbox_scale_single을 사용하여 응답 받기
        responses.update(
            {
                q[1]: checkbox_scale_single(q[0], scale_labels, q[1])
                for q in group["question_list"]
            }
        )

    st.divider()

    # (C) "설문 제출" 버튼 클릭 시 유효성 검사 + dict 생성
    if st.button("설문 제출"):

        # 1) 모든 문항이 선택되었는지 / 나이/성별/지역도 입력됐는지 검사
        if len(user_id) < 5:
            st.error("아이디를 5글자 이상 입력하세요.")
            return

        df = pd.read_csv("./data/survey_results.csv")
        # st.write(df["user_id"])
        for id in df["user_id"]:
            if user_id.strip().lower() == str(id).strip().lower():
                st.error(
                    f"{user_id} 아이디는 이미 존재합니다. 다시 user id를 입력해 주세요."
                )
                return

        if age < 1:
            st.error("나이를 정확히 입력하세요.")
            return

        for idx, value in enumerate(responses.values()):
            if value == None:
                st.error(f"질문 Q[{idx+1}]에 대해 체크해주세요.")
                return

        # 2) 딕셔너리로 구성
        survey_data = {
            "user_id": user_id,
            "age": int(age),
            "gender": gender_val,
            "region": region,
        }

        # 각 응답을 딕셔너리에 추가 (여기서 `value`만 저장)
        for group in question_groups:
            for q, label in zip(group["question_list"], responses.values()):
                survey_data[q[1]] = {
                    "description": q[0],
                    "value_description": label,
                    "value": parse_scale_label(label),  # value만 저장
                }

        st.success("설문이 성공적으로 제출되었습니다.")
        st.write("**[설문 결과 딕셔너리]**", survey_data)

        # CSV 저장 부분에서 value만 저장
        csv_data = {
            "user_id": user_id,
            "age": int(age),
            "gender": gender_val,
            "region": region,
            # "q1": 4,
            # "q2": 5
        }

        # 각 문항에 대해 value만 저장
        for group in question_groups:
            for q, label in zip(group["question_list"], responses.values()):
                csv_data[q[1]] = parse_scale_label(label)  # value만 저장

        # CSV가 이미 존재하는지 확인하고, 존재하면 header 없이 값만 저장
        file_path = "./data/survey_results.csv"
        if pd.io.common.file_exists(file_path):
            df = pd.DataFrame([csv_data])  # 한 사람의 결과를 데이터프레임으로 변환
            df.to_csv(
                file_path, mode="a", header=False, index=False
            )  # 헤더 없이 데이터 추가
        else:
            df = pd.DataFrame([csv_data])  # 한 사람의 결과를 데이터프레임으로 변환
            df.to_csv(
                file_path, mode="w", header=True, index=False
            )  # 헤더와 함께 첫 번째로 저장

        st.write("**CSV 파일에 저장되었습니다.**")
        st.download_button(
            label="CSV 파일 다운로드",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=file_path,
            mime="text/csv",
        )

        if st.button("설문 다시 하기 "):

            st.session_state.clear()  # 모든 값 초기화
            st.experimental_rerun()  # 페이지를 새로고침하여 초기화된 상태로 돌아가기
