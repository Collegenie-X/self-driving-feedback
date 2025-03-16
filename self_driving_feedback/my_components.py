import streamlit as st
import re


def parse_scale_label(label):
    """
    체크박스 라벨 (ex: "매우 불만족(1)")에서 숫자(int)만 추출하여 반환.
    - label: "매우 만족(5)"와 같이 괄호 안에 숫자가 들어있는 문자열
    - return: 5 (int), 만약 찾지 못하면 None
    """
    match = re.search(r"\((\d+)\)", label)
    if match:
        return int(match.group(1))
    else:
        return None


def checkbox_scale_single(question_text, scale_values, key_prefix):
    """
    [단일 선택] 체크박스 컴포넌트.
    - question_text: 문항 질문 텍스트
    - scale_values: 표시할 체크박스 라벨 목록 (예: ["매우 불만족(1)", ...])
    - key_prefix: 세션 키 prefix

    반환값: 사용자가 체크한 라벨(문자열) 또는 None
    """
    if f"{key_prefix}_selected" not in st.session_state:
        st.session_state[f"{key_prefix}_selected"] = None

    # 레이아웃: 왼쪽(질문), 오른쪽(체크박스들)
    col1, col2 = st.columns([3, 5])
    col1.write(question_text)

    # 체크박스들이 들어갈 열 (5항목 기준)
    list_cols = col2.columns([1, 1, 1, 1, 1])

    for idx, val in enumerate(scale_values):
        default_checked = st.session_state[f"{key_prefix}_selected"] == val
        list_cols[idx].checkbox(
            str(val),
            key=f"{key_prefix}_{val}",
            value=default_checked,
            on_change=_on_change_checkbox_single,
            args=(val, scale_values, key_prefix),
        )

    return st.session_state[f"{key_prefix}_selected"]


def _on_change_checkbox_single(val, scale_values, key_prefix):
    """
    체크박스가 클릭될 때(ON/OFF) 호출되는 콜백.
    """
    is_checked = st.session_state[f"{key_prefix}_{val}"]
    if is_checked:
        # 새로 체크된 항목을 session_state에 저장
        st.session_state[f"{key_prefix}_selected"] = val
        # 다른 항목은 해제
        for v in scale_values:
            if v != val:
                st.session_state[f"{key_prefix}_{v}"] = False
    else:
        # 체크 해제됐을 때
        any_other_checked = False
        for v in scale_values:
            if st.session_state.get(f"{key_prefix}_{v}", False):
                st.session_state[f"{key_prefix}_selected"] = v
                any_other_checked = True
                break
        if not any_other_checked:
            st.session_state[f"{key_prefix}_selected"] = None
