import random
import time
import pandas as pd

def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20):
    pesos = [random.randint(1, max_peso) for _ in range(n_itens)]
    valores = [random.randint(1, max_valor) for _ in range(n_itens)]
    capacidade = random.randint(int(0.3 * sum(pesos)), int(0.6 * sum(pesos)))
    return pesos, valores, capacidade

def avaliar(solucao_binaria, pesos, valores, capacidade):
    peso_total = sum(p * i for p, i in zip(pesos, solucao_binaria))
    valor_total = sum(v * i for v, i in zip(valores, solucao_binaria))
    if peso_total > capacidade:
        return 0, peso_total
    return valor_total, peso_total

def gerar_solucao(n):
    return [random.randint(0, 1) for _ in range(n)]

def levy_flight(solucao):
    nova_solucao = solucao[:]
    for i in range(len(nova_solucao)):
        if random.random() < 0.5:
            nova_solucao[i] = 1 - nova_solucao[i]
    return nova_solucao

def cuckoo_search(pesos, valores, capacidade, n_ninhos=25, n_iteracoes=50, pa=0.25):
    n = len(pesos)
    ninhos = [gerar_solucao(n) for _ in range(n_ninhos)]
    fitness = [avaliar(ninho, pesos, valores, capacidade)[0] for ninho in ninhos]
    melhor_ninho = ninhos[fitness.index(max(fitness))]

    for _ in range(n_iteracoes):
        for i in range(n_ninhos):
            novo_ninho = levy_flight(ninhos[i])
            novo_fitness, _ = avaliar(novo_ninho, pesos, valores, capacidade)
            if novo_fitness > fitness[i]:
                ninhos[i] = novo_ninho
                fitness[i] = novo_fitness

        n_abandonados = int(pa * n_ninhos)
        for _ in range(n_abandonados):
            idx = random.randint(0, n_ninhos - 1)
            ninhos[idx] = gerar_solucao(n)
            fitness[idx] = avaliar(ninhos[idx], pesos, valores, capacidade)[0]

        melhor_ninho = ninhos[fitness.index(max(fitness))]

    melhor_valor, melhor_peso = avaliar(melhor_ninho, pesos, valores, capacidade)
    return melhor_ninho, melhor_valor, melhor_peso

def main():
    testes = []
    for i, n_itens in enumerate([5, 1000, 10000], start=1):
        pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens)
        inicio = time.time()
        solucao, valor, peso = cuckoo_search(pesos, valores, capacidade)
        fim = time.time()

        testes.append({
            "algoritmo": "Cuckoo Search",
            "n_itens": n_itens,
            "capacidade": capacidade,
            "valor_total": valor,
            "peso_total": peso,
            "tempo_execucao": round(fim - inicio, 5),
            "pesos": pesos,
            "valores": valores,
            "melhor_solucao": solucao
        })

    df = pd.DataFrame(testes)

    return df