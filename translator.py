from trie import Trie

class Translator:
    def __init__(self, dictionary_file):
        self.trie = Trie()
        self.load_dictionary(dictionary_file)

    def load_dictionary(self, dictionary_file):
        with open(dictionary_file, 'r') as file:
            for line in file:
                entry = line.strip().split(' : ')
                if len(entry) == 2:
                    source_word, target_word = entry
                    self.trie.insert(source_word, target_word)

    def translate(self, word):
        return self.trie.search(word)

# Usage example
translator = Translator('./dictionary.txt')
print(translator.translate('ábaco'))  # Output: 'abacus' (or the corresponding translation)
print(translator.translate('b'))  # Output: None

