from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Restaurant


# Create your views here.

class randomRecommend(View):
    def post(self, request):
        restaurant = Restaurant.objects.order_by('?').first()
        responseBody = {
              "version": "2.0",
                    "template": {"outputs": 
                         [
                         {'basicCard': 
                                  {"title": restaurant.restaurant,
                                    "thumbnail": 
                                       {"imageUrl": restaurant.img,
                                        "link": {"web": restaurant.img}         
                                       },
                                    "buttons": [
                                            {
                                                "action": "webLink",
                                                "label": "가게정보보기",
                                                "webLinkUrl": restaurant.url
                                            },
                                            {
                                                "action": "share",
                                                "label": "공유하기",
                                            }    
                                    ]
                                  }       
                             }             
                         ]
                    }
                }
        return JsonResponse(responseBody)
    