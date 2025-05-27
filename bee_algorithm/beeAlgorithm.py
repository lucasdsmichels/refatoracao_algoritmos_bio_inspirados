import random
import time
import numpy as np
import pandas as pd

def avaliar_solucao(solucao, pesos, valores, capacidade):
    peso_total = sum(p for i, p in enumerate(pesos) if solucao[i] == 1)
    valor_total = sum(v for i, v in enumerate(valores) if solucao[i] == 1)
    if peso_total > capacidade:
        return 0, peso_total  
    return valor_total, peso_total

def gerar_solucao(n):
    return [random.randint(0, 1) for _ in range(n)]

def gerar_vizinho(solucao):
    vizinho = solucao[:]
    idx = random.randint(0, len(solucao) - 1)
    vizinho[idx] = 1 - vizinho[idx]
    return vizinho

def bee_algorithm(pesos, valores, capacidade, n_abelhas=30, n_melhores=10, n_vizinhos=2, n_iter=50):
    n = len(pesos)
    melhores_solucoes = []

    for _ in range(n_iter):
        abelhas = [gerar_solucao(n) for _ in range(n_abelhas)]
        avaliacoes = [(sol, *avaliar_solucao(sol, pesos, valores, capacidade)) for sol in abelhas]
        avaliacoes.sort(key=lambda x: x[1], reverse=True)
        melhores = avaliacoes[:n_melhores]
        
        novas_solucoes = []
        for sol, _, _ in melhores:
            vizinhos = [gerar_vizinho(sol) for _ in range(n_vizinhos)]
            vizinhos.append(sol)
            viz_avaliadas = [(v, *avaliar_solucao(v, pesos, valores, capacidade)) for v in vizinhos]
            melhor_vizinho = max(viz_avaliadas, key=lambda x: x[1])
            novas_solucoes.append(melhor_vizinho)

        melhores_solucoes.extend(novas_solucoes)

    melhor_global = max(melhores_solucoes, key=lambda x: x[1])
    return melhor_global[0], melhor_global[1], melhor_global[2]

def gerar_instancia_aleatoria(num_itens, max_peso=10, max_valor=50):
    pesos = [random.randint(1, max_peso) for _ in range(num_itens)]
    valores = [random.randint(1, max_valor) for _ in range(num_itens)]
    capacidade = random.randint(int(sum(pesos) * 0.3), int(sum(pesos) * 0.6))
    return pesos, valores, capacidade

def main():
    testes_aleatorios = []
    for i, n in enumerate([5, 1000, 10000], start=1):
        pesos, valores, capacidade = gerar_instancia_aleatoria(n)
        inicio = time.time()
        solucao, valor, peso = bee_algorithm(pesos, valores, capacidade)
        fim = time.time()

        testes_aleatorios.append({
            "algoritmo": "Bee Algorithm",
            "n_itens": n,
            "capacidade": capacidade,
            "valor_total": valor,
            "peso_total": peso,
            "tempo_execucao": round(fim - inicio, 5),
            "pesos": pesos,
            "valores": valores,
            "melhor_solucao": solucao
        })

    df = pd.DataFrame(testes_aleatorios)

    return df
