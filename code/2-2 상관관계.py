import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
import plotly.express as px

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우
font_name = fm.FontProperties(fname=font_path).get_name()
rcParams['font.family'] = font_name

# 마이너스 기호가 포함된 폰트 설정
rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = pd.read_csv(r"data\출근_상관관계.csv")

# '격자_ID' 열 제외
df = df.drop(columns=['격자_ID'])

# 상관관계 계산
correlation_matrix = df.corr()

# 상관관계 행렬 터미널에 출력
print("상관관계 행렬:")
print(correlation_matrix)

# Plotly를 사용하여 히트맵 그리기
fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto", color_continuous_scale='plasma')
fig.update_layout(title='출근 시간대 상관관계 히트맵')

# 히트맵을 HTML로 저장
fig.write_html(r"html\출근_상관관계_히트맵.html")

# 히트맵을 시각화
fig.show()


#==================================퇴근
# 데이터 불러오기
df = pd.read_csv(r"data\퇴근_상관관계.csv")

# '격자_ID' 열 제외
df = df.drop(columns=['격자_ID'])

# 상관관계 계산
correlation_matrix = df.corr()

# 상관관계 행렬 터미널에 출력
print("상관관계 행렬:")
print(correlation_matrix)

# Plotly를 사용하여 히트맵 그리기
fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto", color_continuous_scale='plasma')
fig.update_layout(title='퇴근 시간대 상관관계 히트맵')

# 히트맵을 HTML로 저장
fig.write_html(r"html\퇴근_상관관계_히트맵.html")

# 히트맵을 시각화
fig.show()