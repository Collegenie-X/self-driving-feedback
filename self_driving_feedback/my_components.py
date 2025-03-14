import streamlit as st


def checkbox_scale(question_text, scale_values, key_prefix):
    """
    (예시) 체크박스로 1~5 중 하나 이상 선택하도록 하는 컴포넌트.
    - question_text: 문항 질문 텍스트
    - scale_values: 표시할 체크박스 값 예: [1,2,3,4,5]
    - key_prefix: 세션 키 식별용 prefix (문항별로 고유)
    반환값: 사용자가 체크한 항목(리스트)
    """
    col1, col2 = st.columns([3, 5])

    col1.write(question_text)
    selected = []
    list_cols = col2.columns([1, 1, 1, 1, 1])

    for idx, val in enumerate(scale_values):
        # 체크박스
        if list_cols[idx].checkbox(str(val), key=f"{key_prefix}_{val}"):
            selected.append(val)
    return selected
