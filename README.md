# Final_PJT

## 1. 프로젝트 및 팀원 소개

### 📋 **프로젝트 소개**
**초보자를 위한 예적금 추천 서비스**

![StarPot_logo_ai](https://github.com/user-attachments/assets/f19a70e4-bd01-4f08-a0fc-f372ee3ec2bd)

### 📌 **프로젝트 개요**
**🌟 StarPot 이란??**

작은 별을 저금통(Pot)에 담듯이, 당신의 금융 성장을 돕습니다.

금융에 대해 알아가고 싶지만, 어려운 내용 때문에 포기하신 적 많지 않나요?

<img src="https://github.com/user-attachments/assets/50d2b082-23bb-4d35-99e2-9966f4cd4f05"  width="400" height="400"/>

StarPot은 금융 초보자를 대상으로 예적금 상품을 추천하는 서비스입니다.  
어렵고 복잡한 금융 용어와 내용을 배제하고, 간단하고 이해하기 쉬운 정보를 제공합니다.  

**👫 누구를 위한 서비스인가요?**

- 10대~30대의 금융 초보자
  
  "어떤 예적금 상품을 선택해야 할지 모르겠어요!"
  
  "금융 용어가 너무 어렵고 복잡해요!"
  
  "같은 상품인데 조건마다 금리가 많아서 어려워요!"

  
- 예적금 상품을 비교하고 싶은 모든 사람
  
  "쉽게 조건을 비교해서 더 나은 상품을 찾고 싶어요!"
  
  "다른 사용자들의 예적금 상품 후기를 보고 싶어요!"

---

### 👫 **팀원 구성 및 역할**

| 이름   | 역할                          | 주요 담당 업무                         |
|--------|-------------------------------|---------------------------------------|
| 조현희 | 백엔드 팀장 / 기능 구현 | 예적금 데이터 테이블 구축 / 추천 알고리즘 / 주변 은행 찾기 / 환율계산기 / 챗봇 / 똑! 똑! 게시판 |
| 깅명주 | 프론트엔드 팀장 / 기능 구현 | 전체 예적금 상품 조회 / 로그인 회원가입 / 마이페이지 / 상품 좋아요 및 댓글 / 캐릭터 및 로고 디자인 |

---

### 🛠️ **기술 스택**
- **백엔드**: Django(4.2), Django REST Framework, SQLite
- **프론트엔드**: Vue 3
- **API**: 금융감독원 API, 카카오맵 API, 한국수출입은행 환율 API
- **협업 툴**: Notion, Git, Google Colab
- **기타**: 생성형 AI (초보자를 위한 금융 지식 알리미)

---

## 2. 설계 내용(아키텍처 등) 및 실제 구현 정도

### 🔍 **설계 및 구현**
- **아키텍처 설계**
  - RESTful API 구조 설계
  - 클라이언트-서버 구조 기반 데이터 통신
  - 데이터 저장소: SQLite 데이터베이스

- **서비스 구현**

| **기능**              | **설명**                                                                                           |
|------------------------|---------------------------------------------------------------------------------------------------|
| **추천 페이지**         | 쉽고 간단한 질문으로 사용자에게 답변을 받아 추천 상품 제공                                                    |
| **예적금 전체 상품 페이지** | - 예적금 상품의 전체 리스트 보기<br> -각 상품의 금리 별로 상세페이지를 제공하여 유저 간 정보 공유 및 소통 가능<br> - 전체, 금리순, 좋아요순, 은행명순으로 상품을 찾아볼 수 있게 필터 기능 제공 |
| **주변 은행 검색**      | 위치 기반 서비스로 내 주변 은행 찾기                                                                       |
| **똑!똑! 게시판**       | - 관리자 공지<br> - 금융 초보자에게 필요한 금융 지식을 친절한 아티클로 전달                                                     |
| **환율 계산기**         | 사용자 정보와 관심사에 따른 상품 관리 및 조회                                                                 |
| **챗봇 서비스**         | 초보자에게 금융 지식을 쉽게 알려주는 챗봇 서비스.                                                               |
| **마이 페이지**         | - 프로필 관리(개인정보 수정, 비밀번호 변경)<br> - 내가 좋아요한 상품(예금, 적금) 및 좋아요한 상품의 금리 비교 그래프 제공<br> - 내가 댓글 단 상품(예금, 적금)           |
| **회원가입/로그인/로그아웃** | 사용자 맞춤 서비스를 제공하기 위해 회원 기능 제공                                                                   |



---

## 3. 데이터베이스 모델링(ERD) 및 Vue 컴포넌트 구성

### 📊 **데이터베이스 모델링**
![StarPot_ERD](https://github.com/user-attachments/assets/99d6d156-1246-4f66-b8d9-1b16072de7cf)

### 🧚 **Vue 컴포넌트**
![KakaoTalk_Photo_2024-11-26-19-37-57](https://github.com/user-attachments/assets/0f4cefbf-0f9e-4128-8cb3-013ff464f63b)

---

## 4. 금융 상품 추천 알고리즘에 대한 기술적 설명

  사용자의 답변에 따라 적합한 상품에 가중치를 부여하고, 가중치가 높은 순으로 추천 상품을 제공합니다.

  데이터 필터링을 위해 테이블을 먼저 구성했으며, 구글 코랩을 사용해서 DB 테이블을 구현했습니다.

### **DB 테이블 구현 코드**

#### 예금
```python
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

    # join_member 값에 따라 age_range 열 추가하는 함수 정의
    def determine_age_range(join_member):
        if "만14세이상" in join_member:
            return "14, 150"
        elif "만 17세 이상" in join_member:
            return "17, 150"
        elif "만50세 이상" in join_member:
            return "50, 150"
        else:
            return "0, 150"

    # 10. age_range 열 추가
    df_csv["age_range"] = df_csv["join_member"].apply(determine_age_range)

    # 11. SQLite3 데이터베이스에 연결
    sqlite_db_path = '/content/drive/MyDrive/database1.db'  # SQLite3 데이터베이스 파일 경로를 지정
    conn = sqlite3.connect(sqlite_db_path)

    # 12. DataFrame을 SQLite3 데이터베이스에 저장 (테이블 이름은 'table1'으로 지정)
    df_csv.to_sql('table1', conn, if_exists='replace', index=False)

    # 12. 커넥션 종료
    conn.close()
```

#### 적금
```python
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
    csv_file_path = '/content/drive/MyDrive/merge2.csv'  # CSV 파일 경로 지정
    df2_csv = pd.read_csv(csv_file_path)

    # join_member 값에 따라 age_range 열 추가하는 함수 정의
    def determine_age_range(join_member):
        if "만14세이상" in join_member:
        return "14, 150"
        elif "만 17세 이상" in join_member:
            return "17, 150"
        elif "만19세이상" in join_member:  
            return "19, 150"
        elif "만19세~만34세" in join_member:
            return "19, 34"
        elif "만18세이상" in join_member:
            return "18, 150"
        elif "만 29세 이하" in join_member:
            return "0, 29"
        else:
            return "0, 150"

    # 10. age_range 열 추가
    df2_csv["age_range"] = df2_csv["join_member"].apply(determine_age_range)

    # 11. SQLite3 데이터베이스에 연결
    sqlite_db_path = '/content/drive/MyDrive/database2.db'  # SQLite3 데이터베이스 파일 경로를 지정
    conn = sqlite3.connect(sqlite_db_path)

    # 12. DataFrame을 SQLite3 데이터베이스에 저장 (테이블 이름은 'table2'으로 지정)
    df2_csv.to_sql('table2', conn, if_exists='replace', index=False)

    # 12. 커넥션 종료
    conn.close()
```

---

## 5. 서비스 대표 기능들에 대한 설명

### 🤖 **주요 기능 설명**
1. **금융 상품 추천**
   - 사용자 입력 데이터(연령, 관심사)를 기반으로 적합한 예적금 상품 추천.
2. **금리 비교**
   - 각 상품의 금리를 비교하여 최적의 선택을 돕는 기능.
3. **사용자 커스터마이징**
   - 사용자 프로필에 따라 맞춤형 정보 제공.
4. **연령 기반 필터링**
   - 상품의 가입 조건을 분석하여 나이 조건에 적합한 상품만 표시.

---

## 6. 생성형 AI를 활용한 부분

### ⚙️ **생성형 AI 활용**
- 금융 상품 데이터의 요약 및 추천 알고리즘에 AI 기술 활용.
- 사용자 입력 데이터를 분석하여 적합한 상품 카테고리 분류.

---

## 7. 기타

- **팀원 후기**

  - 🦊 조현희: "데이터베이스 설계와 API 연동을 통해 금융 데이터의 활용 가능성을 경험했습니다."


  - 🌟 강명주: "초보 사용자도 이해하기 쉬운 UI/UX를 설계하는 데 중점을 두었습니다."
