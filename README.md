# CaTs_Kakao_Chatbot

## API : POST

`http://chatbot.lagoon3.duckdns.org/`

- `testingApp/` : 서버 응답 확인
- `cafeteriaMenu/` : 식당 기준 학식 메뉴(Sqlite3)
- `ocr/` : 이미지 OCR
- `userInfo/`
    - `setName/` : 사용자 등록(FireBase)
    - `getId/` : 사용자 이름으로 아이디 요청(FireBase)
- `web/` : 홈페이지 렌더
- `foodRecommend/`
    - `random/` : 음식점 랜덤 추천(Sqlite3)
- `karlo/` : 생성형 이미지
- `fcm/`
    - `pushNotification/` : fcm 서버 통신(FireBase)