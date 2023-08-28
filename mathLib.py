from math import isclose

def multiplicar_matrices(matriz1, matriz2):
    filas_matriz1 = len(matriz1)
    columnas_matriz1 = len(matriz1[0])
    filas_matriz2 = len(matriz2)
    columnas_matriz2 = len(matriz2[0])

    # Verificar si las matrices se pueden multiplicar
    if columnas_matriz1 != filas_matriz2:
        print("No se pueden multiplicar las matrices.")
        return None

    # Crear una matriz de resultado con las dimensiones adecuadas
    matriz_resultado = [[0 for y in range(columnas_matriz2)] for x in range(filas_matriz1)]

    # Realizar la multiplicación de matrices
    for i in range(filas_matriz1):
        for j in range(columnas_matriz2):
            for k in range(columnas_matriz1):
                matriz_resultado[i][j] += matriz1[i][k] * matriz2[k][j]

    return matriz_resultado

def multiplicar_matriz_vector(matriz,vector):
    filas_matriz = len(matriz)
    columnas_matriz = len(matriz[0])
    filas_vector = len(vector)

    # Verificar si las matrices se pueden multiplicar
    if columnas_matriz!= filas_vector:
        print("No se puede multiplicar la matriz por el vector.")
        return None

    # Crear un vector de resultado con las dimensiones adecuadas
    vector_resultado = [0 for x in range(filas_matriz)]

    # Realizar la multiplicación matriz-vector
    for i in range(filas_matriz):
        for k in range(columnas_matriz):
            vector_resultado[i] += matriz[i][k] * vector[k]

    return vector_resultado

def barycentricCoords(A, B, C, P):
    # Se saca el área de los subtriángulos y del triángulo
    # mayor usando el Shoelace Theorem, una fórmula que permite
    # sacar el área de un polígono de cualquier cantidad de vértices.

    areaPCB = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) -
                  (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))

    areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) -
                  (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))

    areaABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) -
                  (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))

    areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) -
                  (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    # Si el área del triángulo es 0, retornar nada para
    # prevenir división por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baricéntricas dividiendo el
    # área de cada subtriángulo por el área del triángulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada está entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son válidas.
    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and isclose(u + v + w, 1.0):
        return (u, v, w)
    else:
        return None

def matriz_transpuesta(matriz):
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]

def matriz_adjunta(matriz):
    adjunta = []
    for i in range(len(matriz)):
        fila_adjunta = []
        for j in range(len(matriz)):
            submatriz = [fila[:j] + fila[j+1:] for fila in (matriz[:i]+matriz[i+1:])]
            cofactor = ((-1)**(i+j)) * determinante(submatriz)
            fila_adjunta.append(cofactor)
        adjunta.append(fila_adjunta)
    return matriz_transpuesta(adjunta)

def determinante(matriz):
    if len(matriz) == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    det = 0
    for i in range(len(matriz)):
        submatriz = [fila[1:] for fila in matriz[:i] + matriz[i+1:]]
        det += ((-1)**i) * matriz[i][0] * determinante(submatriz)
    return det

def matriz_inversa(matriz):
    det = determinante(matriz)
    if det == 0:
        raise ValueError("La matriz no tiene inversa.")
    adjunta = matriz_adjunta(matriz)
    inversa = [[adjunta[i][j] / det for j in range(len(adjunta))] for i in range(len(adjunta))]
    return inversa


def producto_cruz(vector1, vector2):
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Los vectores deben tener tres componentes.")

    a1, a2, a3 = vector1
    b1, b2, b3 = vector2

    producto_cruz_x = a2 * b3 - a3 * b2
    producto_cruz_y = a3 * b1 - a1 * b3
    producto_cruz_z = a1 * b2 - a2 * b1

    return (producto_cruz_x, producto_cruz_y, producto_cruz_z)


def subtract_arrays(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Los arrays deben tener la misma longitud.")

    result = []
    for i in range(len(array1)):
        result.append(array1[i] - array2[i])

    return tuple(result)


def calcular_norma(vector):
    suma_cuadrados = sum(componente ** 2 for componente in vector)
    norma = suma_cuadrados ** 0.5
    return norma

def normalizar_vector(vector):
    norma = calcular_norma(vector)
    if norma == 0:
        raise ValueError("No se puede normalizar un vector nulo.")

    vector_normalizado = [componente/norma for componente in vector]

    return tuple(vector_normalizado)


def producto_punto(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud")

    product = sum(x * y for x, y in zip(vector1, vector2))
    return product
