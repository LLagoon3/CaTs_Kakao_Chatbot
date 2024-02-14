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

data = {
  'token': 'f09N2BvkQqOgt4CU5Cyk8b:APA91bE8B1CRu2VBGTp1L1Zq7v0Mzj4ma1rATsPBzXl3y-tamjaWCmydHREvI8dD5rkXD38brwmip9D9aOw7qgZQYGtbtFJSRzmzoBSGeUTsaxjPEm9fkVTITKmPLvW5yffffCWdfTBf',
}
data = {
  'title': '김태완',
  'contents': '머함?',
  'token': 'f09N2BvkQqOgt4CU5Cyk8b:APA91bE8B1CRu2VBGTp1L1Zq7v0Mzj4ma1rATsPBzXl3y-tamjaWCmydHREvI8dD5rkXD38brwmip9D9aOw7qgZQYGtbtFJSRzmzoBSGeUTsaxjPEm9fkVTITKmPLvW5yffffCWdfTBf'
}
# url = 'http://chatbot.lagoon3.duckdns.org/ocr/ocrUserCheck/'
# url = 'http://chatbot.lagoon3.duckdns.org/foodRecommend/random/'
url = 'http://chatbot.lagoon3.duckdns.org/fcm/pushNotification/'
response = requests.post(url, data = json.dumps(data))
data = json.loads(response.content.decode('utf-8'))
print('sucess_count : ' + str(data['sucess_count']) + '   failure_count : ' + str(data['failure_count']))



# from foodRecommend.models import Restaurant
# for i in range(0, len(restaurant_name_list)):
#   data_entry = Restaurant(restaurant=restaurant_name_list[i], url = restaurant_url_list[i], img = restaurant_image_list[i])
#   data_entry.save()
# print(Restaurant.objects.all())
#ifdata.keys


# response = requests.get(url, params=data)

# 응답 확인
if response.status_code == 200:
    print('GET request successful')
    print('Response:', response.text)