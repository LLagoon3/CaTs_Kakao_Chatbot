from django.urls import path
from . import views

urlpatterns = [
    # path('', views.testView.as_view()),
    path('pushNotification/', views.pushNotificationView.as_view()),
]