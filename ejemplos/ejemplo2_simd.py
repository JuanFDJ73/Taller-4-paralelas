"""
Taller 4 - Ejercicio 2 (SIMD): MULTIPLICACIÓN DE MATRICES
NumPy vs bucle tradicional en Python
=========================================================
1. 2 Matrices 1000 x 1000 de números aleatorios
2. Realizar la multiplicación de matrices con Numpy
3. Funcion de multiplicación de matrices con bucle tradicional en Python
4. Medir el tiempo de ejecución con y sin Numpy (SIMD). comparar

requisito: 
1. Numpy
2. Presentar resultados en tabla o grafico
3. Explicar la diferencia de tiempos y el concepto de SIMD (Single Instruction Multiple Data)
"""

import random
import time
import numpy as np

# N = 1000 realiza 10^9 operaciones en Python puro se demorara mas de lo normal
N = 1000

print(f"=== Multiplicación de Matrices ({N}x{N}) ===")

# 1. Crear matrices aleatorias
# Versión Python puro (listas de listas)
matriz_a_py = [
    [random.random() for _ in range(N)]
    for _ in range(N)
]
matriz_b_py = [
    [random.random() for _ in range(N)]
    for _ in range(N)
]

# Versión NumPy (arreglos continuos en memoria)
matriz_a_np = np.array(matriz_a_py, dtype=np.float64)
matriz_b_np = np.array(matriz_b_py, dtype=np.float64)


# 2. Multiplicación tradicional con bucles anidados (Python puro)
def multiplicar_tradicional(A, B, n):
    """
    Multiplicación tradicional C = A x B con complejidad O(N^3).
    N^3 por los 3 For anidados. Cada iteración realiza una suma y una multiplicación.
    """
    # Inicializar matriz resultado en ceros
    C = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            suma = 0.0
            for k in range(n):
                suma += A[i][k] * B[k][j]
            C[i][j] = suma
    return C


# Medición: Python tradicional
inicio = time.perf_counter()
resultado_py = multiplicar_tradicional(matriz_a_py, matriz_b_py, N)
tiempo_tradicional = time.perf_counter() - inicio


# 3. Multiplicación con NumPy (SIMD / BLAS)
inicio = time.perf_counter()
resultado_np = np.matmul(matriz_a_np, matriz_b_np)  # o matriz_a_np @ matriz_b_np
tiempo_numpy = time.perf_counter() - inicio


# Verificación de consistencia (tolerancia de precisión flotante)
es_correcto = np.allclose(resultado_py, resultado_np)
speedup = tiempo_tradicional / tiempo_numpy if tiempo_numpy > 0 else float("inf")

# 4. Tabla de resultados en consola
print("\n" + "=" * 55)
print(f"{'MÉTODO':<25} | {'TIEMPO (s)':<12} | {'ACELERACIÓN':<12}")
print("-" * 55)
print(f"{'Bucle tradicional (Python)':<25} | {tiempo_tradicional:<12.6f} | {'1.0x (base)':<12}")
print(f"{'NumPy (@ / matmul)':<25} | {tiempo_numpy:<12.6f} | {f'{speedup:.1f}x':<12}")
print("=" * 55)
print(f"Resultados numéricamente equivalentes: {es_correcto}")