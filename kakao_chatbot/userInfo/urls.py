from django.urls import path
from . import views

urlpatterns = [
    path('setName/', views.setNameView.as_view()),
    path('getId/', views.getIdView.as_view()),
]