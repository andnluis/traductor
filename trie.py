from hashtable import HashTable, Nodo

# Clase Trie
class Trie:
    
    # Constructor
    def __init__(self, m):
        self.raiz = Nodo("", "")
        self.m = m
        self.hash_table = HashTable(m)

    # Función para insertar una palabra en el trie
    def insertar(self, palabra, traduccion):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.nodosHijos:
                nodo.nodosHijos[char] = Nodo(char, "")
                self.hash_table.insertar(char, nodo.nodosHijos[char])
            nodo = nodo.nodosHijos[char]
        nodo.value = traduccion

    # Función para buscar una palabra en el trie
    def buscar(self, palabra):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.nodosHijos:
                return None
            nodo = nodo.nodosHijos[char]
        return nodo.value