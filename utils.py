import random

def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20, proporcao_capacidade=(0.3, 0.6)):
    pesos = [random.randint(1, max_peso) for _ in range(n_itens)]
    valores = [random.randint(1, max_valor) for _ in range(n_itens)]
    capacidade = random.randint(int(sum(pesos) * proporcao_capacidade[0]), int(sum(pesos) * proporcao_capacidade[1]))
    return pesos, valores, capacidade

def avaliar_solucao(solucao, pesos, valores, capacidade):
    peso_total = sum(p * s for p, s in zip(pesos, solucao))
    valor_total = sum(v * s for v, s in zip(valores, solucao))
    if peso_total > capacidade:
        return 0, peso_total
    return valor_total, peso_total

def gerar_solucao_binaria(n):
    return [random.randint(0, 1) for _ in range(n)]

def gerar_vizinho(solucao):
    vizinho = solucao[:]
    idx = random.randint(0, len(solucao) - 1)
    vizinho[idx] = 1 - vizinho[idx]
    return vizinho
