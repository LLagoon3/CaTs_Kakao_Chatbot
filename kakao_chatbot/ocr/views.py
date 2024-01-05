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
        return JsonResponse(self.firebaseManager(user_id))

        
        
        
        
        