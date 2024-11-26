# Final_PJT

## 1. 프로젝트 및 팀원 소개

### 📋 **프로젝트 소개**
**초보자를 위한 예적금 추천 서비스**

![StarPot_logo_ai](https://github.com/user-attachments/assets/f19a70e4-bd01-4f08-a0fc-f372ee3ec2bd)

### 📌 **프로젝트 개요**
**🌟 StarPot 이란??**

작은 별을 저금통(Pot)에 담듯이, 당신의 금융 성장을 돕습니다.

금융에 대해 알아가고 싶지만, 어려운 내용 때문에 포기하신 적 많지 않나요?

<img src="https://github.com/user-attachments/assets/50d2b082-23bb-4d35-99e2-9966f4cd4f05"  width="200" height="200"/>

StarPot은 금융 초보자를 대상으로 예적금 상품을 추천하는 서비스입니다.  
어렵고 복잡한 금융 용어와 내용을 배제하고, 간단하고 이해하기 쉬운 정보를 제공합니다.  

**👫 누구를 위한 서비스인가요?**

- 10대~30대의 금융 초보자
  
  "어떤 예적금 상품을 선택해야 할지 모르겠어요!"
  
  "금융 용어가 너무 어렵고 복잡해요!"
  
  "같은 상품인데 조건마다 금리가 많아서 어려워요!"



--

  
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
- **프론트엔드**: Vue 3, Bootstrap
- **API**: 금융감독원 API, 카카오맵 API, 한국수출입은행 환율 API
- **협업 툴**: Notion, Git, Google Colab
- **기타**: 생성형 AI (초보자를 위한 금융 지식 알리미)

---

## 2. 설계 내용(아키텍처 등) 및 실제 구현 정도

### 🔍 **설계 및 구현**
- **아키텍처 설계**
1. **데이터 수집 및 저장**
   - 금융감독원 API로 예적금 상품 데이터 사용
   - 데이터를 가공하여 나이 제한(`age_range`), 이자율 비교(`intr_rate`), 가입 조건(`join_member`) 등의 필드를 추가
   - SQLite 데이터베이스에 저장하여 API 호출을 줄이고 빠르게 데이터 제공.

2. **추천 알고리즘**
   - 사용자가 입력한 연령, 원하는 조건 등의 정보를 기반으로 상품 데이터 필터링

3. **클라이언트-서버 통신**
   - 클라이언트(Vue 3)는 Axios를 사용해 백엔드와 통신.
   - 백엔드(Django)는 필터링된 금융 상품 데이터를 JSON 형식으로 반환.
   - 프론트엔드는 JSON 데이터를 받아 화면에 렌더링.

- **구현 수준**
  - 주요 기능 완성: 예적금 추천 알고리즘, 주변 은행 찾기, 환율 계산기, 금융 초보자를 위한 챗봇 등




---

## 3. 서비스 대표 기능


| **기능**              | **설명**                                                                                           |
|------------------------|---------------------------------------------------------------------------------------------------|
| **예적금 추천 페이지**         | 쉽고 간단한 질문으로 사용자에게 답변을 받아 추천 상품 제공                                                    |
| **예적금 전체 상품 조회 페이지** | - 예적금 상품의 전체 리스트 보기<br> -각 상품의 금리 별로 상세페이지를 제공하여 유저 간 정보 공유 및 소통 가능<br> - 전체, 금리순, 좋아요순, 은행명순으로 상품을 찾아볼 수 있게 필터 기능 제공 |
| **주변 은행 검색**      | 위치 기반 서비스로 내 주변 은행 찾기                                                                       |
| **똑!똑! 게시판**       | - 관리자 공지<br> - 금융 초보자에게 필요한 금융 지식을 친절한 아티클로 전달                                                     |
| **환율 계산기**         | 사용자 정보와 관심사에 따른 상품 관리 및 조회                                                                 |
| **챗봇 서비스**         | 초보자에게 금융 지식을 쉽게 알려주는 챗봇 서비스.                                                               |
| **마이 페이지**         | - 프로필 관리(개인정보 수정, 비밀번호 변경)<br> - 내가 좋아요한 상품(예금, 적금) 및 좋아요한 상품의 금리 비교 그래프 제공<br> - 내가 댓글 단 상품(예금, 적금)           |
| **회원가입/로그인/로그아웃** | 사용자 맞춤 서비스를 제공하기 위해 회원 기능 제공                                                                   |

** **


### 서비스 화면

--

**메인화면**

<img width="1432" alt="스크린샷 2024-11-26 오후 10 50 34" src="https://github.com/user-attachments/assets/d609aa9c-6ebe-4017-9e71-0c0c88229191">

- BootStrap의 Carousel로 주요 서비스로 이동

- 로그인 시, 마이페이지, 로그아웃 버튼이 뜸 /  주요 기능 사용 가능

- 로그인을 하지 않으면 주요 기능 클릭 시, 로그인 창으로 이동


--

**예적금 추천 서비스**
<img width="1433" alt="스크린샷 2024-11-26 오후 10 52 02" src="https://github.com/user-attachments/assets/bf14f8ac-124e-4554-961a-e7ecbac8a17f">

--

**예적금 추천 화면**
<img width="1429" alt="스크린샷 2024-11-26 오후 10 51 27" src="https://github.com/user-attachments/assets/35d32051-39a7-4973-92da-9caf21662a04">

--

**예적금 추천 결과 화면**
<img width="1429" alt="스크린샷 2024-11-26 오후 10 51 45" src="https://github.com/user-attachments/assets/0c2bb265-d857-4022-8430-ad2fabe7e0a8">

- 추천 지수 제공
  
- Detail로 상품 상세 페이지로 이동

--

**예적금 전체 상품 리스트 서비스**
<img width="1432" alt="스크린샷 2024-11-26 오후 10 52 13" src="https://github.com/user-attachments/assets/3acc53b2-3723-4cbb-ba33-00c80d3d5714">

- 예금, 적금 상품 전체보기

- 전체, 금리순, 좋아요순, 은행명순 제공

--

**예적금 상품 상세 정보**
<img width="1427" alt="스크린샷 2024-11-26 오후 10 56 14" src="https://github.com/user-attachments/assets/fdb58fea-d4ad-4161-b08f-7dee652beb79">
- 각 상품마다 좋아요, 댓글 기능 구현

--

**주변 은행 찾기**
<img width="1431" alt="스크린샷 2024-11-26 오후 10 52 29" src="https://github.com/user-attachments/assets/daadf644-88e2-4cc5-85be-0d001c8c4a42">

- 위치기반 서비스로 내 주변 은행 찾기
  
<img width="961" alt="스크린샷 2024-11-26 오후 10 52 43" src="https://github.com/user-attachments/assets/da3344fe-b83b-4d69-a80e-a669ef4e3825">

- 은행명 외의 단어를 검색하면 경고창이 뜸

--

**똑! 똑! 게시판**
<img width="1432" alt="스크린샷 2024-11-26 오후 10 54 56" src="https://github.com/user-attachments/assets/b9bc7ceb-e907-4d1f-92c1-312db085c2cb">

- 사이트 공지사항 및 초보자를 위한 금융 아티클 제공

--

**환율 계산기**
  <img width="1429" alt="스크린샷 2024-11-26 오후 10 53 16" src="https://github.com/user-attachments/assets/2e12f582-f879-4b14-afd2-dbddf70abf50">
- 반응형을 제공하여 실시간으로 입력하면서 환율 계산 확인가능

--

**챗봇 기능**
<img width="1432" alt="스크린샷 2024-11-26 오후 10 54 16" src="https://github.com/user-attachments/assets/5983902b-8cc3-4663-ba59-43f03d994724">
- 금융 용어를 모르는 초보자를 위해 챗봇 서비스 제공

**마이페이지**
<img width="1428" alt="스크린샷 2024-11-26 오후 10 55 12" src="https://github.com/user-attachments/assets/281e6426-d75e-42d0-b245-cc8505b4b9cf">
- 내 프로필, 좋아요한 상품, 내가 단 댓글 확인 가능
  
<img width="1433" alt="스크린샷 2024-11-26 오후 10 56 30" src="https://github.com/user-attachments/assets/ccce8e22-3a98-4e9d-83ea-329c44afbb84">

<img width="1433" alt="스크린샷 2024-11-26 오후 10 55 44" src="https://github.com/user-attachments/assets/d87903c4-c7b1-4b51-8cf3-2327ffda1e17">
- 좋아요한 예적금 금리 비교가능
  

---

## 4. 데이터베이스 모델링(ERD) 및 Vue 컴포넌트 구성

### 📊 **데이터베이스 모델링**
![StarPot_ERD](https://github.com/user-attachments/assets/99d6d156-1246-4f66-b8d9-1b16072de7cf)

### 🧚 **Vue 컴포넌트**
![KakaoTalk_Photo_2024-11-26-19-37-57](https://github.com/user-attachments/assets/0f4cefbf-0f9e-4128-8cb3-013ff464f63b)

---

## 5. 금융 상품 추천 알고리즘에 대한 기술적 설명

  사용자의 답변에 따라 적합한 상품에 가중치를 부여하고, 가중치가 높은 순으로 추천 상품을 제공합니다.

  데이터 필터링을 위해 테이블을 먼저 구성했으며, 구글 코랩을 사용해서 DB 테이블을 구현했습니다. 


  - 과정
  1. 금융감독원 API로 예금, 적금 데이터 가져오기
  2. pandas를 사용해 필요한 데이터만 사용하여 DB 테이블 구성(구글 코랩)
  3. DB 테이블을 Json으로 변경하여 Django에서 데이터 사용



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



## 6. 생성형 AI를 활용한 부분

### ⚙️ **생성형 AI 활용**

***친절한 금융 어시스턴트***

StarPot 서비스에서는 생성형 AI를 활용하여 금융 초보자들이 보다 쉽게 금융 지식을 습득하고, 적합한 예적금 상품을 탐색할 수 있도록 도와주는 챗봇 어시스턴트를 구현했습니다.


1. 금융 초보자가 궁금한 점을 물어보면 친절하고 전문적인 답변을 제공
   
  - 쉬운 용어와 간단한 설명을 통해 초보자의 이해를 돕기
    
  - 예금, 적금 상품 추천 시 핵심 정보만 제공하여 정보 과부하를 방지

2. 답변 가이드라인
  - 마크다운 형식을 적극 활용하여 깔끔하고 보기 쉬운 답변 제공
    
  - 사용자의 질문을 분석해 금융 관련 질문에만 답변하며, 비금융 질문에 대해서는 친절히 안내
    
  - 질문자의 수준을 고려해 초보자 친화적인 답변 제공
    

🌟 예시

사용자가 챗봇에게 "적금과 예금의 차이가 무엇인가요?"를 물었을 때, 챗봇은 다음과 같은 답변을 제공합니다

```markdown
## 적금과 예금의 차이

1. **예금**: 
   - 목돈을 한 번에 맡기고, 정해진 기간 후 이자를 더해 돌려받는 방식입니다.
   - *예시*: 1,000만 원을 1년간 맡겨 2%의 이자를 받음.

2. **적금**: 
   - 매달 일정 금액을 모아 저축하며, 만기 시 원금과 이자를 받는 방식입니다.
   - *예시*: 매달 10만 원씩 1년간 적립해 이자를 받음.

### 어떤 경우에 적합할까요?
- **예금**: 이미 목돈이 준비되어 있다면 적합.
- **적금**: 꾸준히 돈을 모으고 싶다면 적합.
```

---

## 7. 후기

- **팀원 후기**

  - 🦊 조현희

: "금융 데이터를 직접 전처리를 하고, 이를 활용하여 사용자 맞춤형 예적금 상품 추천 알고리즘을 설계하였습니다. 금융 데이터가 생각보다 복잡해서 이 데이터를 전처리 하는데 많은 시간이 소요되었습니다. 하지만 처음부터 꼼꼼하게 금융 데이터를 분석한 덕분에 예적금 추천 서비스가 생각보다 쉽게 구현되었습니다. 그리고 이 프로젝트를 통해서 api를 활용하는 것이 어렵다는 것을 깨달았습니다. 금융 예적금 api,  데이터베이스 설계와 API 연동을 통해 금융 데이터의 활용 가능성을 경험했습니다."


  - 🌟 강명주

: "개발의 전반적인 과정을 훑는 기회가 되었습니다. 백엔드와 프론트엔드는 어떻게 통신하는 지, API를 불러오는 것조차 어려워했는데 프로젝트를 통해 아~ 이런식으로 하는 거구나하고 알게 되었습니다. 더불어 페어가 아니었으면 짧은 시간에 이정도 퀄리티의 프로젝트를 구현하지 못했을 것입니다. 이 자리를 빌려 페어에게 진심으로 감사하다고 전합니다.:)"
