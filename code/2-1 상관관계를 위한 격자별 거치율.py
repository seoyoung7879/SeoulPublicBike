import pandas as pd
import geopandas as gpd
import folium
import os

# 1. 데이터 불러오기
bike_station_rate_df = pd.read_csv(r"조서영\data\unique_filtered_bike_station_data.csv")

# 2. GeoDataFrame 변환 (geometry 열을 이용)
bike_station_rate_gdf = gpd.GeoDataFrame(
    bike_station_rate_df,
    geometry=gpd.GeoSeries.from_wkt(bike_station_rate_df["geometry"]),
    crs="EPSG:4326"  # WGS 84 좌표계
)

# 3. 격자 데이터 불러오기
grid_shp = r"data/match/match.shp"  # 격자 shapefile 경로를 넣어주세요
gdf_grid = gpd.read_file(grid_shp)
gdf_grid = gdf_grid.to_crs("EPSG:4326")  # 격자 좌표계를 WGS 84로 변환

# 출근 시간대 (7, 8) 데이터 필터링
morning_df = bike_station_rate_gdf[bike_station_rate_gdf['시간대'].isin([7, 8])]

# 퇴근 시간대 (18, 19) 데이터 필터링
evening_df = bike_station_rate_gdf[bike_station_rate_gdf['시간대'].isin([18, 19])]

# 4. 격자 내 평균 거치율 계산 (출근 시간대)
morning_with_grid = gpd.sjoin(morning_df, gdf_grid, how="left", predicate="within")
avg_rate_per_grid_morning = morning_with_grid.groupby("index_right")["거치율"].mean().reset_index(name="평균_거치율")
avg_rate_per_grid_morning = avg_rate_per_grid_morning.rename(columns={"index_right": "격자_ID"})

# 5. 격자 내 평균 거치율 계산 (퇴근 시간대)
evening_with_grid = gpd.sjoin(evening_df, gdf_grid, how="left", predicate="within")
avg_rate_per_grid_evening = evening_with_grid.groupby("index_right")["거치율"].mean().reset_index(name="평균_거치율")
avg_rate_per_grid_evening = avg_rate_per_grid_evening.rename(columns={"index_right": "격자_ID"})

# 6. 격자 데이터에 평균 거치율 추가 (출근 시간대)
gdf_grid_morning = gdf_grid.merge(avg_rate_per_grid_morning, left_index=True, right_on="격자_ID", how="left").fillna(0)

# 7. 격자 데이터에 평균 거치율 추가 (퇴근 시간대)
gdf_grid_evening = gdf_grid.merge(avg_rate_per_grid_evening, left_index=True, right_on="격자_ID", how="left").fillna(0)

# 8. 평균 거치율 데이터를 CSV 파일로 저장
avg_rate_per_grid_morning.to_csv(r"data\출근_평균_거치율.csv", index=False)
avg_rate_per_grid_evening.to_csv(r"data\퇴근_평균_거치율.csv", index=False)


print("출근 시간대와 퇴근 시간대의 평균 거치율 데이터가 각각 CSV 파일로 저장되었습니다.")
print("출근 시간대와 퇴근 시간대의 평균 거치율 지도가 각각 HTML 파일로 저장되었습니다.")