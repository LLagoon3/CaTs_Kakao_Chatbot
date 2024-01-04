import requests
import json



#### GET method Test ####

# url = 'https://test-project-d1903-default-rtdb.firebaseio.com/Test_Collection.json'
# url = 'https://heartsignal-cd7e8-default-rtdb.firebaseio.com/CPRDATA.json'
# response = requests.get(url)



#### POST method Test 1 ####

# url = 'http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu'
# data = {
#     'bot':'',
#     'action':{
#         'params':
#             {'date':'2024-01-02'},
#         'clientExtra': 
#             {'restaurant' : '한빛식당'}
#     },
#     'date': '2024-01-02',
#     # 'time': '점심',
#     # 'restaurant': '한빛식당',
# }
# response = requests.post(url, data = json.dumps(data))
# print(response.json())



#### POST method Test 2 ####

url = 'http://lagoon3.duckdns.org:20226/ocr/'
files = open('testimg.png', 'rb')
response = requests.post(url, files={'file': files})
print(response.json())



#### Firebase Test ####

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# cred = credentials.Certificate('/Volumes/lagoon3.duckdns.org/docker/code-sever/workspace/mini_project/django/serviceAccountKey.json')
# firebase_admin.initialize_app(cred,{
#     'databaseURL' : 'https://test-project-d1903-default-rtdb.firebaseio.com/' 
# })
# ref = db.reference() 
# ref.update({'data2' : {'id': 3}}) 

# ref = db.reference('data1')
# print(ref.get())


