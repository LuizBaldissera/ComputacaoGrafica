import random

def gerar_matriz_identidade(n):
    return [[1 if i
== j else 0 for j in range(n)] for i in range(n)]

def eh_matriz_identidade(matriz):
    tamanho = len(matriz)
    for i in range(tamanho):
        for j in range(tamanho):
            if (i == j and matriz[i][j] != 1) or (i != j and matriz[i][j] != 0):
                return False
    return True

def imprimir_matriz(matriz, nome):
    print(f"\n{nome}:")
    for linha in matriz:
        print(linha)

# Gerando uma matriz identidade
tamanho = int(input("Digite o tamanho da matriz identidade: "))
matriz = gerar_matriz_identidade(tamanho)

# Verificando se é identidade
imprimir_matriz(matriz, "Matriz Identidade")
if eh_matriz_identidade(matriz):
    print("A matriz é uma identidade.")
else:
    print("A matriz não é uma identidade.")
