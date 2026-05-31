# Método de Monte Carlo — Integrales

Aplicación de escritorio que aproxima **integrales simples (1D)** y **dobles (2D)**
usando el método de Monte Carlo, con interfaz gráfica y visualización de resultados.

Proyecto académico (FICCT - UAGRM).

## ¿Qué hace?

- Calcula integrales **1D** `∫f(x)dx` y **2D** `∬f(x,y)dxdy` generando N puntos aleatorios.
- Permite ingresar la función a mano o usar botones (cos, sin, tan, log, ln, etc.).
- Grafica la función y los puntos aleatorios (curva 2D para 1D, superficie 3D para 2D).
- En el modo 1D compara la aproximación con el **valor exacto** (calculado con SymPy) y muestra el error.
- Incluye ejemplos precargados.

## Estructura (MVC)

- `modelo/` — lógica del cálculo Monte Carlo y valor exacto.
- `vista/` — interfaz gráfica (ventana principal + pestañas 1D y 2D).
- `controlador/` — coordina modelo y vista.
- `app.py` — punto de entrada.

## Requisitos

- Python 3.6+
- numpy, matplotlib, sympy (tkinter ya viene con Python)

```bash
pip install numpy matplotlib sympy
```

## Cómo ejecutar

```bash
python app.py
```