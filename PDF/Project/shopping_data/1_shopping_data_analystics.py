###### product_id: 제품 고유 ID
###### product_name: 제품명 (메이커 코딩 제품 10개)
###### category: 제품 카테고리 (예: 교육 키트, 소프트웨어 등)
###### price: 제품 가격
###### discounted_price: 할인된 가격
###### sold_quantity: 판매된 수량
###### rating: 제품 평점
###### purchase_date: 구매 날짜
###### region: 구매 지역 (서울, 부산 등)
###### material_cost: 재료비 원가 (가격의 40%)
###### revenue: 매출 (판매량 * 가격)
###### discount_rate: 할인율 (할인된 가격 / 원래 가격)


import streamlit as st
import pandas as pd

# 앱 제목
st.title("메이커 코딩 제품 매출 분석")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 파일 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터프레임 미리보기
    st.write("### 데이터 미리보기", df.head())

    # 데이터 정보 (info)
    st.write("### 데이터 정보 (info())")
    buffer = df.info(buf=None)
    st.text(buffer)  # 데이터 정보 출력

    # 통계 요약 정보 (describe)
    st.write("### 통계적 요약 (describe())")
    st.write(df.describe())

    # 결측치 현황
    st.write("### 결측치 현황")
    st.write(df.isnull().sum())

