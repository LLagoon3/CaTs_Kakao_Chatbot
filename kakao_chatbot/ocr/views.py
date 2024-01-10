from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import pytesseract
from PIL import Image
from userInfo.views import FirebaseManager
import json

# Create your views here.

class OcrView(View):
    def get(self, request):
        return JsonResponse({'message': 'REQUEST_ERROR'})
    def post(self, request):
        img = request.FILES.get('file')
        if img:
            text = pytesseract.image_to_string(Image.open(img), lang = 'eng+kor')
            print(text)
            responseBody = {
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
            return JsonResponse(responseBody)
        else:
            return JsonResponse({'message': 'KEY_ERROR'})

class OcrUserCheck(View):
    def __init__(self):
        self.firebaseManager = FirebaseManager()
    def post(self, request):
        data = json.loads(request.body)
        user_id = data['userRequest']['user']['id']
        user_check = self.firebaseManager.userCheck(user_id)
        if user_check[0]:
            jsonBody = {
                            "version": "2.0",
                            "template": {
                                "outputs": [
                                    {
                                        "basicCard": {
                                            "title": "{}님 안녕하세요".format(user_check[1]),
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
        return JsonResponse(jsonBody)

        
        
        
        
        