from django.shortcuts import redirect, render
import random
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Función Que Asigna Los Puntos De Cada Palabra
def wordPuntuation(word):
    if len(word) == 2:           
        score = 2
    elif len(word) == 3:
        score = 3
    elif len(word) == 4:
        score = 4
    elif len(word) == 5:
        score = 6
    elif len(word) == 6:
        score = 7
    elif len(word) == 7:
        score = 8
    elif len(word) == 8:
        score = 9
    elif len(word) > 9:
        score = 18
    
    return score

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


# Heap Para Almacenar La Palabra De Mayor Puntaje           
import math

# Creación del árbol
class FibonacciTree:
    def __init__(self, value, word):
        self.value = value
        self.word = word
        self.child = []
        self.order = 0

    # Se adiciona el nuevo árbol al conjunto de árboles
    def add_at_end(self, t):
        self.child.append(t)
        self.order = self.order + 1

# Creando el heap 
class FibonacciHeap:
    def __init__(self):
        self.trees = []
        self.greatest = None
        self.count = 0

    # Insert a node
    def insert_node(self, value, word):
        new_tree = FibonacciTree(value, word)
        self.trees.append(new_tree)
        if (self.greatest is None or value > self.greatest.value):
            self.greatest = new_tree
        self.count = self.count + 1

    # Obtener el máximo
    def get_max(self):
        if self.greatest is None:
            return None
        return self.greatest.word, self.greatest.value

    # Extraer el máximo
    def extract_max(self):
        largest = self.greatest
        if largest is not None:
            for child in largest.child:
                self.trees.append(child)
            self.trees.remove(largest)
            if self.trees == []:
                self.greatest = None
            else:
                self.greatest = self.trees[0]
                self.consolidate()
            self.count = self.count - 1
            return largest.word, largest.value

    # Consolidación de la raíz
    def consolidate(self):
        aux = (floor_log(self.count) + 1) * [None]

        while self.trees != []:
            x = self.trees[0]
            order = x.order
            self.trees.remove(x)
            while aux[order] is not None:
                y = aux[order]
                if x.value < y.value:
                    x, y = y, x
                x.add_at_end(y)
                aux[order] = None
                order = order + 1
            aux[order] = x

        self.greatest = None
        for k in aux:
            if k is not None:
                self.trees.append(k)
                if (self.greatest is None or k.value > self.greatest.value):
                    self.greatest = k

    # Muestra las raices así como el orden
    def display_roots(self):
        if self.trees:
            print("Raices:")
            for tree in self.trees:
                print(f"{tree.word}: {tree.value} ({tree.order})")
        else:
            print("El heap Fibonacci está vacío")

def floor_log(x):
    return math.frexp(x)[1] - 1

#Tabla Hash
import math
class Node:
    def __init__(self, palabra, puntaje):
        self.palabra = palabra
        self.puntaje = puntaje
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, palabra, puntaje):
        new_node = Node(palabra, puntaje)
        new_node.next = self.head
        self.head = new_node

    def search(self, palabra):
        current = self.head
        while current:
            if current.palabra == palabra:
                return current
            current = current.next
        return None

    def delete(self, palabra):
        current = self.head
        prev = None

        while current:
            if current.palabra == palabra:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next

        return False


class HashTable:
    def __init__(self, size = 200):
        self.size = size
        self.table = [LinkedList() for _ in range(self.size)]
    def hash_function(self, palabra):
        def custom_hash(word, value = 200):
            numberPrime1 = 31
            numberPrime2 = 51
            hash_sum = 0
            for i, char in enumerate(word):
                char_code = ord(char)
                if i % 2 == 0:
                    hash_sum += char_code * numberPrime1
                else:
                    hash_sum += char_code * numberPrime2
            aureo = (5 ** 0.5 - 1) / 2
            return int(value * ((hash_sum * aureo) % 1))
        return custom_hash(palabra) % self.size
    def insert(self, palabra, puntaje):
        key = self.hash_function(palabra)
        valores = self.table[key].search(palabra)
        if valores:
            valores.puntaje = puntaje
        else:
            self.table[key].insert(palabra, puntaje)
    def search(self, palabra):
        key = self.hash_function(palabra)
        valores = self.table[key].search(palabra)
        return (valores.palabra,  valores.puntaje) if valores else None

    def delete(self, palabra):
        key = self.hash_function(palabra)
        return self.table[key].delete(palabra)   

# hash_table = HashTable()
# fibonacciHeap = FibonacciHeap()
trie = Trie()
trie.Insertar_archivo()


# Función Para Validar Las Palabras
def verificar_existencia(request, word):
    #print(word)
    state = hash_table.search(word.lower()) # 1. Busco la palabra en la tabla Hash
    print(state)
    if state == None: # Si devuelve None significa que no ha sido seleccionada
        state = trie.Search(word.lower()) # Ahora compruebo que dicha palabra exista en el diccionario
        if state == True: # Si existe se agrega a la tabla Hash y se le asigna un valor, además se asigna al Heap
            score = wordPuntuation(word)
            hash_table.insert(word.lower(), score)
            fibonacciHeap.insert_node(score, word.lower())
            max_score = fibonacciHeap.get_max()
            print(max_score)
            return JsonResponse({'flag': state, 'score': score, 'word': word,  'max_score': max_score})
        else:
            return JsonResponse({'flag': state})
    else:
        state = False
        return JsonResponse({'flag': state})


# Página Principal
def main(request):
    return render(request, 'BASE/main.html')


# Página Del Juego
def boggle_board(request):
    global hash_table
    hash_table = HashTable() 
    global fibonacciHeap
    fibonacciHeap = FibonacciHeap()
    vowels = ['A', 'E', 'I', 'O', 'U']
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    weights = [0.25 if letter in vowels else 0.7 / (len(alphabet) - len(vowels)) for letter in alphabet]
    board = [[random.choices(alphabet, weights = weights)[0] for j in range(18)] for i in range(8)]
    return render(request, 'BASE/game.html', {'board': board})


