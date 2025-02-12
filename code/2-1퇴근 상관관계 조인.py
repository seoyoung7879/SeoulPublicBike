import pandas as pd

# 각 파일의 경로
file1 = r"data\격자별 따릉이 대여소 개수.csv"
file2 = r"data\격자별 지하철역 개수.csv"
file3 = r"data\격자별 버스정류장 개수.csv"
file6 = r"data\퇴근_평균_거치율.csv"

# 각 파일을 데이터프레임으로 읽기
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df6 = pd.read_csv(file6)

# 격자_ID를 기준으로 조인
merged_df = df1.merge(df2, on='격자_ID', how='inner') \
               .merge(df3, on='격자_ID', how='inner') \
               .merge(df6, on='격자_ID', how='inner')

# 결측값이 있는 행 제거
cleaned_df = merged_df.dropna()

# 결과를 새로운 CSV 파일로 저장
cleaned_df.to_csv(r"data\퇴근_상관관계.csv", index=False)