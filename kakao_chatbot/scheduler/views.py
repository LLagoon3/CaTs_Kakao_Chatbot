from typing import Any
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from userInfo.views import FirebaseManager
from fcm.views import pushNotificationView
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from datetime import datetime, timedelta
import json
from kakao_chatbot.settings import SCHEDULE_TIME
# Create your views here.

# sched = BackgroundScheduler()
# sched.start()

print('sched started')

class TimeManager():
    @staticmethod
    def parsingDatetime(date, time):
        date_list = list(map(int, date.split('-')))
        time_list = [int(time[-5:-3]), int(time[-2:])]
        if time[0:2] == "오후":time_list[0] = time_list[0] + 12
        return date_list + time_list
    @staticmethod
    def formattingDatetime(date_time_list):
        date_list, time_list = date_time_list[:3], date_time_list[3:]
        date, time = '', ''
        for tmp in date_list: date += str(tmp) + '-'
        if time_list[0] > 12: time = '오후 ' + str((time_list[0] - 12)).zfill(2)
        else: time = '오전 '+ str((time_list[0] )).zfill(2) 
        date, time = date[:-1], time + ':' + str(time_list[1]).zfill(2)
        return date, time
    @staticmethod
    def getCurrentTime(schedule_time = 0):
        from datetime import datetime
        now = datetime.now()
        return {'min_time': TimeManager.convertDatetimeTolist(now + timedelta(minutes = (schedule_time - 5))),
                'now_time': TimeManager.convertDatetimeTolist(now + timedelta(minutes = (schedule_time))),
                'max_time': TimeManager.convertDatetimeTolist(now + timedelta(minutes = (schedule_time + 5)))}
    @staticmethod
    def convertDatetimeTolist(datetime_):
        return [datetime_.year, datetime_.month, datetime_.day, datetime_.hour, datetime_.minute]

class ScheduleManager():
    def __init__(self) -> None:
        pass
    @staticmethod
    def fcmSchedule():
        fm = FirebaseManager()
        schedul_dict_list = fm.getSchedule()
        return_data = {}
        if schedul_dict_list == []:
            return JsonResponse({'message': 'NO SCHEDULE DATA'})
        for schedul_dict in schedul_dict_list:
            if 'friends' not in list(schedul_dict.keys()):
                return JsonResponse({'message': 'NO SCHEDULE-FRIENDS DATA'})
            friends_list = schedul_dict['friends']
            friends_token_dict = fm.getToken(friends_list)
            response = pushNotificationView.multicastMessage(schedul_dict['fcmTitle'], schedul_dict['fcmContents'], friends_token_dict)
            print('sucess_count', response.success_count)
            return_data[schedul_dict['fcmTitle']] = response.success_count
        return JsonResponse({'sucess_count': response.success_count})
    @staticmethod
    def updateSchedule(date, time):
        sched = BackgroundScheduler()
        print(date, time)
        datetime_list = TimeManager.parsingDatetime(date, time)
        datetime_list = datetime(*datetime_list) - timedelta(minutes=SCHEDULE_TIME)
        print('datetime : ', datetime_list)
        sched.add_job(ScheduleManager.fcmSchedule, 
                      trigger=DateTrigger(run_date=datetime_list),
                      id=str(datetime_list))
        register_events(sched)
        sched.start()
        print(sched.get_jobs())
        pass
    
class schedulerView(View):
    def get(self, request):
        date, time = request.GET.get('date'), request.GET.get('time')
        ScheduleManager.updateSchedule(date, time)
    def post(self, request):
        data = json.loads(request.body)
        ScheduleManager.updateSchedule(data['date'], data['time'])
        print("UPDATE_SCHEDULER")
        return JsonResponse({"Message": "UPDATE_SCHEDULER"})