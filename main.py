import tkinter as tk

#practica 1 Alejandro Garcia Martinez #




from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

class SearchComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos de Búsqueda")
        self.root.geometry("1200x800")

        self.dark_mode = True
        self.style = ttk.Style()
        self.apply_dark_mode()

        # Variables
        self.listaDatos = []
        self.listaOriginal = []
        self.resultadosTiempo = {'linear': {}, 'binaria': {}}

        self.setupInterfaz()

    def setupInterfaz(self):
        # Frames principales
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.left_frame = ttk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side="left", fill="y", padx=(0,5))

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5,0))

        # --- Top Frame: Botones ---
        ttk.Label(self.top_frame, text="Opciones", font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
        self.btn_load = ttk.Button(self.top_frame, text="Cargar CSV", command=self.dummy_action)
        self.btn_load.pack(side="left", padx=5)
        self.btn_compare = ttk.Button(self.top_frame, text="Comparar", command=self.dummy_action)
        self.btn_compare.pack(side="left", padx=5)
        self.btn_clear = ttk.Button(self.top_frame, text="Limpiar", command=self.dummy_action)
        self.btn_clear.pack(side="left", padx=5)
        self.btn_toggle = ttk.Button(self.top_frame, text="Cambiar Tema", command=self.toggle_theme)
        self.btn_toggle.pack(side="left", padx=20)

        # --- Left Frame: Tabla y Generación de Datos ---
        ttk.Label(self.left_frame, text="Generación de Datos", font=("Segoe UI", 12, "bold")).pack(pady=5)
        ttk.Label(self.left_frame, text="Tamaño de la lista:").pack(pady=(0,2))
        self.size_var = tk.StringVar(value="1000")
        size_combo = ttk.Combobox(self.left_frame, textvariable=self.size_var,
                                  values=["100","1000","10000","100000","1000000"], width=15, state="readonly")
        size_combo.pack(pady=(0,5))
        ttk.Button(self.left_frame, text="Generar datos", command=self.generate_data).pack(pady=(0,10))

        ttk.Label(self.left_frame, text="Búsqueda", font=("Segoe UI", 12, "bold")).pack(pady=5)
        ttk.Label(self.left_frame, text="Valor a buscar:").pack(pady=(0,2))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.left_frame, textvariable=self.search_var, width=15)
        search_entry.pack(pady=(0,5))
        ttk.Button(self.left_frame, text="Búsqueda Lineal", command=self.linear_search).pack(pady=(2,2))
        ttk.Button(self.left_frame, text="Búsqueda Binaria", command=self.binaria_search).pack(pady=(0,10))
        ttk.Button(self.left_frame, text="Generar Comparación Completa", command=self.comparacionCompleta).pack(pady=(10,0))

        # --- Right Frame: Lista, Info y Gráfica ---
        content_frame = ttk.Frame(self.right_frame)
        content_frame.pack(fill="both", expand=True)

        # Lista de Elementos
        list_frame = ttk.LabelFrame(content_frame, text="Lista de Elementos", padding=5)
        list_frame.pack(fill="x", padx=5, pady=5)
        self.list_text = tk.Text(list_frame, height=6)
        list_scroll = ttk.Scrollbar(list_frame, command=self.list_text.yview)
        self.list_text.configure(yscrollcommand=list_scroll.set)
        self.list_text.pack(side="left", fill="both", expand=True)
        list_scroll.pack(side="left", fill="y")

        # Información de Búsqueda
        info_frame = ttk.LabelFrame(content_frame, text="Información de Búsqueda", padding=5)
        info_frame.pack(fill="x", padx=5, pady=5)
        self.search_info_label = ttk.Label(info_frame, text="Realice una búsqueda para ver información")
        self.search_info_label.pack(pady=5)

        # Gráfica
        graph_frame = ttk.LabelFrame(content_frame, text="Comparación de Tiempos (Big O)", padding=5)
        graph_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Resultados
        results_frame = ttk.LabelFrame(content_frame, text="Historial de Resultados", padding=5)
        results_frame.pack(fill="x", padx=5, pady=5)
        self.result_text = tk.Text(results_frame, height=8)
        result_scroll = ttk.Scrollbar(results_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scroll.set)
        self.result_text.pack(side="left", fill="both", expand=True)
        result_scroll.pack(side="left", fill="y")

        self.actualizarDisplayResultados("Aplicación iniciada. Genere datos para comenzar.")

    # ---------- Funciones de Datos y Búsqueda ----------
    def dummy_action(self):
        print("Acción ejecutada")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI",11,"bold"), padding=8, background="#222", foreground="#fff")
        self.style.map("TButton", background=[("active","#444")])
        self.style.configure("Treeview", background="#1e1e1e", foreground="white", rowheight=25, fieldbackground="#1e1e1e")
        self.style.map("Treeview", background=[("selected","#007acc")])

    def apply_light_mode(self):
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI",11,"bold"), padding=8, background="#f0f0f0", foreground="#000")
        self.style.map("TButton", background=[("active","#ddd")])
        self.style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        self.style.map("Treeview", background=[("selected","#4a90e2")])

    def generate_data(self):
        try:
            size = int(self.size_var.get())
            self.listaOriginal = random.sample(range(1,size+1), size)
            self.listaDatos = self.listaOriginal.copy()
            self.actualizarDisplayLista()
            self.actualizarDisplayResultados(f"Lista generada con {size} elementos")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizarDisplayLista(self):
        self.list_text.delete(1.0, tk.END)
        if not self.listaDatos:
            self.list_text.insert(tk.END, "No hay datos generados")
            return
        size = len(self.listaDatos)
        if size <= 20:
            elements_str = ", ".join(map(str, self.listaDatos))
        else:
            first10 = ", ".join(map(str, self.listaDatos[:10]))
            last10 = ", ".join(map(str, self.listaDatos[-10:]))
            elements_str = f"{first10}, ..., {last10}"
        self.list_text.insert(tk.END, f"Elementos ({size} total):\n{elements_str}")

    def actualizarInfoBusqueda(self, algorithm, found_index, search_value, time_ms, is_sorted=False):
        if found_index != -1:
            element = self.listaDatos[found_index] if not is_sorted else sorted(self.listaDatos)[found_index]
            info_text = f"{algorithm} | Índice: {found_index} | Elemento: {element} | Tiempo: {time_ms:.4f} ms"
        else:
            info_text = f"{algorithm} | No encontrado | Valor: {search_value} | Tiempo: {time_ms:.4f} ms"
        self.search_info_label.config(text=info_text)

    def busqueda_lineal(self, lista, x):
        for i in range(len(lista)):
            if lista[i] == x:
                return i
        return -1

    def busqueda_binaria(self, lista, x):
        izquierda, derecha = 0, len(lista)-1
        while izquierda <= derecha:
            medio = (izquierda+derecha)//2
            if lista[medio]==x:
                return medio
            elif lista[medio]<x:
                izquierda = medio+1
            else:
                derecha = medio-1
        return -1

    def medirTiempo(self, search_function, lista, x, repetitions=5):
        times=[]
        for _ in range(repetitions):
            start=time.perf_counter()
            result=search_function(lista,x)
            end=time.perf_counter()
            times.append((end-start)*1000)
        return result, sum(times)/len(times)

    def linear_search(self):
        if not self.listaDatos:
            messagebox.showwarning("Advertencia","Primero genere datos")
            return
        try:
            search_value=int(self.search_var.get())
            result, avg_time=self.medirTiempo(self.busqueda_lineal,self.listaDatos,search_value)
            self.actualizarInfoBusqueda("Búsqueda Lineal", result, search_value, avg_time)
            self.actualizarDisplayResultados(f"Búsqueda Lineal: Índice={result}, Tiempo={avg_time:.4f} ms")
        except ValueError:
            messagebox.showerror("Error","Ingrese valor numérico válido")

    def binaria_search(self):
        if not self.listaDatos:
            messagebox.showwarning("Advertencia","Primero genere datos")
            return
        try:
            search_value=int(self.search_var.get())
            lista_ordenada=sorted(self.listaDatos)
            result, avg_time=self.medirTiempo(self.busqueda_binaria,lista_ordenada,search_value)
            self.actualizarInfoBusqueda("Búsqueda Binaria", result, search_value, avg_time, True)
            self.actualizarDisplayResultados(f"Búsqueda Binaria: Índice={result}, Tiempo={avg_time:.4f} ms")
        except ValueError:
            messagebox.showerror("Error","Ingrese valor numérico válido")

    def comparacionCompleta(self):
        sizes=[100,1000,10000,100000]
        linear_times=[]
        binaria_times=[]
        self.actualizarDisplayResultados("Iniciando comparación completa...")
        for size in sizes:
            test_data=random.sample(range(1,size+1),size)
            search_value=test_data[size//2]
            _, lin_time=self.medirTiempo(self.busqueda_lineal,test_data,search_value,5)
            _, bin_time=self.medirTiempo(self.busqueda_binaria,sorted(test_data),search_value,5)
            linear_times.append(lin_time)
            binaria_times.append(bin_time)
            self.actualizarDisplayResultados(f"Tamaño={size}: Lineal={lin_time:.4f} ms, Binaria={bin_time:.4f} ms")
        self.update_graph(sizes,linear_times,binaria_times)
        self.actualizarDisplayResultados("Comparación completa terminada.")

    def update_graph(self, sizes, linear_times, binaria_times):
        self.ax.clear()
        self.ax.plot(sizes, linear_times,'o-',color='red',label='Lineal O(n)')
        self.ax.plot(sizes, binaria_times,'s-',color='blue',label='Binaria O(log n)')
        self.ax.set_xlabel("Tamaño de la lista (n)")
        self.ax.set_ylabel("Tiempo promedio (ms)")
        self.ax.set_title("Comparación de Complejidad Temporal")
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def actualizarDisplayResultados(self,message):
        self.result_text.insert(tk.END,message+"\n")
        self.result_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = SearchComparator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
