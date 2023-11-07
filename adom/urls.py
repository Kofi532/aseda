# musicapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('solfa/', views.music_view, name='music_view'),
    path('trigger-action/', views.music_view, name='trigger_action'),
    path('all/', views.index, name='index'),
    path('all/base.html/', views.base, name='base'),
    path('handle-click/', views.handle_click, name='handle_click'),  # Maps /handle-click/ to handle_click view
    path('previous/', views.previous_view, name='previous_view'),

]
