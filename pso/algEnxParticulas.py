import random
import math
import time
import pandas as pd  

def gerar_dados(n_itens):
    pesos = [random.randint(1, 10) for _ in range(n_itens)]
    valores = [random.randint(1, 10) for _ in range(n_itens)]
    capacidade = int(0.2 * sum(pesos))  
    return pesos, valores, capacidade

n_particulas = 30
n_iteracoes = 100
c1 = 1.5
c2 = 1.5
w = 0.8
limite_velocidade = 4

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def avaliar(solucao_binaria, pesos, valores, capacidade):
    peso_total = sum(p * i for p, i in zip(pesos, solucao_binaria))
    valor_total = sum(v * i for v, i in zip(valores, solucao_binaria))
    if peso_total > capacidade:
        return 0
    return valor_total

class Particula:
    def __init__(self, n_itens, pesos, valores, capacidade):
        self.n_itens = n_itens
        self.pesos = pesos
        self.valores = valores
        self.capacidade = capacidade
        self.posicao = [random.uniform(-4, -2) for _ in range(n_itens)]
        self.velocidade = [random.uniform(-1, 1) for _ in range(n_itens)]
        self.best_posicao = self.posicao[:]
        self.best_valor = avaliar(self.binarizar(), pesos, valores, capacidade)

    def binarizar(self):
        return [1 if sigmoid(x) >= 0.5 else 0 for x in self.posicao]

    def atualizar_velocidade(self, global_best):
        for i in range(len(self.posicao)):
            r1 = random.random()
            r2 = random.random()
            cog = c1 * r1 * (self.best_posicao[i] - self.posicao[i])
            soc = c2 * r2 * (global_best[i] - self.posicao[i])
            nova_vel = w * self.velocidade[i] + cog + soc
            nova_vel = max(min(nova_vel, limite_velocidade), -limite_velocidade)
            self.velocidade[i] = nova_vel

    def atualizar_posicao(self):
        for i in range(len(self.posicao)):
            self.posicao[i] += self.velocidade[i]

    def atualizar_pessoal(self):
        bin_pos = self.binarizar()
        valor = avaliar(bin_pos, self.pesos, self.valores, self.capacidade)
        if valor > self.best_valor:
            self.best_valor = valor
            self.best_posicao = self.posicao[:]

def pso(n_itens, pesos, valores, capacidade):
    enxame = [Particula(n_itens, pesos, valores, capacidade) for _ in range(n_particulas)]
    global_best = enxame[0].posicao[:]
    global_best_valor = avaliar(enxame[0].binarizar(), pesos, valores, capacidade)

    for iteracao in range(n_iteracoes):
        for particula in enxame:
            particula.atualizar_velocidade(global_best)
            particula.atualizar_posicao()
            particula.atualizar_pessoal()

            valor = avaliar(particula.binarizar(), pesos, valores, capacidade)
            if valor > global_best_valor:
                global_best = particula.posicao[:]
                global_best_valor = valor


    melhor_solucao = [1 if sigmoid(x) >= 0.5 else 0 for x in global_best]
    return melhor_solucao, global_best_valor

def main():
    tamanhos = [5, 1000, 10000]  
    resultados = [] 

    for n_itens in tamanhos:
        pesos, valores, capacidade = gerar_dados(n_itens)
        
        inicio = time.time()
        solucao, valor = pso(n_itens, pesos, valores, capacidade)
        fim = time.time()
        peso_total = sum(p * i for p, i in zip(pesos, solucao))

        tempo_execucao = fim - inicio
        resultados.append({
            "algoritmo": "PSO",
            "n_itens": n_itens,
            "capacidade": capacidade,
            "valor_total": valor,
            "peso_total": peso_total,
            "tempo_execucao": tempo_execucao,
            "pesos": pesos,
            "valores": valores,
            "melhor_solucao": solucao
        })

    df_resultados = pd.DataFrame(resultados)
    return df_resultados

if __name__ == "__main__":
    df_resultados = main()

    print("\nResumo dos resultados de todos os testes:")
    print(df_resultados)