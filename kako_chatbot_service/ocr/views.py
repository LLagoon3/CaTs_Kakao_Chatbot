from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import pytesseract
from PIL import Image

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