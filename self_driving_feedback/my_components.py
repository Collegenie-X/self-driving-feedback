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

    #### print("-----------------------------------------------")
    #### print("key_prefix:", key_prefix)
    #### print()
    #### print("question_text:", question_text)
    #### print()
    #### # for q in st.session_state:
    #### #     print(f"{q}: {st.session_state[q]}")
    #### print("-----------------------------------------------")

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


def print_session_state_table(key_prefix):
    """
    key_prefix 관련된 session_state 값을 표 형식으로 출력.
    """
    header = f"{'키':<30} | {'값':<10}"
    separator = "-" * 45
    print(separator)
    print(header)
    print(separator)
    for key, value in st.session_state.items():
        if key.startswith(key_prefix):
            print(f"{key:<30} | {str(value):<10}")
    print(separator)


# 예시로 _on_change_checkbox_single 콜백 내에서 사용
def _on_change_checkbox_single(val, scale_values, key_prefix):
    print("=== 콜백 호출 전 상태 (표 형식) ===")
    print_session_state_table(key_prefix)

    is_checked = st.session_state[f"{key_prefix}_{val}"]
    if is_checked:
        st.session_state[f"{key_prefix}_selected"] = val
        for v in scale_values:
            if v != val:
                st.session_state[f"{key_prefix}_{v}"] = False
    else:
        any_other_checked = False
        for v in scale_values:
            if st.session_state.get(f"{key_prefix}_{v}", False):
                st.session_state[f"{key_prefix}_selected"] = v
                any_other_checked = True
                break
        if not any_other_checked:
            st.session_state[f"{key_prefix}_selected"] = None

    print("=== 콜백 호출 후 상태 (표 형식) ===")
    print_session_state_table(key_prefix)
