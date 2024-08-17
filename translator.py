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
        self.crear_widgets()

    def cargarDiccionario(self):
        with open("dictionary.txt", "r") as f:
            for line in f:
                es, en = line.strip().split(" : ")
                self.es_to_en_trie.insertar(es, en)
                self.en_to_es_trie.insertar(en, es)

    def crear_widgets(self):

        #Declaración de Fuente  
        fuente_titulo = font.Font(family="Helvetica", size=16, weight="normal") 

         # Create a style for the buttons
        style = ttk.Style()
        style.configure("TButton", background="#00aad4", foreground="white")

        # Texto original
        tk.Label(self.master, text="Texto original:", font=fuente_titulo).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entrada_text_original = tk.Text(self.master, height=5, width=60)
        self.entrada_text_original.grid(row=1, column=0, padx=10, pady=10)

        # Traducción
        tk.Label(self.master, text="Traducción:", font=fuente_titulo).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entrada_texto_traducida = tk.Text(self.master, height=5, width=60)
        self.entrada_texto_traducida.grid(row=3, column=0, padx=10, pady=10)

        # Palabras encontradas
        tk.Label(self.master, text="Palabras encontradas:", font=fuente_titulo).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.lista_palabras_encontradas = tk.Listbox(self.master, height=5, width=40)
        self.lista_palabras_encontradas.grid(row=1, column=1, padx=5, pady=5)

        # Palabras no encontradas
        tk.Label(self.master, text="Palabras no encontradas:", font=fuente_titulo).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.lista_palabras_no_encontradas = tk.Listbox(self.master, height=5, width=40)
        self.lista_palabras_no_encontradas.grid(row=3, column=1, padx=10, pady=10)

       # Botones
        self.translate_button = ttk.Button(self.master, text="Traducir", command=self.traducir, style="TButton")
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


    def traducir(self):
        texto_original = self.entrada_text_original.get("1.0", tk.END).strip()
        self.entrada_texto_traducida.delete("1.0", tk.END)
        self.lista_palabras_encontradas.delete(0, tk.END)
        self.lista_palabras_no_encontradas.delete(0, tk.END)

        if self.translation_type.get() == "es-en":
            palabras = texto_original.split()
            palabras_traducidas = []
            for palabra in palabras:
                traduccion = self.es_to_en_trie.buscar(palabra)
                if traduccion:
                    traducciones = traduccion.split(", ")
                    palabras_traducidas.append(traducciones[0])
                    self.lista_palabras_encontradas.insert(tk.END, f"{palabra}: {traduccion}")
                else:
                    palabras_traducidas.append(palabra)
                    self.lista_palabras_no_encontradas.insert(tk.END, palabra)
            text_traducido = " ".join(palabras_traducidas)
        else:
            palabras = texto_original.split()
            palabras_traducidas = []
            for palabra in palabras:
                traduccion = self.en_to_es_trie.buscar(palabra)
                if traduccion:
                    palabras_traducidas.append(traduccion)
                    self.lista_palabras_encontradas.insert(tk.END, f"{palabra}: {traduccion}")
                else:
                    palabras_traducidas.append(palabra)
                    self.lista_palabras_no_encontradas.insert(tk.END, palabra)
            text_traducido = " ".join(palabras_traducidas)

        self.entrada_texto_traducida.insert(tk.END, text_traducido)

    def limpiar(self):
        self.entrada_text_original.delete("1.0", tk.END)
        self.entrada_texto_traducida.delete("1.0", tk.END)
        self.lista_palabras_encontradas.delete(0, tk.END)
        self.lista_palabras_no_encontradas.delete(0, tk.END)

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