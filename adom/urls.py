# musicapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_view, name='music_view'),
    path('trigger-action/', views.music_view, name='trigger_action'),
]
