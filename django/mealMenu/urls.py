from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('getMenu/Menu', views.MenuView.as_view()),
    path('getMenu/ChatBot', views.MenuView.as_view()),
]