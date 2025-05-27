import random
import time
import pandas as pd

def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20):
    pesos = [random.randint(1, max_peso) for _ in range(n_itens)]
    valores = [random.randint(1, max_valor) for _ in range(n_itens)]
    capacidade = random.randint(int(sum(pesos) * 0.3), int(sum(pesos) * 0.6))
    return pesos, valores, capacidade

def gerar_individuo(n_itens):
    return [random.randint(0, 1) for _ in range(n_itens)]

def avaliar_individuo(individuo, pesos, valores, capacidade):
    peso_total = sum(p * i for p, i in zip(pesos, individuo))
    valor_total = sum(v * i for v, i in zip(valores, individuo))
    if peso_total > capacidade:
        excesso = peso_total - capacidade

        return valor_total - excesso * 2 
    return valor_total

def selecao(populacao, pesos, valores, capacidade):
    torneio = random.sample(populacao, 3)
    torneio.sort(key=lambda ind: avaliar_individuo(ind, pesos, valores, capacidade), reverse=True)
    return torneio[0], torneio[1]

def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    return pai1[:ponto] + pai2[ponto:], pai2[:ponto] + pai1[ponto:]

def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]
    return individuo

def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
    n_itens = len(pesos)
    populacao = [gerar_individuo(n_itens) for _ in range(tam_populacao)]
    melhor_solucao = None
    melhor_valor = 0

    for _ in range(n_geracoes):
        nova_populacao = []
        for _ in range(tam_populacao // 2):
            pai1, pai2 = selecao(populacao, pesos, valores, capacidade)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao

        for individuo in populacao:
            valor = avaliar_individuo(individuo, pesos, valores, capacidade)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_solucao = individuo

        return melhor_solucao, melhor_valor

def main():
    testes = []
    for i, n in enumerate([5, 1000, 10000], start=1):
        pesos, valores, capacidade = gerar_instancia_aleatoria(n)
        inicio = time.time()
        solucao, valor = algoritmo_genetico(pesos, valores, capacidade)
        fim = time.time()
        peso_total = sum(p * i for p, i in zip(pesos, solucao))

        testes.append({
            "algoritmo": "Algoritmo Genético",
            "n_itens": n,
            "capacidade": capacidade,
            "valor_total": valor,
            "peso_total": peso_total,
            "tempo_execucao": round(fim - inicio, 5),
            "pesos": pesos,
            "valores": valores,
            "melhor_solucao": solucao
        })

    df = pd.DataFrame(testes)

    return df

if __name__ == "__main__":
    main()