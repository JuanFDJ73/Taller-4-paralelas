"""
Taller 4 - Ejercicio Integrador: SIMULACIÓN DE UN SISTEMA HÍBRIDO SMP-SIMD
==========================================================================
1. Crea una matriz de 10000x10000 con números aleatorios.
2. Divide la matriz en bloques de 1000x1000 y asigna cada bloque a un hilo (SMP).
3. Dentro de cada hilo, utiliza NumPy para operaciones SIMD (suma de columnas/filas).
4. Combina los resultados de todos los hilos para obtener la suma total.
5. Mide el tiempo de ejecución y compáralo con una versión secuencial.
"""

import threading
import time
import numpy as np

# Dimensiones
N = 10000
Tamano_bloque = 1000

print(f"1. Generando matriz de {N}x{N}...")
matriz = np.random.rand(N, N)

# 2 Dividir la matriz en bloques de 1000x1000 (SMP)
bloques = [
    matriz[i:i + Tamano_bloque, j:j + Tamano_bloque]
    for i in range(0, N, Tamano_bloque)
    for j in range(0, N, Tamano_bloque)
]

num_bloques = len(bloques)
resultados_parciales = [0.0] * num_bloques


# 3 Operación dentro del hilo: SIMD por columnas y luego reducción
def sumar_bloque_simd(bloque, indice):
    # Paso SIMD 1: suma vectorial a lo largo de las columnas (axis=0)
    suma_columnas = np.sum(bloque, axis=0)
    # Paso SIMD 2: reducción final del vector resultante
    resultados_parciales[indice] = np.sum(suma_columnas)


# 5. VERSIÓN SECUENCIAL (sin concurrencia SMP)
print("Ejecutando versión secuencial...")
inicio_sec = time.perf_counter()

# Suma secuencial bloque a bloque (un solo hilo de control)
suma_secuencial = 0.0
for b in bloques:
    suma_secuencial += np.sum(np.sum(b, axis=0))

tiempo_secuencial = time.perf_counter() - inicio_sec



# VERSIÓN HÍBRIDA (SMP con hilos + SIMD con NumPy)
print("Ejecutando versión híbrida (SMP + SIMD)...")
inicio_hib = time.perf_counter()

hilos = []
for idx, bloque in enumerate(bloques):
    hilo = threading.Thread(
        target=sumar_bloque_simd,
        args=(bloque, idx)
    )
    hilos.append(hilo)
    hilo.start()

# 4. Esperar finalización y combinar resultados
for hilo in hilos:
    hilo.join()

suma_hibrida = sum(resultados_parciales)
tiempo_hibrido = time.perf_counter() - inicio_hib


# Métricas y comprobación
es_equivalente = np.isclose(suma_secuencial, suma_hibrida)
speedup = tiempo_secuencial / tiempo_hibrido if tiempo_hibrido > 0 else 1.0

print("\n" + "=========================================================================")
print("RESULTADOS DEL SISTEMA HÍBRIDO SMP-SIMD")
print("=========================================================================")
print(f"Dimensiones de matriz : {N} x {N} ({N * N:,} elementos)")
print(f"Tamaño de bloque      : {Tamano_bloque} x {Tamano_bloque}")
print(f"Total de hilos/bloques: {num_bloques}")
print("=========================================================================")
print(f"Suma Secuencial       : {suma_secuencial:.4f}")
print(f"Suma Híbrida          : {suma_hibrida:.4f}")
print(f"¿Resultados iguales?  : {es_equivalente}")
print("=========================================================================")
print(f"Tiempo Secuencial     : {tiempo_secuencial:.6f} segundos")
print(f"Tiempo Híbrido        : {tiempo_hibrido:.6f} segundos")
print(f"Speedup (Aceleración) : {speedup:.2f}x")
print("=========================================================================")