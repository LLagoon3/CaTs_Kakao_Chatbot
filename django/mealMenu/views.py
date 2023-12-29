from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Menu
from django.utils import timezone
from django.views import View
from .crawling import Crawling
import json

def index(request):
    q_list = Menu.objects.filter(date = timezone.now())
    context = {'q_list': q_list}
    return render(request, 'mealMenu/question_list.html', context)


        
# def getMenu(request):
#     print(request)
#     putData()
#     print(timezone.localdate())
#     menu_list, res = Menu.objects.filter(date = timezone.localdate()), dict()
#     for menu in menu_list:
#         if menu.restaurant not in res.keys():
#             res[menu.restaurant] = []
#         res[menu.restaurant].append({menu.time: menu.menu})
#     return JsonResponse(res)

class MenuView(View):
    def get(self, request):
        param = {
            'date': request.GET.get('date', None),
            'time': request.GET.get('time', None),
            'restaurant': request.GET.get('restaurant', None), 
        }
        res = self.processParam(param)
        return JsonResponse(res)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            param = {
                'date': data.get('date', None),
                'time': data.get('time', None),
                'restaurant': data.get('restaurant', None),
            }
            res = self.processParam(param)
            return JsonResponse(res)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    
    def processParam(self, param):
        if param['date'] is None: return {"message": "KEY_ERROR"}
        filtered_param = {key: value for key, value in param.items() if value is not None}
        menu_obj_list, res = Menu.objects.filter(**filtered_param), dict()
        if not menu_obj_list.exists(): self.putData()
        for menu_obj in menu_obj_list:
            date = menu_obj.date.strftime("%Y-%m-%d") 
            if date not in res.keys(): res[date] = list()
            if not any(entry.get('restaurant') == menu_obj.restaurant for entry in res[date]):
                res[date].append({'restaurant': menu_obj.restaurant, 'menu':{}})
            for i in range(0, len(res[date])):
                if res[date][i]['restaurant'] == menu_obj.restaurant:
                    res[date][i]['menu'][menu_obj.time] = [menu_obj.menu]
                    break
        return res
    
    def putData(self):
        crawling_data = Crawling().parsingMenu()
        for data in crawling_data:
            if not Menu.objects.filter(date = data['date'], time = data['time'], restaurant = data['restaurant'], menu = data['menu']).exists():
                m = Menu(date = data['date'], time = data['time'], restaurant = data['restaurant'], menu = data['menu'])
                m.save()
    
               
            