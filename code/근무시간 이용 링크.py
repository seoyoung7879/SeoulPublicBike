import pandas as pd
import pydeck as pdk
import numpy as np

# 데이터 불러오기
file_path = r"./data/processed_bike_data.parquet"
df = pd.read_parquet(file_path)

# 주중 9시부터 17시까지의 데이터 필터링
df['대여일시'] = pd.to_datetime(df['대여일시'])
df['대여시간'] = df['대여일시'].dt.hour
df['대여요일'] = df['대여일시'].dt.weekday

# 주중 (월요일~금요일) 9시부터 17시까지의 데이터 필터링
df_filtered = df[(df['대여시간'] >= 10) & (df['대여시간'] < 17) & (df['대여요일'] < 5)]

# 대여대여소ID와 반납대여소ID가 같은 경우 카운팅
df_grouped = df_filtered.groupby(
    ['대여대여소ID', '반납대여소ID']
).agg(
    대여소_LAT=('대여소_LAT', 'first'),
    대여소_LOT=('대여소_LOT', 'first'),
    반납소_LAT=('반납소_LAT', 'first'),
    반납소_LOT=('반납소_LOT', 'first'),
    이용자수=('대여대여소ID', 'size')
).reset_index()

# 이용자수 기준으로 내림차순 정렬
df_grouped = df_grouped.sort_values(by='이용자수', ascending=False)

# 상위 1000개의 데이터만 선택
df_grouped_top1000 = df_grouped.head(2000)

# ArcLayer 생성 (출발지와 도착지 간 링크)
arc_layer = pdk.Layer(
    'ArcLayer',
    df_grouped_top1000,
    get_source_position='[대여소_LOT, 대여소_LAT]',
    get_target_position='[반납소_LOT, 반납소_LAT]',
    get_source_color='[255, 0, 0, 160]',  # 빨강색으로 출발지 표시
    get_target_color='[0, 0, 255, 160]',  # 파랑색으로 도착지 표시
    get_width='이용자수 / 200',  # 이용자수로 선 두께 결정
    pickable=True,
    auto_highlight=True
)

# TileLayer 설정 (지도 배경으로 OpenStreetMap 사용)
tile_layer = pdk.Layer(
    "TileLayer",
    data=None,
    get_tile_url="http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
)

# ViewState 설정 (중심 좌표와 줌 설정)
view_state = pdk.ViewState(
    latitude=df_grouped_top1000['대여소_LAT'].mean(),
    longitude=df_grouped_top1000['대여소_LOT'].mean(),
    zoom=11,
    pitch=45
)

# 툴팁 설정 (이용자수 표시)
tooltip_html = """
<div style='font-size: 14px; padding: 5px;'>
    <div><span style='color:#ffffff'>시작 위도:</span> {대여소_LAT}</div>
    <div><span style='color:#ffffff'>시작 경도:</span> {대여소_LOT}</div>
    <div><span style='color:#ffffff'>종료 위도:</span> {반납소_LAT}</div>
    <div><span style='color:#ffffff'>종료 경도:</span> {반납소_LOT}</div>
    <div><span style='color:#33ff57'>이용자수:</span> {이용자수}</div>
</div>
"""

# Deck 생성 (레이어와 툴팁 포함)
deck = pdk.Deck(
    layers=[tile_layer, arc_layer],
    initial_view_state=view_state,
    tooltip={"html": tooltip_html}
)

# HTML 파일로 저장
output_file = r'출퇴근관련\조서영\html\주중_근무시간_링크_시각화.html'
deck.to_html(output_file, notebook_display=False)

print("시각화가 완료되었습니다. HTML 파일이 저장되었습니다.")
