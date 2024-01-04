# CaTs_Kakao_Chatbot

## CBNU Cafeteria Menu

### Parameter

- date : ‘YYYY:MM:DD’
- time : ‘아침’, ‘점심’, ‘저녁’, None
- restaurant : ‘한빛식당’, ‘별빛식당’, ‘은하수식당’, None

### Responses

```json
{'2023-12-29': [
	{'restaurant': '한빛식당', 
	'menu': {'아침': ['카레라이스,배추김치,계란후라이,미소장국'], 
	'점심': ['고추장칼국수,배추김치,쌀밥,떡갈비데리야끼조림'], 
	'저녁': ['미운영,']}}, 
	{'restaurant': '별빛식당', 
		'menu': {'점심': ['닭살데리야끼볶음,어묵무국,배추김치,요구르트,팽이버섯맛살전,오이쑥갓무침']}},
	{'restaurant': '은하수식당', 
		'menu': {'점심': ['표고버섯튀김&탕수육소스,요구르트,포기김치,계란파국,오징어볶음,통배추나물무침'], 
			'저녁': ['미운영,']}}
				]
}
```

### URL

```markup
http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu
```

### Http GET Method

```python
url = 'http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu?date=2023-12-29'
response = requests.get(url)
```

### Http POST Method

```python
url = 'http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu'
data = {
    'date': '2023-12-29',
    'time': '점심',
    'restaurant': '한빛식당',
}
response = requests.post(url, data = json.dumps(data))
```

## OCR

### Responses

```python
{
	"version": "2.0",
	"template": {
		"outputs": [
			{
				"simpleText": {
					"text": text
					}
				}
			]
		}
	}
```

### URL

```markdown
http://lagoon3.duckdns.org:20226/ocr/
```

### Http POST Method

```python
files = open('testimg.png', 'rb')
response = requests.post(url, files={'file': files})
```