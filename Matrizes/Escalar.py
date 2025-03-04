import random

def gerar_matriz(linhas, colunas):
    matriz = []
    for i in range(linhas):
        linha = [random.randint(1, 10) for _ in range(colunas)]
        matriz.append(linha)
    return matriz

def multiplicar_matriz(matriz, escalar):
    matriz_multiplicada = []
    for linha in matriz:
        linha_multiplicada = [elemento * escalar for elemento in linha]
        matriz_multiplicada.append(linha_multiplicada)
    return matriz_multiplicada

matriz = gerar_matriz(3, 3)

matriz_multiplicada = multiplicar_matriz(matriz, 3)

print("Matriz original:")
for linha in matriz:
    print(linha)

print("\nMatriz multiplicada por 3:")
for linha in matriz_multiplicada:
    print(linha)
