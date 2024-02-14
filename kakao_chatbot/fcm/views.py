from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from userInfo.views import FirebaseManager
import firebase_admin
from firebase_admin import credentials, messaging
from kakao_chatbot.settings import FIREBASE_CREDENTIALS_PATH

class pushNotificationView(View):
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
    def multicastMessage(self, title, contents):
        fb = FirebaseManager()
        fcm_token_dict = fb.getToken()
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=contents
            ),
            tokens=list(fcm_token_dict.values()),
        )
        return messaging.send_multicast(message)
    def unicast(self, title, contents, token):
        message = messaging.Message(
            notification = messaging.Notification(
                title = title,
                body = contents,
            ),
            token = token,
        )
        return messaging.send(message)
    def get(self, request):
        title, contents, token = request.GET.get('title'), request.GET.get('contents'), request.GET.get('token')
        if token is not None:
            response = self.unicast(title, contents, token)
            print(response)
            return JsonResponse({'response': "good:"})
        elif (title is not None) and (contents is not None):
            response = self.multicastMessage(title, contents)
            print('{0} messages were sent successfully'.format(response.success_count))
            return JsonResponse({'sucess_count': response.success_count,
                                    'failure_count': response.failure_count})
        else:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        if 'token' in data:
            response = self.unicast(data['title'], data['contents'], data['token'])
            print(response)
            return JsonResponse({'response': "good:"})
        elif 'title' in data and 'contents' in data:
            response = self.multicastMessage(data['title'], data['contents'])
            print('{0} messages were sent successfully'.format(response.success_count))
            return JsonResponse({'sucess_count': response.success_count,
                                'failure_count': response.failure_count})
        else:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
# http://chatbot.lagoon3.duckdns.org/fcm/pushNotification/
# GET, POST 모두 가능
# 파라메터로 title, contents, token 존재 -> 지정된 토큰 값으로 유니캐스트
# 파라메터로 title, contents 존재 -> 파이어베이스 토큰 값으로 브로드캐스트