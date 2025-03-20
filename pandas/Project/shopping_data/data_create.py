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

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 랜덤 시드 설정
random.seed(42)

# 제품 목록과 카테고리 정의
product_names = [
    "Arduino Starter Kit",
    "Raspberry Pi 4",
    "Micro:bit Educational Kit",
    "Scratch Coding Kit",
    "Python Programming Book",
    "Robotics Kit",
    "3D Printer Kit",
    "IoT Kit",
    "AI Learning Kit",
    "STEM Learning Pack",
]
categories = ["Electronics", "Books", "Educational Kits", "Robotics", "Programming"]

# 지역 정보
regions = [
    "Seoul",
    "Busan",
    "Incheon",
    "Daegu",
    "Gwangju",
    "Daejeon",
    "Ulsan",
    "Jeju",
    "Gyeonggi",
    "Gangwon",
]

# 1. 가격과 할인율
price_range = (50, 500)  # 제품 가격 범위
discount_range = (0.1, 0.5)  # 할인 범위

# 2. 판매량, 평점
sold_range = (1, 50)  # 판매 수량 범위
rating_range = (3.5, 5.0)  # 평점 범위

# 3. 날짜 범위 (최근 2년)
start_date = datetime.now() - timedelta(days=730)  # 2년 전
end_date = datetime.now()

# 4. 데이터 생성
data = []
for i in range(500):
    product_id = i + 1
    product_name = random.choice(product_names)
    category = random.choice(categories)
    price = random.randint(price_range[0], price_range[1])
    discounted_price = round(
        price * (1 - random.uniform(discount_range[0], discount_range[1])), 2
    )
    sold_quantity = random.randint(sold_range[0], sold_range[1])
    rating = round(random.uniform(rating_range[0], rating_range[1]), 1)

    # 결측치 추가 (20개 제품마다)
    if i % 20 == 0:
        discounted_price = np.nan

    # 이상치 추가 (10개마다)
    if i % 10 == 0:
        price = -1  # 가격 이상치

    # 지역 정보
    region = random.choice(regions)

    # 날짜 생성 (최근 2년 내)
    purchase_date = start_date + timedelta(days=random.randint(0, 730))

    # 재료비 원가 (제품 가격의 40%)
    material_cost = price * 0.4
    revenue = discounted_price * sold_quantity

    # 데이터 추가
    data.append(
        [
            product_id,
            product_name,
            category,
            price,
            discounted_price,
            sold_quantity,
            rating,
            purchase_date,
            region,
            material_cost,
            revenue,
        ]
    )

# 데이터프레임 생성
df = pd.DataFrame(
    data,
    columns=[
        "product_id",
        "product_name",
        "category",
        "price",
        "discounted_price",
        "sold_quantity",
        "rating",
        "purchase_date",
        "region",
        "material_cost",
        "revenue",
    ],
)

# CSV 파일로 저장
df.to_csv("shopping_mall_data.csv", index=False)

print("CSV 파일이 생성되었습니다.")
