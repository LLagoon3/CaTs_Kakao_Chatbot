from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
import requests
from userInfo.views import FirebaseManager
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import messaging
from kakao_chatbot.settings import FACE_DETECTION_SERVER_URL
from kakao_chatbot.settings import FIREBASE_CREDENTIALS_PATH

# from rest_framework import viewsets

# Create your views here.


class testView(View):
    def post(self, request):
        # print("-"*40, "\nrequest : ", request)
        # data = json.loads(request.body)   
        # print(data)
        # try:
        #     responseBody = {
        #             #'식당': data['action']['clientExtra']['restaurant'],
        #             '식당': data['action']['params']['test'],
        #             '아침': '없음',
        #             '점심': '없음',
        #             '저녁': '없음',
        #     }
        #     return JsonResponse(responseBody)
        # except KeyError:
        #     return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        fb = FirebaseManager()
        fcm_token_dict = fb.getToken()
        print(fcm_token_dict.values())
        return JsonResponse(fcm_token_dict)

class faceDetection(View):
    def post(self, request):
        data = json.loads(request.body) 
        if 'get_img' not in data['action']['params'].keys(): return JsonResponse({'message': 'KEYERROR'})
        secure_urls_str = data['action']['params']['get_img']
        secure_urls_dict = json.loads(secure_urls_str)
        secure_urls = secure_urls_dict.get('secureUrls', '')
        if secure_urls.startswith('List(') and secure_urls.endswith(')'):
            secure_urls = secure_urls[5:-1]
        if not secure_urls:
            return JsonResponse({"error": "이미지 URL을 찾을 수 없습니다."})
        try:
            responseBody = {
                'url': secure_urls,
            }
            response = request.post(FACE_DETECTION_SERVER_URL, data = json.dumps(responseBody))
            if response.status_code == 200:
                JsonResponse({"val": ""})####
            else: 
                JsonResponse({'message': 'SERVER RESPONSE ERROR'})
        except:
            JsonResponse({'message': 'CANNOT CONNECT FACE_DETECTION_SERVER_URL'})

class pushNotification(View):
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
    def sendToFirebaseCloudMessaging(self, token):
        registration_token = token
        # See documentation on defining a message payload.
        message = messaging.Message(
            notification = messaging.Notification(
                title = 'it is title',
                body = 'code smell',
            ),
            token = registration_token,
        )
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return response
    def get(self, request):
        data = json.loads(request.body.decode('utf-8'))
        token = data['token']
        print("token" + token)
        response = self.sendToFirebaseCloudMessaging(token)
        print(response) 
        return JsonResponse({'response': "good:"})
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        token = data['token']
        print("token" + token)
        response = self.sendToFirebaseCloudMessaging(token)
        print(response) 
        return JsonResponse({'response': "good:"})
    
class pushNotificationToAll(View):
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        fb = FirebaseManager()
        fcm_token_dict = fb.getToken()
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=data['title'],
                body=data['contents']
            ),
            tokens=list(fcm_token_dict.values()),
        )
        response = messaging.send_multicast(message)
        print('{0} messages were sent successfully'.format(response.success_count))

        return JsonResponse({'sucess_count': response.success_count,
                             'failure_count': response.failure_count})
        