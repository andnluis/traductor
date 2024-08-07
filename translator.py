import tkinter as tk
from tkinter import messagebox
from trie import Trie

class Translator:
    def __init__(self, master):
        self.master = master
        self.master.title("Spanish-English Translator")
        self.es_to_en_trie = Trie(27)
        self.en_to_es_trie = Trie(26)
        self.cargarDiccionario()
        self.create_widgets()

    def cargarDiccionario(self):
        with open("dictionary.txt", "r") as f:
            for line in f:
                es, en = line.strip().split(" : ")
                self.es_to_en_trie.insertar(es, en)
                self.en_to_es_trie.insertar(en, es)

    def create_widgets(self):
        self.es_label = tk.Label(self.master, text="Spanish:")
        self.es_label.pack()
        self.es_entry = tk.Entry(self.master, width=40)
        self.es_entry.pack()

        self.en_label = tk.Label(self.master, text="English:")
        self.en_label.pack()
        self.en_entry = tk.Entry(self.master, width=40)
        self.en_entry.pack()

        self.translate_button = tk.Button(self.master, text="Translate", command=self.translate)
        self.translate_button.pack()

    def translate(self):
        es_text = self.es_entry.get()
        en_text = self.en_entry.get()
        if es_text:
            en_translation = self.es_to_en_trie.buscar(es_text)
            if en_translation:
                self.en_entry.delete(0, tk.END)
                self.en_entry.insert(0, en_translation)
            else:
                messagebox.showinfo("Error", "No translation found")
        elif en_text:
            es_translation = self.en_to_es_trie.search(en_text)
            if es_translation:
                self.es_entry.delete(0, tk.END)
                self.es_entry.insert(0, es_translation)
            else:
                messagebox.showinfo("Error", "No translation found")

root = tk.Tk()
translator = Translator(root)
root.mainloop()