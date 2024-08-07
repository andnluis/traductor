
# Clase HashTable 
class HashTable:

    # Constructor
    def __init__(self, m):
        self.m = m
        self.tabla = [None] * m

    # Función hash
    def _hash(self, llave):
        return ord(llave) % self.m

    # Función para Insertar un valor en la tabla
    def insertar(self, llave, valor):
        index = self._hash(llave)
        if self.tabla[index] is None:
            self.tabla[index] = Nodo(llave, valor)
        else:
            self.tabla[index].insertar(llave, valor)

    # Función para obtener un valor de la tabla
    def obtener(self, llave):
        index = self._hash(llave)
        if self.tabla[index] is not None:
            return self.tabla[index].get(llave)
        return None

# Clase Nodo
class Nodo:

    # Constructor
    def __init__(self, llave, valor):
        self.llave = llave
        self.valor = valor
        self.nodosHijos = {}

    # Función para insertar un valor en el nodo
    def insertar(self, llave, valor):
        if llave not in self.nodosHijos:
            self.nodosHijos[llave] = Nodo(llave, valor)
        else:
            self.nodosHijos[llave].valor = valor

    # Función para obtener un valor del nodo
    def get(self, llave):
        if llave in self.nodosHijos:
            return self.nodosHijos[llave].valor
        return None