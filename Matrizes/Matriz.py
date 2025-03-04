import random


def gerar_matriz(linhas, colunas):
    return [[random.randint(1, 9) for _ in range(colunas)] for _ in range(linhas)]


def multiplicar_matrizes(matriz_a, matriz_b):
    linhas_a, colunas_a = len(matriz_a), len(matriz_a[0])
    linhas_b, colunas_b = len(matriz_b), len(matriz_b[0])

    if colunas_a != linhas_b:
        raise ValueError("O número de colunas da primeira matriz deve ser igual ao número de linhas da segunda matriz.")

    resultado = [[0 for _ in range(colunas_b)] for _ in range(linhas_a)]

    for i in range(linhas_a):
        for j in range(colunas_b):
            soma = 0
            for k in range(colunas_a):
                soma += matriz_a[i][k] * matriz_b[k][j]
            resultado[i][j] = soma

    return resultado


def imprimir_matriz(matriz, nome):
    print(f"\n{nome}:")
    for linha in matriz:
        print(linha)


matriz_2x3 = gerar_matriz(2, 3)
matriz_3x2 = gerar_matriz(3, 2)

resultado = multiplicar_matrizes(matriz_2x3, matriz_3x2)

imprimir_matriz(matriz_2x3, "Matriz 2x3")
imprimir_matriz(matriz_3x2, "Matriz 3x2")
imprimir_matriz(resultado, "Resultado da Multiplicação (2x2)")

