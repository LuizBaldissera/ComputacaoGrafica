import random

def gerar_matriz_quadrada(n):
    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]

def eh_matriz_diagonal(matriz):
    tamanho = len(matriz)
    for i in range(tamanho):
        for j in range(tamanho):
            if i != j and matriz[i][j] != 0:
                return False
    return True

def imprimir_matriz(matriz, nome):
    print(f"\n{nome}:")
    for linha in matriz:
        print(linha)

tamanho = int(input("Digite o tamanho da matriz quadrada: "))
matriz = gerar_matriz_quadrada(tamanho)

imprimir_matriz(matriz, "Matriz Gerada")
if eh_matriz_diagonal(matriz):
    print("A matriz é diagonal.")
else:
    print("A matriz não é diagonal.")
