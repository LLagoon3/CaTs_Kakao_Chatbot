from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from kakao_chatbot.settings import KAKAOBRAIN_KEY_PATH
import json
import requests
import base64
from PIL import Image
import io

with open(KAKAOBRAIN_KEY_PATH, 'r') as f: REST_API_KEY = json.load(f)['key']
# Create your views here.

class karloView(View):
    def variations(image):
        r = requests.post(
            'https://api.kakaobrain.com/v2/inference/karlo/variations',
            json = {
                'image': image
            },
            headers = {
                'Authorization': f'KakaoAK {REST_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        response = json.loads(r.content)
        return response
    def imageToString(img):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return my_encoded_img
    def post(self, request):
        data = json.loads(request.body)
        secure_urls_str = data['action']['params']['karlo']
        secure_urls_dict = json.loads(secure_urls_str)
        secure_urls = secure_urls_dict.get('secureUrls', '')
        if secure_urls.startswith('List(') and secure_urls.endswith(')'):
            secure_urls = secure_urls[5:-1]
        if not secure_urls:
            return JsonResponse({'message': 'CANNOT FIND IMG URL'})
        response = requests.get(secure_urls)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            print(img.format)
            img_base64 = self.imageToString(img)
            response = self.variations(img_base64)
            image_url = response['images'][0]['image']
            responseBody = {
                            "version": "2.0",
                            "template": {
                                "outputs": [
                                    {
                                        "simpleImage": {
                                            "imageUrl": f'{image_url}',
                                            
                                        }
                                    }
                                ]
                            }
                        }
            return JsonResponse(responseBody)
        else:
            return JsonResponse({'message': 'IMGURL CONNECTION ERROR'})