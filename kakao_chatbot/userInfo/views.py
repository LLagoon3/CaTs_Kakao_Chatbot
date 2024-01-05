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
        pass
    def authentication(self):
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    def setData(self, params):
        document = self.db.collection("PendingUsers").document(params["Request_id"])
        document.set(params)
    def userCheck(self, user_id):
        pending_user_ref = self.db.collection('ApprovedUsers').document(user_id)
        pending_user = pending_user_ref.get()
        if pending_user.exists:
            print("Pending User Found")
            data = pending_user.to_dict()
            user_name = data.get("Request_name")
            jsonBody = {
                            "version": "2.0",
                            "template": {
                                "outputs": [
                                    {
                                        "basicCard": {
                                            "title": "{}님 안녕하세요".format(user_name),
                                            "thumbnail": {
                                                "imageUrl": "https://avatars.githubusercontent.com/u/141043183?s=400&u=56efb37f8ba9145f99c5e5e19ba875986825d85c&v=4"
                                            },
                                            "buttons": [
                                                {
                                                    "action": "block",
                                                    "label": "OCR 시작하기",
                                                    "blockId": "652f32d7b3ba010afdf6e56d"
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
            return jsonBody
        else:
            jsonBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "CATS 회원이 아닙니다"
                            }
                        }
                    ]
                }
            }
            return jsonBody
        
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
            return JsonResponse({"message": "SUCCESS"}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        