from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
import firebase_admin
from firebase_admin import credentials, firestore
from kakao_chatbot.settings import FIREBASE_CREDENTIALS_PATH, SCHEDULE_TIME
from firebase_admin import messaging
import json
from datetime import datetime, timedelta


# Create your views here.

class FirebaseManager():
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    # @staticmethod
    # def parsingDatetime(date, time):
    #     date_list = list(map(int, date.split('-')))
    #     time_list = [int(time[-5:-3]), int(time[-2:])]
    #     if time[0:2] == "오후":time_list[0] = time_list[0] + 12
    #     return date_list + time_list
    # @staticmethod
    # def formattingDatetime(date_time_list):
    #     date_list, time_list = date_time_list[:3], date_time_list[3:]
    #     date, time = '', ''
    #     for tmp in date_list: date += str(tmp) + '-'
    #     if time_list[0] > 12: time = '오후 ' + str((time_list[0] - 12)).zfill(2)
    #     else: time = '오전 '+ str((time_list[0] )).zfill(2) 
    #     date, time = date[:-1], time + ':' + str(time_list[1]).zfill(2)
    #     return date, time
    # @staticmethod
    # def getCurrentTime():
    #     from datetime import datetime
    #     now = datetime.now()
    #     return {'min_time': [now.year, now.month, now.day, now.hour, now.minute - 5],
    #             'now_time': [now.year, now.month, now.day, now.hour, now.minute],
    #             'max_time': [now.year, now.month, now.day, now.hour, now.minute + 5]}
    def authentication(self):
        pass
    def setData(self, params):
        document = self.db.collection("PendingUsers").document(params["Request_id"])
        document.set(params)
    def getId(self, user_name):
        pending_user_ref = self.db.collection('PendingUsers')
        query = pending_user_ref.where('Request_name', '==', user_name).limit(1)
        try:
            return next(query.stream()).id
        except StopIteration:
            return None
    def getToken(self, params = None, collection = "KAKAO"):#params : fcm_Token을 쿼리할 유저 이름 리스트
        users_ref = self.db.collection(collection)
        query_ref = users_ref.where("fcmToken", "!=", "").stream()
        fcm_token_dict = {}
        if params is None:
          for doc in query_ref:
            user_data = doc.to_dict()
            fcm_token_dict[doc.id] = user_data.get("fcmToken")
        else:
          for doc in query_ref:
            user_data = doc.to_dict()
            if doc.id in params:
              fcm_token_dict[doc.id] = user_data.get("fcmToken")
        return fcm_token_dict
    def getSchedule(self):
        from scheduler.views import TimeManager
        schedule_ref =  self.db.collection("PromisePlace").get()
        schedule_dict_list = []
        for doc in schedule_ref:
            doc_dict = doc.to_dict()
            schedule_datetime = TimeManager.parsingDatetime(doc_dict['date'], doc_dict['time'])
            current_datetime = TimeManager.getCurrentTime(schedule_time=SCHEDULE_TIME)
            print("sch Time : ", schedule_datetime)
            print("cur Time : ", current_datetime)
            if (schedule_datetime >= current_datetime['min_time'] and schedule_datetime <= current_datetime['max_time']):
                schedule_dict_list.append(doc_dict)
        return schedule_dict_list
    def userCheck(self, user_id):
        approved_user_ref = self.db.collection('ApprovedUsers').document(user_id)
        approved_user = approved_user_ref.get()
        if approved_user.exists: 
            print("Pending User Found")
            data = approved_user.to_dict()
            user_name = data.get("Request_name")
            return [True, user_name]
        else:
            return [False, '']
        
