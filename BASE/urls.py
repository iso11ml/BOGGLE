from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = "home"),
    path('game/', views.boggle_board, name = "game"),
    path('verificar-existencia/<str:word>/', views.verificar_existencia, name = 'verificar-existencia'),
    path('wordsFound/', views.eliminate_heap, name = "eliminateHeap"),
]


