import random
import time
import pandas as pd

def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20):
    pesos = [random.randint(1, max_peso) for _ in range(n_itens)]
    valores = [random.randint(1, max_valor) for _ in range(n_itens)]
    capacidade = random.randint(int(0.3 * sum(pesos)), int(0.6 * sum(pesos)))
    return pesos, valores, capacidade

def avaliar(solucao, pesos, valores, capacidade):
    peso_total = sum(p * i for p, i in zip(pesos, solucao))
    valor_total = sum(v * i for v, i in zip(valores, solucao))
    if peso_total > capacidade:
        return 0, peso_total
    return valor_total, peso_total

def aco_knapsack(pesos, valores, capacidade, n_formigas=50, n_iteracoes=50, alfa=1.0, beta=2.0, rho=0.1, Q=100):
    n = len(pesos)
    feromonio = [1.0] * n
    melhor_solucao = None
    melhor_valor = 0
    melhor_peso = 0

    for _ in range(n_iteracoes):
        for _ in range(n_formigas):
            solucao = [0] * n
            peso_total = 0
            for i in range(n):
                if peso_total + pesos[i] <= capacidade:
                    atratividade = (valores[i] / pesos[i]) if pesos[i] > 0 else 0
                    prob = (feromonio[i] ** alfa) * (atratividade ** beta)
                    if random.random() < prob / (1 + prob):  
                        solucao[i] = 1
                        peso_total += pesos[i]
            valor, peso = avaliar(solucao, pesos, valores, capacidade)
            if valor > melhor_valor:
                melhor_solucao = solucao
                melhor_valor = valor
                melhor_peso = peso

        for i in range(n):
            feromonio[i] *= (1 - rho)
            if melhor_solucao and melhor_solucao[i] == 1:
                feromonio[i] += Q / (1 + melhor_peso)

    return melhor_solucao, melhor_valor, melhor_peso

def main():
    testes = []
    for i, n_itens in enumerate([5, 1000, 10000], start=1):
        pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens)
        inicio = time.time()
        solucao, valor, peso = aco_knapsack(pesos, valores, capacidade)
        fim = time.time()

        testes.append({
            "algoritmo": "Algoritmo ACO",
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