class setNameView(View):
    def __init__(self) -> None:
        self.fm = FirebaseManager()
    def get(self, request):
        pass
    def post(self, request):
        data = json.loads(request.body)   
        try:
            datetime = json.loads(data["action"]["params"]["Request_birth"])
            datetime = datetime["value"]

            print(data)
            params = {
                "Request_id":  data["userRequest"]["user"]["id"],
                "Request_name": data["action"]["params"]["Request_name"],
                "Request_student_id": data["action"]["params"]["Request_student_id"],
                "Request_interest": data["action"]["params"]["Request_interest"],
                "Request_motivation": data["action"]["params"]["Request_motivation"],
                "Request_birth": datetime,
                "Request_phone_number": data["action"]["params"]["Request_phone_number"],
                "Request_gender" : data["action"]["params"]["Request_gender"],
            }
            fb = FirebaseManager()
            fb.setData(params=params)
            # reponseBody =  {
            #           "version": "2.0",
            #           "template": {
            #             "outputs": [
            #               {
            #                 "listCard": {
            #                   "header": {
            #                     "title": "확인 후 제출해주세요"
            #                   },
            #                   "items": [
            #                     {
            #                       "title": "이름",
            #                       "description": params["Request_name"],
                                  
            #                     },
            #                     {
            #                       "title": "학번",
            #                       "description": params["Request_student_id"],
            #                       "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     },
            #                     {
            #                       "title": "신청 이유",
            #                       "description": params["Request_interest"],
            #                       "messageText": "Kakao i Voice Service",
            #                       "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     },
            #                      {
            #                       "title": "지원 동기",
            #                       "description": params["Request_motivation"],
            #                       "messageText": "Kakao i Voice Service",
            #                       "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     },
            #                     {
            #                       "title": "생년월일",
            #                       "description": datetime,
            #                       "messageText": "Kakao i Voice Service",
            #                       "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     },
            #                     # {
            #                     #   "title": "전화번호",
            #                     #   "description": params["Request_phone_number"],
            #                     #   "messageText": "Kakao i Voice Service",
            #                     #   "extra": {
            #                     #     "key1": "value1",
            #                     #     "key2": "value2"
            #                     #   }
            #                     # },
            #                     # {
            #                     #   "title": "성별",
            #                     #   "description": params["Request_gender"],
            #                     #   "messageText": "Kakao i Voice Service",
            #                     #   "extra": {
            #                     #     "key1": "value1",
            #                     #     "key2": "value2"
            #                     #   }
            #                     # }
            #                   ],
            #                   "buttons": [
            #                     {
            #                       "label": "제출하기",
            #                       "action": "block",
            #                       "blockId": "653508bc4bafae5aad4a01b7",
            #                       "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     },
            #                     {
            #                         "label": "재제출",
            #                         "action":"block",
            #                         "blockId":"6510e5b76faba427636621b1",
            #                         "extra": {
            #                         "key1": "value1",
            #                         "key2": "value2"
            #                       }
            #                     }
            #                   ]
            #                 }
            #               }
            #             ]
            #           }
            # }
            reponseBody = {
                  "version": "2.0",
                  "template": {
                      "outputs": [
                          {
                              "itemCard": {
                                  "imageTitle": {
                                      "title": "확인 후 제출해주세요",
                                      "description": ""
                                  },
                                  "title": "",
                                  "description": "",
                                  "thumbnail": {
                                      "imageUrl": "https://i.ibb.co/bvS3b7w/cats-logo-bg-800x2.png",
                                      "width": 800,
                                      "height": 800
                                  },
                                  "profile": {
                                      "title": "CATS",
                                      "imageUrl": "https://i.ibb.co/bvS3b7w/cats-logo-bg-800x2.png"
                                  },
                                  "itemList": [
                                      {
                                          "title": "이름",
                                          "description": params["Request_name"]
                                      },
                                      {
                                          "title": "학번",
                                          "description": params["Request_student_id"]
                                      },
                                      {
                                          "title": "관심 분야",
                                          "description": params["Request_interest"]
                                      },
                                      {
                                          "title": "지원 동기",
                                          "description": params["Request_motivation"]
                                      },
                                      {
                                          "title": "생년월일",
                                          "description": datetime
                                      },
                                      {
                                          "title": "전화번호",
                                          "description": params["Request_phone_number"]
                                      },
                                      {
                                          "title": "성별",
                                          "description": params["Request_gender"]
                                      },
                                  ],
                                  "itemListAlignment" : "right",
                                  # "itemListSummary": {
                                  #     "title": "Total",
                                  #     "description": "$4,032.54"
                                  # },
                                  "buttons": [
                                    {
                                      "label": "제출하기",
                                      "action": "block",
                                      "blockId": "653508bc4bafae5aad4a01b7",
                                      # "extra": {
                                      #   "key1": "value1",
                                      #   "key2": "value2"
                                      # }
                                    },
                                    {
                                        "label": "재제출",
                                        "action":"block",
                                        "blockId":"6510e5b76faba427636621b1",
                                      #   "extra": {
                                      #   "key1": "value1",
                                      #   "key2": "value2"
                                      # }
                                    }
                                  ],
                                  "buttonLayout" : "horizontal"
                              }
                          }
                      ]
                  }
              }
            from fcm.views import pushNotificationView
            admin_docs = self.fm.db.collection('admin').get()
            admin_uids = []
            for doc in admin_docs:
                doc = doc.to_dict()
                admin_uids.append(doc['id'])
            print(pushNotificationView.multicastMessage("신규 회원 등록", data["action"]["params"]["Request_name"], 
                                                        fcm_token = self.fm.getToken(params=admin_uids,
                                                                                     collection = "KAKAO")))
            return JsonResponse(reponseBody, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class getIdView(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['action']['params']['name']
        tmp = FirebaseManager()
        user_id = tmp.getId(name)
        if user_id is not None:
            return JsonResponse({'id': user_id})
        else:
            return JsonResponse({'message': 'KEY ERROR'})
        

            
        
        