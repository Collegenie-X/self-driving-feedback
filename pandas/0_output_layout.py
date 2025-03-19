import streamlit as st


st.title("여러 컬럼 사용 (Columns)")
# 두 개의 컬럼 사용
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    name = st.text_input("이름을 입력하세요:")
    age = st.number_input("나이를 입력하세요:", min_value=0, max_value=100)

with col2:
    gender = st.radio("성별을 선택하세요", ["남성", "여성"])
    city = st.selectbox("거주 도시를 선택하세요", ["서울", "부산", "대구", "광주"])

with col3:
    st.write("col3입니다.")
st.write(f"입력한 이름: {name}, 나이: {age}, 성별: {gender}, 도시: {city}")


st.write("----------------------------------------")


st.title("Expander로 내용 숨기기 (Expandable)")

# Expander 사용
with st.expander("추가 옵션을 보기"):
    color = st.radio("색을 선택하세요", ["빨강", "파랑", "초록"])
    size = st.selectbox("사이즈를 선택하세요", ["S", "M", "L"])
    st.write(f"선택한 색상: {color}, 사이즈: {size}")


st.write("----------------------------------------")


st.title("수평 배치 (Horizontal Form)")

# 수평 폼 배치
with st.form("my_form"):
    name = st.text_input("이름을 입력하세요:")
    age = st.number_input("나이를 입력하세요:", min_value=0, max_value=100)
    submit_button = st.form_submit_button(label="제출")

if submit_button:
    st.write(f"입력한 이름: {name}, 나이: {age}")


st.write("----------------------------------------")


st.title("Markdown 부분 ")

st.markdown("### 제목 (Markdown 사용)")
st.markdown("**굵은 텍스트**와 *기울어진 텍스트*")
st.markdown("> 제목")


st.markdown(
    '<p style="color: red"> 이 텍스트는 빨간색입니다. </p>', unsafe_allow_html=True
)
