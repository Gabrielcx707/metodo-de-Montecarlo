import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class Vista1D:
    def __init__(self, frame_1D, controlador=None, crear_botones_funciones=None):
        """ Inicializa la vista 1D. """

        # Frame principal de la vista 1D
        self.frame_1d = frame_1D
        self.controlador = controlador
        self._crear_botones_funciones = crear_botones_funciones

        # Fuentes para labels y entradas
        self.font_label = ("Arial", 14)
        self.font_entry = ("Arial", 13)
        # Crear estilo para los botones de funciones matemáticas
        estilo_func = ttk.Style()
        estilo_func.configure("BotonFunc.TButton", font=("Arial", 12))

        # Área de resultados (se creará en _crear_interfaz_1d)
        self.texto_resultados_1d = None

        # Contenedor del gráfico (se creará en _crear_interfaz_1d)
        self.graph_container_1d = None

        # Entradas de datos
        self.func_1d = None
        self.a_1d = None
        self.b_1d = None
        self.n_1d = None

        # Botón calcular
        self.btn_calcular_1d = None

        # Botones de ejemplo
        self.btn_ej1_1d = None
        self.btn_ej2_1d = None
        self.btn_ej3_1d = None

    def _crear_interfaz_1d(self):
        """Crea la interfaz para integral 1D"""
        # Frame izquierdo - Entradas
        left_frame = ttk.Frame(self.frame_1d)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Título
        ttk.Label(left_frame, text="Integral Simple ∫f(x)dx", 
                font=("Arial", 15, "bold")).pack(pady=10)
        
        # Función
        ttk.Label(left_frame, text="Función f(x):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.func_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.func_1d.pack(pady=5, padx=5, fill=tk.X)
        self.func_1d.insert(0, "x**2")
        ttk.Label(left_frame, text="Ejemplo: x**2, math.sin(x), math.exp(x)", 
                font=("Arial", 10)).pack(anchor=tk.W, padx=5)
        
        # Frame para botones de funciones matemáticas
        func_buttons_frame = ttk.Frame(left_frame)
        func_buttons_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Crear botones de funciones matemáticas
        self._crear_botones_funciones(func_buttons_frame, self.func_1d)
        
        # Límite a
        ttk.Label(left_frame, text="Límite inferior (a):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.a_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.a_1d.pack(pady=5, padx=5, fill=tk.X)
        self.a_1d.insert(0, "0")
        
        # Límite b
        ttk.Label(left_frame, text="Límite superior (b):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.b_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.b_1d.pack(pady=5, padx=5, fill=tk.X)
        self.b_1d.insert(0, "1")
        
        # Número de puntos
        ttk.Label(left_frame, text="Número de puntos (N):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.n_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.n_1d.pack(pady=5, padx=5, fill=tk.X)
        self.n_1d.insert(0, "10000")
        
        # Botón calcular
        self.btn_calcular_1d = ttk.Button(left_frame, text="Calcular", style="BotonFunc.TButton",
                                        command=self._calcular_1d)
        self.btn_calcular_1d.pack(pady=20, padx=5, fill=tk.X)
        
        # Botones de ejemplo
        ttk.Label(left_frame, text="Ejemplos:", font=("Arial", 12, "bold")).pack(pady=(20,5))
        
        self.btn_ej1_1d = ttk.Button(left_frame, text="Ejemplo 1: x² en [0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("x**2", 0, 1, 10000))
        self.btn_ej1_1d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej2_1d = ttk.Button(left_frame, text="Ejemplo 2: sin(x) en [0,π]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("math.sin(x)", 0, math.pi, 10000))
        self.btn_ej2_1d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej3_1d = ttk.Button(left_frame, text="Ejemplo 3: eˣ en [0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("math.exp(x)", 0, 1, 10000))
        self.btn_ej3_1d.pack(pady=2, padx=5, fill=tk.X)
        
        # Frame derecho - Gráfico y resultados
        right_frame = ttk.Frame(self.frame_1d)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de gráfico
        graph_frame = ttk.LabelFrame(right_frame, text="Gráfico")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(right_frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_resultados_1d = scrolledtext.ScrolledText(result_frame, 
                                                            height=15, 
                                                            wrap=tk.WORD,
                                                            font=("Courier", 12))
        self.texto_resultados_1d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para el gráfico (se creará cuando se calcule)
        self.graph_container_1d = ttk.Frame(graph_frame)
        self.graph_container_1d.pack(fill=tk.BOTH, expand=True)

    def obtener_valores_1d(self):
        """Obtiene los valores de los campos 1D"""
        return {
            'func': self.func_1d.get(),
            'a': self.a_1d.get(),
            'b': self.b_1d.get(),
            'n': self.n_1d.get()
        }
    
    def actualizar_grafico_1d(self, func, a, b, puntos):
        """Actualiza el gráfico 1D"""
        # Limpiar gráfico anterior
        for widget in self.graph_container_1d.winfo_children():
            widget.destroy()
        
        # Crear nuevo gráfico
        self.fig_1d, ax = plt.subplots(figsize=(2, 3))
        
        # Generar puntos para la función
        x_vals = np.linspace(a, b, 200)
        y_vals = []
        for x in x_vals:
            try:
                y = eval(func, {"x": x, "math": math, "np": np, "__builtins__": {}})
                y_vals.append(y)
            except:
                try:
                    y = eval(func, {"x": x, "math": math, "np": np})
                    y_vals.append(y)
                except:
                    y_vals.append(0)
        
        # Graficar función
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
        
        # Graficar puntos aleatorios
        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, color='red', s=20, alpha=0.6, label='Puntos aleatorios')
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Integral de f(x) = {func} en [{a}, {b}]')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Integrar en tkinter
        self.canvas_1d = FigureCanvasTkAgg(self.fig_1d, self.graph_container_1d)
        self.canvas_1d.draw()
        self.canvas_1d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _calcular_1d(self):
        """Método auxiliar para calcular 1D"""
        if self.controlador:
            self.controlador.calcular_1d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _cargar_ejemplo_1d(self, func, a, b, n):
        """Método auxiliar para cargar ejemplo 1D"""
        if self.controlador:
            self.controlador.cargar_ejemplo_1d(func, a, b, n)
        else:
            self.mostrar_error("Controlador no inicializado")

    def mostrar_resultados(self, texto):
        self.texto_resultados_1d.delete(1.0, tk.END)
        self.texto_resultados_1d.insert(tk.END, texto)