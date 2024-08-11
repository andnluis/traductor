import tkinter as tk
from tkinter import ttk, messagebox, font
from trie import Trie

class Translator:
    def __init__(self, master):
        self.master = master
        self.master.title("Traductor")
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

        #Declaración de Fuente  
        fuente_titulo = font.Font(family="Helvetica", size=16, weight="normal") 

         # Create a style for the buttons
        style = ttk.Style()
        style.configure("TButton", background="#00aad4", foreground="white")

        # Texto original
        tk.Label(self.master, text="Texto original:", font=fuente_titulo).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.original_text_entry = tk.Text(self.master, height=5, width=60)
        self.original_text_entry.grid(row=1, column=0, padx=10, pady=10)

        # Traducción
        tk.Label(self.master, text="Traducción:", font=fuente_titulo).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.translated_text_entry = tk.Text(self.master, height=5, width=60)
        self.translated_text_entry.grid(row=3, column=0, padx=10, pady=10)

        # Palabras encontradas
        tk.Label(self.master, text="Palabras encontradas:", font=fuente_titulo).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.found_words_listbox = tk.Listbox(self.master, height=5, width=40)
        self.found_words_listbox.grid(row=1, column=1, padx=5, pady=5)

        # Palabras no encontradas
        tk.Label(self.master, text="Palabras no encontradas:", font=fuente_titulo).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.not_found_words_listbox = tk.Listbox(self.master, height=5, width=40)
        self.not_found_words_listbox.grid(row=3, column=1, padx=10, pady=10)

       # Botones
        self.translate_button = ttk.Button(self.master, text="Traducir", command=self.translate, style="TButton")
        self.translate_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.clear_button = ttk.Button(self.master, text="Limpiar", command=self.limpiar)
        self.clear_button.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        # Tipo de traducción
        tk.Label(self.master, text="Tipo de traducción:").grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.translation_type = tk.StringVar(value="es-en")
        tk.Radiobutton(self.master, text="Español a inglés", variable=self.translation_type, value="es-en").grid(row=5, column=1, padx=10, pady=2, sticky="w")
        tk.Radiobutton(self.master, text="Inglés a español", variable=self.translation_type, value="en-es").grid(row=6, column=1, padx=10, pady=2, sticky="w")

        # Agregar nueva palabra al diccionario
        self.add_word_label = tk.Label(self.master, text="+ Agregar una nueva palabra al diccionario", fg="blue", cursor="hand2")
        self.add_word_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.add_word_label.bind("<Button-1>", self.agregar_palabra)


    def translate(self):
        original_text = self.original_text_entry.get("1.0", tk.END).strip()
        self.translated_text_entry.delete("1.0", tk.END)
        self.found_words_listbox.delete(0, tk.END)
        self.not_found_words_listbox.delete(0, tk.END)

        if self.translation_type.get() == "es-en":
            words = original_text.split()
            translated_words = []
            for word in words:
                translation = self.es_to_en_trie.buscar(word)
                if translation:
                    translated_words.append(translation)
                    self.found_words_listbox.insert(tk.END, f"{word}: {translation}")
                else:
                    translated_words.append(word)
                    self.not_found_words_listbox.insert(tk.END, word)
            translated_text = " ".join(translated_words)
        else:
            words = original_text.split()
            translated_words = []
            for word in words:
                translation = self.en_to_es_trie.buscar(word)
                if translation:
                    translated_words.append(translation)
                    self.found_words_listbox.insert(tk.END, f"{word}: {translation}")
                else:
                    translated_words.append(word)
                    self.not_found_words_listbox.insert(tk.END, word)
            translated_text = " ".join(translated_words)

        self.translated_text_entry.insert(tk.END, translated_text)

    def limpiar(self):
        self.original_text_entry.delete("1.0", tk.END)
        self.translated_text_entry.delete("1.0", tk.END)
        self.found_words_listbox.delete(0, tk.END)
        self.not_found_words_listbox.delete(0, tk.END)

    def agregar_palabra(self, event):
        new_window = tk.Toplevel(self.master)
        new_window.title("Agregar nueva palabra")

        tk.Label(new_window, text="Español:").grid(row=0, column=0, padx=10, pady=10)
        es_entry = tk.Entry(new_window, width=30)
        es_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(new_window, text="Inglés:").grid(row=1, column=0, padx=10, pady=10)
        en_entry = tk.Entry(new_window, width=30)
        en_entry.grid(row=1, column=1, padx=10, pady=10)

        def add_word():
            es_word = es_entry.get().strip()
            en_word = en_entry.get().strip()
            if es_word and en_word:
                self.es_to_en_trie.insertar(es_word, en_word)
                self.en_to_es_trie.insertar(en_word, es_word)
                with open("dictionary.txt", "a") as f:
                    f.write(f"{es_word} : {en_word}\n")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Ambos campos deben ser rellenados")

        add_button = tk.Button(new_window, text="Agregar", command=add_word)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar la aplicación
root = tk.Tk()
translator = Translator(root)
root.mainloop()