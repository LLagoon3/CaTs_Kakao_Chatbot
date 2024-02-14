from django.urls import path
from . import views

urlpatterns = [
    path('', views.testView.as_view()),
    path('faceDetection/', views.faceDetection.as_view()),
    path('pushNotification/', views.pushNotification.as_view()),
    path('pushNotificationToAll/', views.pushNotificationToAll.as_view()),
]