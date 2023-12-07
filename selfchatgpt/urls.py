# blog/urls.py
from django.urls import path
from . import views

app_name = 'selfchatgpt'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('test', views.test, name='test'),
    path('page', views.page, name='page'),
    path('page2', views.page2, name='page2'),
    path('page3', views.page3, name='page3'),
]
