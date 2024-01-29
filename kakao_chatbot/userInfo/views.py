from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
import firebase_admin
from firebase_admin import credentials, firestore
from kakao_chatbot.settings import FIREBASE_CREDENTIALS_PATH

# Create your views here.

class FirebaseManager():
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
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
    def get(self, request):
        pass
    def post(self, request):
        data = json.loads(request.body)   
        try:
            params = {
                "Request_id" : data["userRequest"]["user"]["id"],
                "Request_name": data["action"]["params"]["Request_name"],
                "Request_number": data["action"]["params"]["Request_number"],
                "Request_text": data["action"]["params"]["Request_text"],
                "Request_field": data["action"]["params"]["Request_field"],
            }
            tmp = FirebaseManager()
            tmp.setData(params=params)
            reponseBody =  {
                      "version": "2.0",
                      "template": {
                        "outputs": [
                          {
                            "listCard": {
                              "header": {
                                "title": "확인 후 제출해주세요"
                              },
                              "items": [
                                {
                                  "title": "이름",
                                  "description": params["Request_name"],
                                  
                                },
                                {
                                  "title": "학번",
                                  "description": params["Request_number"],
                                  "extra": {
                                    "key1": "value1",
                                    "key2": "value2"
                                  }
                                },
                                {
                                  "title": "신청 이유",
                                  "description": params["Request_text"],
                                  "messageText": "Kakao i Voice Service",
                                  "extra": {
                                    "key1": "value1",
                                    "key2": "value2"
                                  }
                                },
                                 {
                                  "title": "관심 분야",
                                  "description": params["Request_field"],
                                  "messageText": "Kakao i Voice Service",
                                  "extra": {
                                    "key1": "value1",
                                    "key2": "value2"
                                  }
                                }
                              ],
                              "buttons": [
                                {
                                  "label": "제출하기",
                                  "action": "block",
                                  "blockId": "653508bc4bafae5aad4a01b7",
                                  "extra": {
                                    "key1": "value1",
                                    "key2": "value2"
                                  }
                                }
                              ]
                            }
                          }
                        ]
                      }
            }
            return JsonResponse(reponseBody, status=200)
        except KeyError:
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

            
        
        