import pandas as pd
import numpy as np

# 테스트용 데이터 생성
np.random.seed(42)  # 랜덤 시드를 고정하여 재현 가능하게 함

# 임의의 마케팅 데이터 생성
data = {
    "Customer_ID": np.arange(1, 101),
    "Age": np.random.randint(18, 65, 100),
    "Gender": np.random.choice(["Male", "Female"], 100),
    "Income": np.random.randint(20000, 100000, 100),
    "Product_Purchased": np.random.choice(
        ["Product_A", "Product_B", "Product_C", "Product_D"], 100
    ),
    "Purchase_Amount": np.round(np.random.uniform(10, 500, 100), 2),
    "Purchase_Date": pd.to_datetime(
        np.random.choice(pd.date_range("2022-01-01", "2022-12-31", freq="D"), 100)
    ),
    "Store_Location": np.random.choice(
        ["Store_1", "Store_2", "Store_3", "Store_4"], 100
    ),
    "Customer_Satisfaction": np.random.randint(1, 6, 100),  # 1-5 점 척도
    "Marketing_Channel": np.random.choice(["Online", "TV", "Print", "In-store"], 100),
}

# DataFrame 생성
df_marketing = pd.DataFrame(data)

# CSV로 저장
csv_file_path = "./marketing_data.csv"
df_marketing.to_csv(csv_file_path, index=False)

csv_file_path
