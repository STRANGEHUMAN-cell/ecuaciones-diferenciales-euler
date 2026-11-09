"""Solución analítica y aproximación con Euler para y' = y, y(0) = 1."""
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

T_INICIAL = 0.0
T_FINAL = 1.0
H = 0.2
Y_INICIAL = 1.0


def f(t: float, y: float) -> float:
    """Ecuación diferencial separable: dy/dt = y."""
    return y


def solucion_exacta(t: float) -> float:
    """Por separación de variables: y(t) = e^t."""
    return math.exp(t)


def metodo_euler(t0: float, tf: float, y0: float, h: float):
    """Calcula la aproximación de Euler de y' = y."""
    if h <= 0 or tf < t0:
        raise ValueError("Se requiere h > 0 y tf >= t0.")
    pasos_reales = (tf - t0) / h
    pasos = round(pasos_reales)
    if not math.isclose(pasos_reales, pasos, rel_tol=0, abs_tol=1e-9):
        raise ValueError("El paso h debe dividir exactamente el intervalo.")

    t, y = t0, y0
    puntos = [(t, y)]
    for n in range(pasos):
        y = y + h * f(t, y)
        t = round(t0 + (n + 1) * h, 10)
        puntos.append((t, y))
    return puntos


def comparar(puntos):
    return [
        (t, y_euler, solucion_exacta(t), abs(solucion_exacta(t) - y_euler))
        for t, y_euler in puntos
    ]


def guardar_csv(filas, ruta: Path):
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["t", "Euler", "Solucion exacta", "Error absoluto"])
        for fila in filas:
            escritor.writerow([f"{v:.8f}" for v in fila])


def guardar_grafica(filas, ruta: Path):
    tiempos = [fila[0] for fila in filas]
    aproximaciones = [fila[1] for fila in filas]
    exactos = [fila[2] for fila in filas]
    tiempos_suaves = [T_INICIAL + i * (T_FINAL - T_INICIAL) / 200 for i in range(201)]
    curva_exacta = [solucion_exacta(t) for t in tiempos_suaves]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(tiempos_suaves, curva_exacta, label="Solución exacta: e^t", linewidth=2.4)
    ax.plot(tiempos, aproximaciones, "o--", label="Método de Euler (h = 0.2)", linewidth=2)
    ax.scatter(tiempos, exactos, s=30, marker="x", label="Valores exactos en la malla")
    ax.set_title("Comparación: solución exacta y método de Euler")
    ax.set_xlabel("Tiempo t")
    ax.set_ylabel("y(t)")
    ax.set_xlim(T_INICIAL, T_FINAL)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=180)
    plt.close(fig)


def main():
    puntos = metodo_euler(T_INICIAL, T_FINAL, Y_INICIAL, H)
    filas = comparar(puntos)

    print("Ecuación diferencial: dy/dt = y, con y(0) = 1")
    print("Solución analítica exacta: y(t) = e^t")
    print("Método de Euler: y_(n+1) = y_n + 0.2*y_n\n")
    print(f"{'t':>5} {'Euler':>14} {'Exacta':>14} {'Error absoluto':>18}")
    for t, euler, exacta, error in filas:
        print(f"{t:5.1f} {euler:14.6f} {exacta:14.6f} {error:18.6f}")

    print(f"\nError absoluto final en t = 1: {filas[-1][3]:.6f}")
    carpeta = Path(__file__).resolve().parent
    guardar_csv(filas, carpeta / "resultados.csv")
    guardar_grafica(filas, carpeta / "comparacion_euler.png")
    print("Archivos generados: resultados.csv y comparacion_euler.png")


if __name__ == "__main__":
    main()
