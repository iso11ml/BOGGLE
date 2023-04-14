from django.shortcuts import render
import random


# Página Principal
def home(request):
        return render(request, 'BASE/home.html')

# Página Del Juego
def boggle_board(request):
    board = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(18)] for i in range(8)]
    return render(request, 'BASE/game.html', {'board': board})

