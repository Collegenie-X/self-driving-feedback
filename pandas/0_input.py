import streamlit as st

####  제목 추가
st.title("텍스트 입력 (Text Input)")

####  텍스트 입력
user_input = st.text_input("이름을 입력하세요:")

####  입력받은 이름 출력
if user_input:
    st.write(f"안녕하세요, {user_input}님!")

st.write(
    "------------------------------------------------------------------------------"
)

st.title("텍스트 영역 입력 (Text Area)")

####  텍스트 영역
feedback = st.text_area("피드백을 남겨주세요:", height=340)

if feedback:
    st.write("입력된 피드백:", feedback)

st.write(
    "------------------------------------------------------------------------------"
)
st.divider()


st.title("숫자 입력 (슬라이더)")
####  숫자 입력
age = st.number_input("나이를 입력하세요:", min_value=0, max_value=100, step=3)

####  슬라이더로 범위 입력
height = st.slider("키를 입력하세요 (cm)", 100, 200, 150, step=5)

####  입력받은 값 출력
st.write(f"당신의 나이는 [{age}] 세 입니다.")
st.write(f"당신의 키는 [{height}]cm 입니다.")

st.divider()


st.title("버튼")
# 버튼을 클릭했을 때 출력
if st.button("버튼 클릭"):
    st.write("버튼이 클릭되었습니다!")


st.write(
    "------------------------------------------------------------------------------"
)

st.title("숫자 입력 (첫번째,두번째)")
####  두 숫자 입력
num1 = st.number_input("첫 번째 숫자를 입력하세요", 10)
num2 = st.number_input("두 번째 숫자를 입력하세요", 0)

# 버튼 클릭 시 계산
if st.button("합계 계산"):
    result = num1 + num2
    st.write(f"입력한 {num1} + {num2} = {result}입니다.")


st.write(
    "------------------------------------------------------------------------------"
)


st.title("체크 박스")
####  체크박스
accept_terms = st.checkbox("약관에 동의합니다.")  ### boolean

if accept_terms:
    st.write("약관에 동의하셨습니다.")
else:
    st.write("약관에 동의하지 않았습니다.")


st.title("라디오 버튼")
####  라디오 버튼
favorite_color = st.radio("가장 좋아하는 색은 무엇인가요?", ["빨강", "파랑", "초록"])

st.write(f"선택한 색은 [{favorite_color}]입니다.")


st.write(
    "------------------------------------------------------------------------------"
)


st.title("선택 박스(selectbox)")
####  선택 박스
option = st.selectbox("어떤 과일을 좋아하나요?", ["사과", "바나나", "체리", "오렌지"])

# 선택한 과일에 대한 출력
if option == "사과":
    st.write("사과는 건강에 좋습니다!")
elif option == "바나나":
    st.write("바나나는 에너지를 줍니다!")
elif option == "체리":
    st.write("체리는 항산화 성분이 많습니다!")
else:
    st.write("오렌지는 비타민 C가 풍부합니다.")


st.write(
    "------------------------------------------------------------------------------"
)

st.title("멀티 Select 박스  (multiselect) ")

# 멀티 셀렉트
selected_fruits = st.multiselect(
    "좋아하는 과일을 선택하세요", ["사과", "바나나", "체리", "딸기"]
)

st.write(f"선택한 과일들: {', '.join(selected_fruits)}")


st.write(
    "------------------------------------------------------------------------------"
)

st.title("날짜 입력 (date_input)")

####  날짜 입력
birthday = st.date_input("생일을 입력하세요:")
st.write(f"당신의 생일은 {birthday}입니다.")


st.write(
    "------------------------------------------------------------------------------"
)

import numpy as np
import matplotlib.pyplot as plt

st.title("Slider")

####  슬라이더로 값 입력 받기
value = st.slider("값을 선택하세요", 0, 100, 50)

####  실시간으로 변화하는 그래프
x = np.linspace(0, 10, 100)
y = np.sin(x + value / 10)

fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)


st.write(
    "------------------------------------------------------------------------------"
)
