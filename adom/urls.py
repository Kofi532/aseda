# musicapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_view, name='music_view'),
]
