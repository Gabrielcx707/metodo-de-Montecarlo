import tkinter as tk
from tkinter import ttk, messagebox

class VistaMonteCarlo:
    """Vista - Interfaz gráfica para el método de Monte Carlo"""
    
    def __init__(self, root_or_controlador):
        # Si se pasa un controlador, crear la ventana
        if isinstance(root_or_controlador, tk.Tk) or isinstance(root_or_controlador, tk.Toplevel):
            self.root = root_or_controlador
            self.controlador = None
        else:
            # Si se pasa el controlador, crear la ventana
            self.root = tk.Tk()
            self.controlador = root_or_controlador
        
        # Crear estilo para los botones de funciones matemáticas
        estilo_func = ttk.Style()
        estilo_func.configure("BotonFunc.TButton", font=("Arial", 12))

        self.root.title("Simulación Monte Carlo - Integrales")
        self.root.geometry("1200x800")
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para integral 1D
        self.frame_1d = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_1d, text="Integral Simple (1D)")
        
        # Frame para integral 2D
        self.frame_2d = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_2d, text="Integral Doble (2D)")
        
        # Inicializar gráficos
        self.fig_1d = None
        self.canvas_1d = None
        self.fig_2d = None
        self.canvas_2d = None
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", mensaje)
    
    def mostrar_progreso(self, mensaje):
        """Muestra un mensaje de progreso accediendo a las sub-vistas"""
        # 1. Identificamos qué pestaña está activa
        es_pestaña_1d = self.notebook.index(self.notebook.select()) == 0
    
        # 2. Accedemos al widget de texto a través del controlador
        if es_pestaña_1d:
            # Buscamos el widget que vive dentro de vista_1d
            texto_widget = self.controlador.vista_1d.texto_resultados_1d
        else:
            # Buscamos el widget que vive dentro de vista_2d
            texto_widget = self.controlador.vista_2d.texto_resultados_2d
    
        # 3. Operamos normalmente
        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(1.0, mensaje)
        self.root.update()
    
    def establecer_controlador(self, controlador):
        """Establece el controlador después de la creación"""
        self.controlador = controlador
    
    def _crear_botones_funciones(self, parent_frame, entry_widget):
        """Crea los botones de funciones matemáticas"""
        # Primera fila: funciones trigonométricas básicas
        row1 = ttk.Frame(parent_frame)
        row1.pack(fill=tk.X, pady=2)
        
        btn_cos = ttk.Button(row1, text="cos", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.cos("))
        btn_cos.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_sin = ttk.Button(row1, text="sin", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.sin("))
        btn_sin.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_tan = ttk.Button(row1, text="tan", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.tan("))
        btn_tan.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # Segunda fila: funciones trigonométricas inversas
        row2 = ttk.Frame(parent_frame)
        row2.pack(fill=tk.X, pady=2)
        
        btn_arcsin = ttk.Button(row2, text="arcsin", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.asin("))
        btn_arcsin.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_arccos = ttk.Button(row2, text="arccos", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.acos("))
        btn_arccos.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_arctan = ttk.Button(row2, text="arctan", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.atan("))
        btn_arctan.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # Tercera fila: logaritmos
        row3 = ttk.Frame(parent_frame)
        row3.pack(fill=tk.X, pady=2)
        
        btn_log = ttk.Button(row3, text="log", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.log10("))
        btn_log.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_ln = ttk.Button(row3, text="ln", width=8, style="BotonFunc.TButton",
                        command=lambda: self._insertar_funcion(entry_widget, "math.log("))
        btn_ln.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
    
    def _insertar_funcion(self, entry_widget, funcion):
        """Inserta una función matemática en el Entry en la posición del cursor"""
        cursor_pos = entry_widget.index(tk.INSERT)
        texto_actual = entry_widget.get()
        nuevo_texto = texto_actual[:cursor_pos] + funcion + texto_actual[cursor_pos:]
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, nuevo_texto)
        # Mover el cursor después de la función insertada
        nueva_pos = cursor_pos + len(funcion)
        entry_widget.icursor(nueva_pos)
        entry_widget.focus_set()
    
    def ejecutar(self):
        """Inicia la aplicación (ya está ejecutándose si se pasó root)"""
        if self.controlador:
            # Si se creó desde el controlador, iniciar mainloop
            self.root.mainloop()
