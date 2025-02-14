import pandas as pd

# 1. 데이터 불러오기
bike_station_rate_df = pd.read_csv(r"result_gdf_cell.csv")  # 데이터 파일 경로

# 2. 필요한 열만 선택
columns_to_keep = [
    "대여소번호", "시간대", "대여가능수량", "보관소(대여소)명", "설치대수", "거치율", "geometry", "CELL_ID", "CELL_X", "CELL_Y", "GID", "LBL", "VAL"
]
filtered_df = bike_station_rate_df[columns_to_keep]

# 3. 데이터 저장
filtered_df.to_csv(r"data\filtered_bike_station_data.csv", index=False)

print("필요한 열만 남긴 데이터가 CSV 파일로 저장되었습니다.")