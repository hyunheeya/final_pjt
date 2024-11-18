# final_pjt
### DB 테이블 구현 코드 ###
- 구글 코랩 사용

#### 예금 ####
``` 
import requests
import pandas as pd
import sqlite3
from google.colab import drive
drive.mount('/content/drive')

# 1. API_KEY를 활용하여 url 지정
API_KEY = ?
url = f"https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"

# 2. 가져온 데이터를 json 데이터로 변환
response = requests.get(url)
data = response.json()

# 3. 데이터 프레임으로 변환 후 csv 파일로 저장
df1 = pd.DataFrame(data['result']['baseList'])
df1.to_csv('/content/drive/MyDrive/baseList.csv')

df2 = pd.DataFrame(data['result']['optionList'])
df2.to_csv('/content/drive/MyDrive/optionList.csv')

# 4. 첫 번째 파일과 두 번째 파일을 불러와
df1_read = pd.read_csv('/content/drive/MyDrive/baseList.csv')  # 첫 번째 파일 경로
df2_read = pd.read_csv('/content/drive/MyDrive/optionList.csv') # 두 번째 파일 경로

# 5. 여러 개의 인덱스의 행 삭제
df1_read = df1_read.drop([9, 38], axis=0) 
# index 9번 상품 드랍 (사유 : 성별 이슈)
# index 38번 상품 드랍 (사유 : 토스 계좌 보유해야 함)

# 6. 첫 번째 파일의 특정 열을 선택하여 두 번째 파일과 합치기
# 'fin_prdt_cd'을 기준으로 합침
# 첫 번째 파일에서 특정 열만 선택해서 merge
df1_selected = df1_read[['kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm', 'join_way', 'join_member']]  # 합치고 싶은 열 선택

# 7. outer join을 사용하여 결합
result = pd.merge(df1_selected, df2_read, on='fin_prdt_cd', how='outer')

# 8. 결과 CSV 파일로 저장
result = result.drop(['fin_prdt_cd', 'Unnamed: 0', 'fin_co_no', 'dcls_month'], axis=1)
result = result.dropna()  # null 값이 존재하는 행 삭제
result.to_csv('/content/drive/MyDrive/merge1.csv')

# 9. CSV 파일을 pandas DataFrame으로 읽기
csv_file_path = '/content/drive/MyDrive/merge1.csv'  # CSV 파일 경로를 지정
df_csv = pd.read_csv(csv_file_path)

# 10. SQLite3 데이터베이스에 연결
sqlite_db_path = '/content/drive/MyDrive/database1.db'  # SQLite3 데이터베이스 파일 경로를 지정
conn = sqlite3.connect(sqlite_db_path)

# 11. DataFrame을 SQLite3 데이터베이스에 저장 (테이블 이름은 'table1'으로 지정)
df_csv.to_sql('table1', conn, if_exists='replace', index=False)

# 12. 커넥션 종료
conn.close()
```


#### 적금 ####
```
import requests
import pandas as pd
import sqlite3
from google.colab import drive
drive.mount('/content/drive')

# 1. API_KEY를 활용하여 url 지정
API_KEY = ?
url2 = f'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'


# 2. 가져온 데이터를 json 데이터로 변환
response2 = requests.get(url2)
data2 = response2.json()

# 3. 데이터 프레임으로 변환 후 csv 파일로 저장
df3 = pd.DataFrame(data2['result']['baseList'])
df3.to_csv('/content/drive/MyDrive/baseList2.csv')

df4 = pd.DataFrame(data2['result']['optionList'])
df4.to_csv('/content/drive/MyDrive/optionList2.csv')

# 4. 첫 번째 파일과 두 번째 파일을 불러와
df3_read = pd.read_csv('/content/drive/MyDrive/baseList2.csv')  # 첫 번째 파일 경로
df4_read = pd.read_csv('/content/drive/MyDrive/optionList2.csv') # 두 번째 파일 경로

# 5. 여러 개의 인덱스의 행 삭제
df3_read = df3_read.drop([29, 54, 55, 56, 57], axis=0)
# index 29번 상품 드랍 (사유 : 중소기업에 재직해야 함)
# index 54~57번 상품 드랍 (사유 : 토스 계좌 보유해야 함)

# 6. 첫 번째 파일의 특정 열을 선택하여 두 번째 파일과 합치기
# 예시로 'fin_prdt_nm'을 기준으로 합침
# 첫 번째 파일에서 특정 열만 선택해서 merge
df3_selected = df3_read[['kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm', 'join_way', 'join_member', 'etc_note']]  # 합치고 싶은 열 선택

# 7. outer join을 사용하여 결합
result2 = pd.merge(df3_selected, df4_read, on='fin_prdt_cd', how='outer')

# 8. 결과 확인
result2 = result2.drop(['fin_prdt_cd', 'Unnamed: 0', 'fin_co_no', 'dcls_month'], axis=1)
result2 = result2.dropna() # null 값이 존재하는 행 삭제
result2.to_csv('/content/drive/MyDrive/merge2.csv')

# 9. CSV 파일을 pandas DataFrame으로 읽기
csv_file_path = '/content/drive/MyDrive/merge2.csv'  # CSV 파일 경로를 지정해주세요
df2_csv = pd.read_csv(csv_file_path)

# 10. SQLite3 데이터베이스에 연결
sqlite_db_path = '/content/drive/MyDrive/database2.db'  # SQLite3 데이터베이스 파일 경로를 지정해주세요
conn = sqlite3.connect(sqlite_db_path)

# 11. DataFrame을 SQLite3 데이터베이스에 저장 (테이블 이름은 'table2'으로 지정)
df2_csv.to_sql('table2', conn, if_exists='replace', index=False)

# 12. 커넥션 종료
conn.close()
```