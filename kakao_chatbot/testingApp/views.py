from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
# from rest_framework import viewsets

# Create your views here.


class testView(View):
    def post(self, request):
        print("-"*40, "\nrequest : ", request)
        data = json.loads(request.body)   
        print(data)
        try:
            responseBody = {
                    #'식당': data['action']['clientExtra']['restaurant'],
                    '식당': data['action']['params']['test'],
                    '아침': '없음',
                    '점심': '없음',
                    '저녁': '없음',
            }
            return JsonResponse(responseBody)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    