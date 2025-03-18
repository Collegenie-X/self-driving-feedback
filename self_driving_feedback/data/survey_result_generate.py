### user_id: 각 행을 식별하기 위한 고유 ID (예: user1, user2, …)
### age: 15~60 사이의 나이 (정수)
### gender: 성별 정보 (True/False; 예시에서는 True가 여성, False가 남성으로 가정)
### region: ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"] 중 하나
### q1 ~ q16: 각 질문에 대한 응답 (정수, 1~5 사이)


import pandas as pd
import numpy as np

# 난수 생성 seed 설정 (재현 가능하도록)
np.random.seed(42)

n = 200  # 생성할 데이터 수

# user_id: user1, user2, ..., user200 생성
user_ids = [f"user{i+1}" for i in range(n)]

# age: 15~60 사이의 정수
ages = np.random.randint(15, 61, n)

# gender: True (여성) 또는 False (남성)
genders = np.random.choice([True, False], n)

# region: 미리 정해진 6개 지역 중 하나 선택
regions = np.random.choice(
    ["서울", "경기/인천", "충청/대전", "전라/광주", "경상/부산", "강원/제주"], n
)

# q1 ~ q16: 각 질문에 대한 응답 (1~5 사이의 정수)
questions = {}
for i in range(1, 17):
    questions[f"q{i}"] = np.random.randint(1, 6, n)

# 데이터프레임 생성
df = pd.DataFrame(
    {"user_id": user_ids, "age": ages, "gender": genders, "region": regions}
)

# 질문 컬럼 추가 (q1 ~ q16)
for i in range(1, 17):
    df[f"q{i}"] = questions[f"q{i}"]

# CSV 파일로 저장 (./data/survey_results.csv 경로에 저장)
df.to_csv("./survey_results.csv", index=False)

print("임시 설문 데이터 200개가 ./data/survey_results.csv 에 저장되었습니다.")
