from modelo.modelo import MonteCarloCalculator
from vista.vista import VistaMonteCarlo
from vista.vista_1d import Vista1D
from vista.vista_2d import Vista2D

class ControladorMonteCarlo:
    """Controlador - Coordina Modelo y Vista"""
    
    def __init__(self, modelo=None, vista=None):
        # Inicializar Modelo y Vista si no se pasan
        self.modelo = modelo if modelo else MonteCarloCalculator()
        self.vista = vista if vista else VistaMonteCarlo(self)
        
        # Crear sub-vistas 1D y 2D dentro de la vista principal
        self.vista_1d = Vista1D(
            self.vista.frame_1d, 
            self, 
            crear_botones_funciones=self.vista._crear_botones_funciones
            )
        self.vista_1d._crear_interfaz_1d()
        
        self.vista_2d = Vista2D(self.vista.frame_2d, self, crear_botones_funciones=self.vista._crear_botones_funciones)
        self.vista_2d._crear_interfaz_2d()
    
    def calcular_1d(self):
        """Maneja el cálculo de integral 1D"""
        try:
            # Obtener valores de la vista
            valores = self.vista_1d.obtener_valores_1d()
            func = valores['func']
            a = float(valores['a'])
            b = float(valores['b'])
            n = int(valores['n'])
            
            # Validar
            if a >= b:
                self.vista.mostrar_error("El límite 'a' debe ser menor que 'b'")
                return
            
            # Mostrar progreso
            self.vista.mostrar_progreso(f"🔄 Calculando...\n\nGenerando {n:,} puntos aleatorios...\n")
            
            # Calcular usando el modelo
            resultado, puntos = self.modelo.calcular_integral_1d(func, a, b, n)
            
            # Actualizar vista
            self.vista_1d.actualizar_grafico_1d(func, a, b, puntos)
            self.mostrar_resultados_1d(resultado, puntos, func, a, b, n)
            
        except Exception as e:
            self.vista.mostrar_error(f"Error en cálculo 1D: {str(e)}")
    
    def calcular_2d(self):
        """Maneja el cálculo de integral 2D"""
        try:
            # Obtener valores de la vista
            valores = self.vista_2d.obtener_valores_2d()
            func = valores['func']
            ax = float(valores['ax'])
            bx = float(valores['bx'])
            cy = float(valores['cy'])
            dy = float(valores['dy'])
            n = int(valores['n'])
            
            # Validar
            if ax >= bx or cy >= dy:
                self.vista.mostrar_error("Los límites inferiores deben ser menores que los superiores")
                return
            
            # Mostrar progreso
            self.vista.mostrar_progreso(f"🔄 Calculando...\n\nGenerando {n:,} puntos aleatorios en 2D...\n")
            
            # Calcular usando el modelo
            resultado, puntos = self.modelo.calcular_integral_2d(func, ax, bx, cy, dy, n)
            
            # Actualizar vista
            self.vista_2d.actualizar_grafico_2d(func, ax, bx, cy, dy, puntos)
            self.mostrar_resultados_2d(resultado, puntos, func, ax, bx, cy, dy, n)
            
        except Exception as e:
            self.vista.mostrar_error(f"Error en cálculo 2D: {str(e)}")
    
    def mostrar_resultados_1d(self, resultado, puntos, func, a, b, n):
        """Formatea y muestra resultados para 1D"""
        texto = "="*60 + "\n"
        texto += "INTEGRAL SIMPLE - MÉTODO DE MONTE CARLO\n"
        texto += "="*60 + "\n\n"
        
        texto += f"📊 INFORMACIÓN DEL CÁLCULO:\n"
        texto += f"   Función: f(x) = {func}\n"
        texto += f"   Intervalo: [{a}, {b}]\n"
        texto += f"   Puntos generados (N): {n:,}\n\n"
        
        texto += f"🎯 RESULTADO DE LA APROXIMACIÓN:\n"
        texto += f"   ∫f(x)dx ≈ {resultado:.8f}\n\n"
        
        # Calcular valor exacto si es posible
        exacto = self.modelo.calcular_valor_exacto_1d(func, a, b)
        if exacto is not None:
            error = abs(resultado - exacto)
            texto += f"📐 COMPARACIÓN CON VALOR EXACTO:\n"
            texto += f"   Valor exacto: {exacto:.8f}\n"
            texto += f"   Error absoluto: {error:.8f}\n"
            texto += f"   Error relativo: {(error/exacto*100):.4f}%\n\n"
        
        texto += f"🔢 PUNTOS ALEATORIOS UTILIZADOS (primeros 10):\n"
        for i, punto in enumerate(puntos[:10]):
            texto += f"   Punto {i+1}: x = {punto['x']:.4f}, f(x) = {punto['y']:.4f}\n"
        if len(puntos) > 10:
            texto += f"   ... y {len(puntos)-10} puntos más\n\n"
        
        texto += f"📈 EXPLICACIÓN DEL MÉTODO:\n"
        texto += f"   1. Se generan {n:,} puntos xᵢ aleatorios en [{a}, {b}]\n"
        texto += f"   2. Se evalúa f(xᵢ) en cada punto\n"
        texto += f"   3. Se calcula el promedio: (1/{n}) × Σ f(xᵢ)\n"
        texto += f"   4. Se multiplica por el ancho del intervalo: ({b-a})\n"
        texto += f"   5. Fórmula: ∫f(x)dx ≈ (b-a) × (1/N) × Σ f(xᵢ)\n\n"
        
        texto += f"   Resultado: ({b-a}) × ({resultado/(b-a):.8f}) = {resultado:.8f}\n"
        
        self.vista_1d.mostrar_resultados(texto)
    
    def mostrar_resultados_2d(self, resultado, puntos, func, ax, bx, cy, dy, n):
        """Formatea y muestra resultados para 2D"""
        area = (bx - ax) * (dy - cy)
        
        texto = "="*60 + "\n"
        texto += "INTEGRAL DOBLE - MÉTODO DE MONTE CARLO\n"
        texto += "="*60 + "\n\n"
        
        texto += f"📊 INFORMACIÓN DEL CÁLCULO:\n"
        texto += f"   Función: f(x,y) = {func}\n"
        texto += f"   Intervalo X: [{ax}, {bx}]\n"
        texto += f"   Intervalo Y: [{cy}, {dy}]\n"
        texto += f"   Área de integración: {area:.4f}\n"
        texto += f"   Puntos generados (N): {n:,}\n\n"
        
        texto += f"🎯 RESULTADO DE LA APROXIMACIÓN:\n"
        texto += f"   ∬f(x,y)dxdy ≈ {resultado:.8f}\n\n"
        
        texto += f"🔢 PUNTOS ALEATORIOS UTILIZADOS (primeros 10):\n"
        for i, punto in enumerate(puntos[:10]):
            texto += f"   Punto {i+1}: x = {punto['x']:.3f}, y = {punto['y']:.3f}, f(x,y) = {punto['z']:.4f}\n"
        if len(puntos) > 10:
            texto += f"   ... y {len(puntos)-10} puntos más \n\n"
        texto += f"📈 EXPLICACIÓN DEL MÉTODO 2D:\n"
        texto += f"   1. Se generan {n:,} puntos (xᵢ,yᵢ) en el rectángulo\n"
        texto += f"   2. Se evalúa f(xᵢ,yᵢ) en cada punto\n"
        texto += f"   3. Se calcula el promedio: (1/{n}) × Σ f(xᵢ,yᵢ)\n"
        texto += f"   4. Se multiplica por el área: {area:.4f}\n"
        texto += f"   5. Fórmula: ∬f(x,y)dxdy ≈ Área × (1/N) × Σ f(xᵢ,yᵢ)\n\n"
        
        texto += f"   Resultado: {area:.4f} × ({resultado/area:.8f}) = {resultado:.8f}\n"
        
        self.vista_2d.mostrar_resultados(texto)
    
    def cargar_ejemplo_1d(self, func, a, b, n):
        """Carga un ejemplo en los campos 1D"""
        self.vista_1d.func_1d.delete(0, 'end')
        self.vista_1d.func_1d.insert(0, func)
        self.vista_1d.a_1d.delete(0, 'end')
        self.vista_1d.a_1d.insert(0, a)
        self.vista_1d.b_1d.delete(0, 'end')
        self.vista_1d.b_1d.insert(0, b)
        self.vista_1d.n_1d.delete(0, 'end')
        self.vista_1d.n_1d.insert(0, n)
    
    def cargar_ejemplo_2d(self, func, ax, bx, cy, dy, n):
        """Carga un ejemplo en los campos 2D"""
        self.vista_2d.func_2d.delete(0, 'end')
        self.vista_2d.func_2d.insert(0, func)
        self.vista_2d.ax_2d.delete(0, 'end')
        self.vista_2d.ax_2d.insert(0, ax)
        self.vista_2d.bx_2d.delete(0, 'end')
        self.vista_2d.bx_2d.insert(0, bx)
        self.vista_2d.cy_2d.delete(0, 'end')
        self.vista_2d.cy_2d.insert(0, cy)
        self.vista_2d.dy_2d.delete(0, 'end')
        self.vista_2d.dy_2d.insert(0, dy)
        self.vista_2d.n_2d.delete(0, 'end')
        self.vista_2d.n_2d.insert(0, n)
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.vista.ejecutar()

# Alias para compatibilidad con app.py
Controlador = ControladorMonteCarlo