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
    def userCheck(self, user_id):
        pending_user_ref = self.db.collection('ApprovedUsers').document(user_id)
        pending_user = pending_user_ref.get()
        if pending_user.exists: 
            print("Pending User Found")
            data = pending_user.to_dict()
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
            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        