"""
Taller 4 - Ejercicio 1 (SMP): SUMA DE UNA MATRIZ CON HILOS
==========================================================
1. Crear una matriz 1000 x 1000 de números aleatorios
2. Dividir la matriz en bloques de 100x100 y asignar bloque a cada hilo
3. Cada hilo suma su bloque y devuelve el resultado parcial
4. Combinar los resultados parciales para obtener la suma total

Medir el tiempo de ejecución con y sin hilos (SMP)
"""

import random
import threading
import time

TamanoMatrizX = 1000
TamanoMatrizY = 1000
Tamano_bloque = 100

# Crear la matriz
matriz = [
    [random.randint(0, 9) for _ in range(TamanoMatrizX)]
    for _ in range(TamanoMatrizY)
]


# Dividir la matriz en bloques de 100 x 100
bloques = [
    [
        matriz[fila_inicio + i][columna_inicio:columna_inicio + Tamano_bloque]
        for i in range(Tamano_bloque)
    ]
    for fila_inicio in range(0, TamanoMatrizY, Tamano_bloque)
    for columna_inicio in range(0, TamanoMatrizX, Tamano_bloque)
]


# Lista donde cada hilo guardará su resultado
resultados_parciales = [0] * len(bloques)


def sumar_bloque(bloque, indice):
    """Suma un bloque y guarda el resultado parcial."""
    suma = 0

    for fila in bloque:
        suma += sum(fila)

    resultados_parciales[indice] = suma


# Suma secuencial, sin hilos
inicio = time.perf_counter()

suma_secuencial = 0

for fila in matriz:
    suma_secuencial += sum(fila)

tiempo_secuencial = time.perf_counter() - inicio


# Suma usando hilos
inicio = time.perf_counter()

hilos = []

for indice, bloque in enumerate(bloques):
    hilo = threading.Thread(
        target=sumar_bloque,
        args=(bloque, indice)
    )

    hilos.append(hilo)
    hilo.start()


# Esperar a que terminen todos los hilos
for hilo in hilos:
    hilo.join()


suma_total = sum(resultados_parciales)
tiempo_hilos = time.perf_counter() - inicio


# Mostrar resultados
print("SUMA DE MATRIZ CON HILOS")
print(f"Tamaño de la matriz: {TamanoMatrizX} x {TamanoMatrizY}")
print(f"Tamaño de cada bloque: {Tamano_bloque} x {Tamano_bloque}")
print(f"Cantidad de bloques: {len(bloques)}")
print()
print(f"Resultados parciales: {resultados_parciales}")
print(f"Suma secuencial: {suma_secuencial}")
print(f"Suma con hilos: {suma_total}")
print()
print(f"Tiempo secuencial: {tiempo_secuencial:.6f} segundos")
print(f"Tiempo con hilos: {tiempo_hilos:.6f} segundos")
print(f"Resultados iguales: {suma_secuencial == suma_total}")