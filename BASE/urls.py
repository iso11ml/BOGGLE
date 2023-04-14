from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('game/', views.boggle_board, name = "game"),
]
