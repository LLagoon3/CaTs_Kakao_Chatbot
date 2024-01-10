# from django.test import TestCase

# Create your tests here.
import requests
import json
data = {
  "intent": {
    "id": "iegps972h9ekjupmdjkwmo4j",
    "name": "블록 이름"
  },
  "userRequest": {
    "timezone": "Asia/Seoul",
    "params": {
      "ignoreMe": "true"
    },
    "block": {
      "id": "iegps972h9ekjupmdjkwmo4j",
      "name": "블록 이름"
    },
    "utterance": "발화 내용",
    "lang": None,
    "user": {
      "id": "951358",
      "type": "accountId",
      "properties": {}
    }
  },
  "bot": {
    "id": "6346135c30eb8c15211fa328",
    "name": "봇 이름"
  },
  "action": {
    "name": "o7m4md7a7c",
    "clientExtra": None,
    "params": {},
    "id": "hezxfcrboixoinfldoyffasg",
    "detailParams": {}
  }
}

url = 'http://chatbot.lagoon3.duckdns.org/ocr/ocrUserCheck/'
url = 'http://chatbot.lagoon3.duckdns.org/foodRecommend/random/'

response = requests.post(url, data = json.dumps(data))
print(response)


# from foodRecommend.models import Restaurant
# for i in range(0, len(restaurant_name_list)):
#   data_entry = Restaurant(restaurant=restaurant_name_list[i], url = restaurant_url_list[i], img = restaurant_image_list[i])
#   data_entry.save()
# print(Restaurant.objects.all())
