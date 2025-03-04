import math


def ler_vetor():
    x = float(input("Digite o valor de x: "))
    y = float(input("Digite o valor de y: "))
    z = float(input("Digite o valor de z: "))
    return [x, y, z]


def calcular_tamanho(vetor):
    return math.sqrt(vetor[0] ** 2 + vetor[1] ** 2 + vetor[2] ** 2)


def normalizar_vetor(vetor):
    tamanho = calcular_tamanho(vetor)
    if tamanho == 0:
        return [0, 0, 0]
    return [vetor[0] / tamanho, vetor[1] / tamanho, vetor[2] / tamanho]


def adicionar_vetores(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


def subtrair_vetores(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]


def multiplicar_por_escalar(vetor, escalar):
    return [vetor[0] * escalar, vetor[1] * escalar, vetor[2] * escalar]


def dividir_por_escalar(vetor, escalar):
    if escalar == 0:
        print("Erro: divisão por zero.")
        return vetor
    return [vetor[0] / escalar, vetor[1] / escalar, vetor[2] / escalar]


def produto_escalar(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


vetor = ler_vetor()
while True:
    print("\nMenu:")
    print("1) Calcular o tamanho do vetor")
    print("2) Normalizar o vetor")
    print("3) Adicionar outro vetor")
    print("4) Subtrair outro vetor")
    print("5) Multiplicar por um escalar")
    print("6) Dividir por um escalar")
    print("7) Calcular o produto escalar com outro vetor")
    print("8) Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        print("Tamanho do vetor:", calcular_tamanho(vetor))
    elif opcao == '2':
        print("Vetor normalizado:", normalizar_vetor(vetor))
    elif opcao == '3':
        novo_vetor = ler_vetor()
        vetor = adicionar_vetores(vetor, novo_vetor)
        print("Vetor resultante:", vetor)
    elif opcao == '4':
        novo_vetor = ler_vetor()
        vetor = subtrair_vetores(vetor, novo_vetor)
        print("Vetor resultante:", vetor)
    elif opcao == '5':
        escalar = float(input("Digite o escalar: "))
        vetor = multiplicar_por_escalar(vetor, escalar)
        print("Vetor resultante:", vetor)
    elif opcao == '6':
        escalar = float(input("Digite o escalar: "))
        vetor = dividir_por_escalar(vetor, escalar)
        print("Vetor resultante:", vetor)
    elif opcao == '7':
        novo_vetor = ler_vetor()
        print("Produto escalar:", produto_escalar(vetor, novo_vetor))
    elif opcao == '8':
        break
    else:
        print("Opção inválida. Tente novamente.")