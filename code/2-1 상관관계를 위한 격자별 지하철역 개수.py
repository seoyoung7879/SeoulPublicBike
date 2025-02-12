import pandas as pd
import geopandas as gpd
import folium
import os

# 1. 지하철역 데이터 불러오기
subway_df = pd.read_csv(r"data\subway_with_coords_unique.csv")  # 지하철역 데이터 파일 경로를 넣어주세요

# 2. GeoDataFrame 변환 (위도/경도를 포인트로 변환)
subway_gdf = gpd.GeoDataFrame(
    subway_df,
    geometry=gpd.points_from_xy(subway_df["경도"], subway_df["위도"]),
    crs="EPSG:4326"  # WGS 84 좌표계
)

# 3. 격자 데이터 불러오기
grid_shp = r"data\match\match.shp"  # 격자 shapefile 경로를 넣어주세요
gdf_grid = gpd.read_file(grid_shp)
gdf_grid = gdf_grid.to_crs("EPSG:4326")  # 격자 좌표계를 WGS 84로 변환

# 4. 격자 내 지하철역 개수 계산
subway_with_grid = gpd.sjoin(subway_gdf, gdf_grid, how="left", predicate="within")
subway_count = subway_with_grid.groupby("index_right").size().reset_index(name="지하철역_개수")
subway_count = subway_count.rename(columns={"index_right": "격자_ID"})

# 5. 격자 데이터에 지하철역 개수 추가
gdf_grid = gdf_grid.merge(subway_count, left_index=True, right_on="격자_ID", how="left").fillna(0)

# 6. 지하철역 개수 데이터를 CSV 파일로 저장
subway_count.to_csv(r"data\격자별 지하철역 개수.csv", index=False)