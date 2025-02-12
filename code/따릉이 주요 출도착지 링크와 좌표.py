import pandas as pd
import pydeck as pdk
import geopandas as gpd

# 한글 폰트 설정
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows의 경우
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df1 = pd.read_csv(r"./data/격자_출근_일평균_대여량(링크)_위경도.csv")
df2 = pd.read_csv(r"./data/격자_퇴근_일평균_대여량(링크)_위경도.csv")

# 좌표 데이터 추가
additional_coords = pd.DataFrame({
    'name': ['여의나루역', '국회의사당역', '영등포역 5번출구', '영등포로터리', '대방역', '샛강역(신림,9호선)'],
    'latitude': [37.52689256754171, 37.52818073611419, 37.51643280394692, 37.51815788663115, 37.51279089944814, 37.51718446863203],
    'longitude': [126.93246127093647, 126.91782929728485, 126.90720377279115, 126.91266801476523, 126.92703909758625, 126.92896909571402]
})

# 반납소 시각화
file_paths = [
    './data/격자_출근_일평균_대여량(링크)_위경도.csv',
    './data/격자_퇴근_일평균_대여량(링크)_위경도.csv'
]

output_files2 = [
    r'html\격자_출근_일평균_반납량_링크_시각화.html',
    r'html\격자_퇴근_일평균_반납량_링크_시각화.html'
]

for file_path, output_file in zip(file_paths, output_files2):
    df = pd.read_csv(file_path)
    df = df.rename(columns={
        '대여건수': 'avg_rental_count',
        '이용시간(분)': 'use_time'
    })    
    
    df_node = df.groupby(["반납소_셀"]).agg({
        "이용거리(M)" : "mean",
        "use_time" : "mean",
        "avg_rental_count" : "sum",
        "대여소_geometry" : "first",
        "반납소_geometry" : "first"}).reset_index()
    
    df = df.dropna(subset=['avg_rental_count'])
    df['avg_rental_count'] = pd.to_numeric(df['avg_rental_count'], errors='coerce')    
    
    gdf_node = gpd.GeoDataFrame(df_node, geometry=gpd.GeoSeries.from_wkt(df_node['반납소_geometry']))
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['대여소_geometry']))
    end_gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['반납소_geometry']))
    
    gdf_node['centroid'] = gdf_node['geometry'].centroid
    gdf['start_centroid'] = gdf['geometry'].centroid
    end_gdf['end_centroid'] = end_gdf['geometry'].centroid
    
    gdf_node['centroid_lat'] = gdf_node['centroid'].y
    gdf_node['centroid_lng'] = gdf_node['centroid'].x
    gdf['start_lat'] = gdf['start_centroid'].y
    gdf['start_lng'] = gdf['start_centroid'].x
    end_gdf['end_lat'] = end_gdf['end_centroid'].y
    end_gdf['end_lng'] = end_gdf['end_centroid'].x
    
    gdf_node = gdf_node.drop(columns=['geometry', 'centroid'])
    gdf = gdf.drop(columns=['geometry', 'start_centroid'])
    end_gdf = end_gdf.drop(columns=['geometry', 'end_centroid'])
    
    duplicate_cols = gdf.columns.intersection(end_gdf.columns)
    end_gdf = end_gdf.drop(columns=duplicate_cols)
    merged_df = pd.concat([gdf, end_gdf], axis=1)
    
    top_50_df = merged_df.nlargest(1000, 'avg_rental_count')

    arc_layer = pdk.Layer(
        'ArcLayer',
        top_50_df,
        get_source_position='[start_lng, start_lat]',
        get_target_position='[end_lng, end_lat]',
        get_source_color='[255, 0, 0, 160]',
        get_target_color='[0, 0, 255, 160]',
        get_width='avg_rental_count / 1000',
        pickable=True,
        auto_highlight=True
    )
    
    scatter_plot_layer = pdk.Layer(
        'ScatterplotLayer',
        data=gdf_node,
        get_position=['centroid_lng', 'centroid_lat'],
        get_radius='avg_rental_count/100',
        get_fill_color=[0, 255, 255],
        pickable=True,
        auto_highlight=True,
    )

    additional_scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=additional_coords,
        get_position=['longitude', 'latitude'],
        get_radius=50,  # 점의 크기를 줄임
        get_fill_color=[255, 0, 0],
        pickable=True,
        auto_highlight=True,
    )

    tile_layer = pdk.Layer(
        "TileLayer",
        data=None,
        get_tile_url="http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
    )

    view_state = pdk.ViewState(
        latitude=top_50_df['start_lat'].mean(),
        longitude=top_50_df['start_lng'].mean(),
        zoom=11,
        pitch=45
    )

    deck = pdk.Deck(
    layers=[tile_layer, arc_layer, scatter_plot_layer, additional_scatter_layer],
    initial_view_state=view_state,
    tooltip={
        "html": """
        <div style='font-size: 14px; padding: 5px;'>
            {% if name is defined %}
                <div><span style='color:#ffffff'>이름:</span> {name}</div>
                <div><span style='color:#ffffff'>위도:</span> {latitude}</div>
                <div><span style='color:#ffffff'>경도:</span> {longitude}</div>
            {% else %}
                <div><span style='color:#ffffff'>시작 위도:</span> {start_lat}</div>
                <div><span style='color:#ffffff'>시작 경도:</span> {start_lng}</div>
                <div><span style='color:#ffffff'>종료 위도:</span> {end_lat}</div>
                <div><span style='color:#ffffff'>종료 경도:</span> {end_lng}</div>
                <div><span style='color:#ffffff'>이용 시간:</span> {use_time}</div>
                <div><span style='color:#33ff57'>일평균 대여량:</span> {avg_rental_count}</div>
            {% endif %}
        </div>
        """
    }
)

    deck.to_html(output_file, notebook_display=False)

print("시각화가 완료되었습니다. 각 HTML 파일이 저장되었습니다.")