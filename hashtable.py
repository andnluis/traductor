class TrieNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next_nodes = [None] * m

class HashTable:
    def __init__(self, m):
        self.m = m
        self.table = [None] * m

    def hash_function(self, key):
        if self.m == 27:
            return ord(key) - ord('a')
        elif self.m == 26:
            return ord(key.lower()) - ord('a')

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = TrieNode(key, value)
        else:
            current_node = self.table[index]
            while current_node.next_nodes[index] is not None:
                current_node = current_node.next_nodes[index]
            current_node.next_nodes[index] = TrieNode(key, value)

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index] is None:
            return None
        else:
            current_node = self.table[index]
            while current_node is not None:
                if current_node.key == key:
                    return current_node.value
                current_node = current_node.next_nodes[index]
            return None