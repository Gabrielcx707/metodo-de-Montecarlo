import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

class Vista2D:
    def __init__(self, frame_2D, controlador=None, crear_botones_funciones=None):
        """Inicializa la vista 2D"""
        self.controlador = controlador
        self._crear_botones_funciones = crear_botones_funciones

        # Frame principal de la vista 2D
        self.frame_2d = frame_2D

        # Fuentes para labels y entradas
        self.font_label = ("Arial", 14)
        self.font_label2 = ("Arial", 12)
        self.font_entry = ("Arial", 13)
        self.font_entry2 = ("Arial", 11)
        # Crear estilo para los botones de funciones matemáticas
        estilo_func = ttk.Style()
        estilo_func.configure("BotonFunc.TButton", font=("Arial", 12))

        # Área de resultados (se creará en _crear_interfaz_2d)
        self.texto_resultados_2d = None

        # Contenedor del gráfico (se creará en _crear_interfaz_2d)
        self.graph_container_2d = None

        # Entradas de datos
        self.func_2d = None
        self.ax_2d = None
        self.bx_2d = None
        self.cy_2d = None
        self.dy_2d = None
        self.n_2d = None

        # Botón calcular
        self.btn_calcular_2d = None

        # Botones de ejemplo
        self.btn_ej1_2d = None
        self.btn_ej2_2d = None

        # Crear estilo para los botones de funciones matemáticas
        estilo_func = ttk.Style()
        estilo_func.configure("BotonFunc.TButton", font=("Arial", 12))

    def _crear_interfaz_2d(self):
        """Crea la interfaz para integral 2D"""
        # Frame izquierdo - Entradas
        left_frame = ttk.Frame(self.frame_2d)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Título
        ttk.Label(left_frame, text="Integral Doble ∬f(x,y)dxdy", 
                font=("Arial", 15, "bold")).pack(pady=7)
        
        # Función
        ttk.Label(left_frame, text="Función f(x,y):", font=self.font_label2).pack(anchor=tk.W, pady=5)
        self.func_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.func_2d.pack(pady=5, padx=5, fill=tk.X)
        self.func_2d.insert(0, "x*y")
        ttk.Label(left_frame, text="Ejemplo: x*y, x**2 + y**2", 
                font=("Arial", 11)).pack(anchor=tk.W, padx=5)
        
        # Frame para botones de funciones matemáticas
        func_buttons_frame = ttk.Frame(left_frame)
        func_buttons_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Crear botones de funciones matemáticas
        self._crear_botones_funciones(func_buttons_frame, self.func_2d)
        
        # Límites X
        ttk.Label(left_frame, text="Intervalo X:", font=("Arial", 13, "bold")).pack(anchor=tk.W, pady=(10,5))
        ttk.Label(left_frame, text="Límite inferior (ax):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.ax_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.ax_2d.pack(pady=2, padx=5, fill=tk.X)
        self.ax_2d.insert(0, "0")
        
        ttk.Label(left_frame, text="Límite superior (bx):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.bx_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.bx_2d.pack(pady=2, padx=5, fill=tk.X)
        self.bx_2d.insert(0, "1")
        
        # Límites Y
        ttk.Label(left_frame, text="Intervalo Y:", font=("Arial", 13, "bold")).pack(anchor=tk.W, pady=(10,5))
        ttk.Label(left_frame, text="Límite inferior (cy):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.cy_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.cy_2d.pack(pady=2, padx=5, fill=tk.X)
        self.cy_2d.insert(0, "0")
        
        ttk.Label(left_frame, text="Límite superior (dy):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.dy_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.dy_2d.pack(pady=2, padx=5, fill=tk.X)
        self.dy_2d.insert(0, "1")
        
        # Número de puntos
        ttk.Label(left_frame, text="Número de puntos (N):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.n_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.n_2d.pack(pady=5, padx=5, fill=tk.X)
        self.n_2d.insert(0, "10000")
        
        # Botón calcular
        self.btn_calcular_2d = ttk.Button(left_frame, text="Calcular", style="BotonFunc.TButton", 
                                        command=self._calcular_2d)
        self.btn_calcular_2d.pack(pady=2, padx=5, fill=tk.X)
        
        # Botones de ejemplo
        ttk.Label(left_frame, text="Ejemplos:", font=("Arial", 12, "bold")).pack(pady=(5))
        
        self.btn_ej1_2d = ttk.Button(left_frame, text="Ejemplo 1: x*y en [0,1]×[0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_2d("x*y", 0, 1, 0, 1, 10000))
        self.btn_ej1_2d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej2_2d = ttk.Button(left_frame, text="Ejemplo 2: x²+y² en [0,1]×[0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_2d("x**2 + y**2", 0, 1, 0, 1, 10000))
        self.btn_ej2_2d.pack(pady=2, padx=5, fill=tk.X)
        
        # Frame derecho - Gráfico y resultados
        right_frame = ttk.Frame(self.frame_2d)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de gráfico
        graph_frame = ttk.LabelFrame(right_frame, text="Gráfico")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(right_frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_resultados_2d = scrolledtext.ScrolledText(result_frame, 
                                                            height=15, 
                                                            wrap=tk.WORD,
                                                            font=("Courier", 12))
        self.texto_resultados_2d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para el gráfico (se creará cuando se calcule)
        self.graph_container_2d = ttk.Frame(graph_frame)
        self.graph_container_2d.pack(fill=tk.BOTH, expand=True)

    def obtener_valores_2d(self):
        """Obtiene los valores de los campos 2D"""
        return {
            'func': self.func_2d.get(),
            'ax': self.ax_2d.get(),
            'bx': self.bx_2d.get(),
            'cy': self.cy_2d.get(),
            'dy': self.dy_2d.get(),
            'n': self.n_2d.get()
        }
    
    def actualizar_grafico_2d(self, func, ax_val, bx_val, cy_val, dy_val, puntos):
        """Actualiza el gráfico 2D"""
        # Limpiar gráfico anterior
        for widget in self.graph_container_2d.winfo_children():
            widget.destroy()
        
        # Crear nuevo gráfico
        self.fig_2d = plt.figure(figsize=(4, 4))
        ax = self.fig_2d.add_subplot(111, projection='3d')
        
        # Generar malla para la superficie
        x_vals = np.linspace(ax_val, bx_val, 30)
        y_vals = np.linspace(cy_val, dy_val, 30)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    z = eval(func, {"x": X[i,j], "y": Y[i,j], "math": math, "np": np, "__builtins__": {}})
                    Z[i,j] = z
                except:
                    try:
                        z = eval(func, {"x": X[i,j], "y": Y[i,j], "math": math, "np": np})
                        Z[i,j] = z
                    except:
                        Z[i,j] = 0
        
        # Graficar superficie
        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')
        
        # Graficar puntos aleatorios
        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            z_puntos = [p['z'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, z_puntos, color='red', s=20, alpha=0.8)
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('f(x,y)')
        ax.set_title(f'Integral de f(x,y) = {func}')
        
        # Integrar en tkinter
        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, self.graph_container_2d)
        self.canvas_2d.draw()
        self.canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _calcular_2d(self):
        """Método auxiliar para calcular 2D"""
        if self.controlador:
            self.controlador.calcular_2d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _cargar_ejemplo_2d(self, func, ax, bx, cy, dy, n):
        """Método auxiliar para cargar ejemplo 2D"""
        if self.controlador:
            self.controlador.cargar_ejemplo_2d(func, ax, bx, cy, dy, n)
        else:
            self.mostrar_error("Controlador no inicializado")

    def mostrar_resultados(self, texto):
        self.texto_resultados_2d.delete(1.0, tk.END)
        self.texto_resultados_2d.insert(tk.END, texto)