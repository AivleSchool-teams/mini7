from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('detail/', views.detail, name='detail'),
    path('list/', views.list, name='list'),
    path('', views.board, name='board'),
]
