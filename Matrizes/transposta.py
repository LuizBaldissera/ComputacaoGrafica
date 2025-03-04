import random

def gerar_matriz(linhas, colunas):
    return [[random.randint(1, 9) for _ in range(colunas)] for _ in range(linhas)]

def transpor_matriz(matriz):
    linhas, colunas = len(matriz), len(matriz[0])
    return [[matriz[j][i] for j in range(linhas)] for i in range(colunas)]

def imprimir_matriz(matriz, nome):
    print(f"\n{nome}:")
    for linha in matriz:
        print(linha)

tamanho_linhas = int(input("Digite o número de linhas da matriz: "))
tamanho_colunas = int(input("Digite o número de colunas da matriz: "))
matriz = gerar_matriz(tamanho_linhas, tamanho_colunas)

matriz_transposta = transpor_matriz(matriz)

imprimir_matriz(matriz, "Matriz Original")
imprimir_matriz(matriz_transposta, "Matriz Transposta")
