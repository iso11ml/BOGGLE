from django.shortcuts import redirect, render
import random
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Clase Del Trie Diccionario
class NodoTrie:
    def __init__(self):
        self.children = {}
        self.final_de_palabra = False
    

class Trie:
    def __init__(self):
        self.root = NodoTrie()

    def Insert(self, word):
        nodo_actual = self.root
        for char in word:
            if char not in nodo_actual.children:
                nodo_actual.children[char] = NodoTrie()
            nodo_actual = nodo_actual.children[char]
        nodo_actual.final_de_palabra = True

    def Delete(self, word):
        def eliminate_aux(node, word, depth):
            if depth == len(word):
                node.final_de_palabra = False
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            eliminar_nodo_actual = eliminate_aux(node.children[char], word, depth + 1)
            if eliminar_nodo_actual:
                del node.children[char]
            return len(node.children) == 0 and not node.final_de_palabra

        eliminate_aux(self.root, word, 0)

    def Search(self, word):
        nodo_actual = self.root
        for char in word:
            if char not in nodo_actual.children:
                return False
            nodo_actual = nodo_actual.children[char]
        return nodo_actual.final_de_palabra
    
    def Autocomplete(self, prefijo):
        def funcion_aux(node, path):
            if node.final_de_palabra:
                sugerencia.append("".join(path))
            for char, child_node in node.children.items():
                path.append(char)
                funcion_aux(child_node, path)
                path.pop()
        sugerencia = []
        nodo_actual = self.root
        for char in prefijo:
            if char not in nodo_actual.children:
                return sugerencia
            nodo_actual = nodo_actual.children[char]
        funcion_aux(nodo_actual, list(prefijo))
        return [suggestion[len(prefijo):] for suggestion in sugerencia]

# Para cargar el banco de palabras es necesario que el archivo este en la misma ruta que el código
# Se recomienda que tenga el mismo nombre '348713_BANCO_PALABRAS.txt'
    def Insertar_archivo(self):
        with open(finders.find('archivos/348713_BANCO_PALABRAS.txt'), 'r') as file:
            for line in file:
                word = line.strip()
                self.Insert(word)
trie = Trie()
trie.Insertar_archivo()
# Función Será Llamada desde boggle-board
def verificar_existencia(request, word):
    print(word)
    resultado = trie.Search(word)
    return JsonResponse({'existe': resultado})

# Página Principal
def home(request):
        return render(request, 'BASE/home.html')

# Página Del Juego
def boggle_board(request):
        vowels = ['A', 'E', 'I', 'O', 'U']
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        weights = [0.3 if letter in vowels else 0.7 / (len(alphabet) - len(vowels)) for letter in alphabet]
        board = [[random.choices(alphabet, weights=weights)[0] for j in range(18)] for i in range(8)]
        return render(request, 'BASE/main.html', {'board': board})

