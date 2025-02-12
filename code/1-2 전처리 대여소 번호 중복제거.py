import pandas as pd

# 주어진 데이터
df = pd.read_csv(r"출퇴근관련\조서영\data\filtered_bike_station_data.csv")

# 시간대와 대여소 번호별로 중복 제거하고 첫 번째 값만 선택
unique_df = df.drop_duplicates(subset=['시간대', '대여소번호'], keep='first')

# 새로운 CSV 파일로 저장
unique_df.to_csv(r"출퇴근관련\조서영\data\unique_filtered_bike_station_data.csv", index=False)

print("중복 제거된 데이터가 'unique_filtered_bike_station_data.csv' 파일에 저장되었습니다.")