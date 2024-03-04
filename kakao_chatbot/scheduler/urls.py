from django.urls import path
from . import views

urlpatterns = [
    path('createSchedule/', views.schedulerView.as_view()),
]