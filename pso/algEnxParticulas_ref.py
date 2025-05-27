import random
import math
import time
import pandas as pd
from utils import gerar_instancia_aleatoria, avaliar_solucao

# Parâmetros do PSO
n_particulas = 30
n_iteracoes = 100
c1 = 1.5
c2 = 1.5
w = 0.8
limite_velocidade = 4

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def binarizar(posicao):
    """Converte posição contínua em solução binária."""
    return [1 if sigmoid(x) >= 0.5 else 0 for x in posicao]

def inicializar_particula(n_itens):
    """Inicializa posição e velocidade de uma partícula."""
    posicao = [random.uniform(-4, -2) for _ in range(n_itens)]
    velocidade = [random.uniform(-1, 1) for _ in range(n_itens)]
    return posicao, velocidade

def calcular_nova_velocidade(vel_atual, pos_atual, melhor_pessoal, melhor_global, indice):
    """Calcula nova velocidade para uma dimensão."""
    r1 = random.random()
    r2 = random.random()
    cog = c1 * r1 * (melhor_pessoal[indice] - pos_atual[indice])
    soc = c2 * r2 * (melhor_global[indice] - pos_atual[indice])
    nova_vel = w * vel_atual[indice] + cog + soc
    return max(min(nova_vel, limite_velocidade), -limite_velocidade)

def atualizar_velocidade(velocidade, posicao, melhor_pessoal, melhor_global):
    """Atualiza velocidade de todas as dimensões."""
    nova_velocidade = []
    for i in range(len(posicao)):
        nova_vel = calcular_nova_velocidade(velocidade, posicao, melhor_pessoal, melhor_global, i)
        nova_velocidade.append(nova_vel)
    return nova_velocidade

def atualizar_posicao(posicao, velocidade):
    """Atualiza posição baseada na velocidade."""
    return [pos + vel for pos, vel in zip(posicao, velocidade)]

def avaliar_particula(posicao, pesos, valores, capacidade):
    """Avalia fitness de uma partícula."""
    solucao_binaria = binarizar(posicao)
    valor, _ = avaliar_solucao(solucao_binaria, pesos, valores, capacidade)
    return valor

def inicializar_enxame(n_itens, pesos, valores, capacidade):
    """Inicializa o enxame completo."""
    particulas = []
    for _ in range(n_particulas):
        posicao, velocidade = inicializar_particula(n_itens)
        valor = avaliar_particula(posicao, pesos, valores, capacidade)
        particulas.append({
            'posicao': posicao,
            'velocidade': velocidade,
            'melhor_posicao': posicao[:],
            'melhor_valor': valor
        })
    return particulas

def encontrar_melhor_global(particulas):
    """Encontra a melhor partícula do enxame."""
    melhor = max(particulas, key=lambda p: p['melhor_valor'])
    return melhor['melhor_posicao'][:], melhor['melhor_valor']

def atualizar_melhor_pessoal(particula, pesos, valores, capacidade):
    """Atualiza melhor posição pessoal se necessário."""
    valor_atual = avaliar_particula(particula['posicao'], pesos, valores, capacidade)
    if valor_atual > particula['melhor_valor']:
        particula['melhor_valor'] = valor_atual
        particula['melhor_posicao'] = particula['posicao'][:]

def pso(n_itens, pesos, valores, capacidade):
    """Executa o algoritmo PSO."""
    # Inicialização
    particulas = inicializar_enxame(n_itens, pesos, valores, capacidade)
    melhor_global, melhor_valor_global = encontrar_melhor_global(particulas)

    # Loop principal
    for _ in range(n_iteracoes):
        for particula in particulas:
            # Atualizar velocidade e posição
            particula['velocidade'] = atualizar_velocidade(
                particula['velocidade'],
                particula['posicao'],
                particula['melhor_posicao'],
                melhor_global
            )
            particula['posicao'] = atualizar_posicao(
                particula['posicao'],
                particula['velocidade']
            )

            # Atualizar melhor pessoal
            atualizar_melhor_pessoal(particula, pesos, valores, capacidade)

            # Verificar se é nova melhor global
            if particula['melhor_valor'] > melhor_valor_global:
                melhor_global = particula['melhor_posicao'][:]
                melhor_valor_global = particula['melhor_valor']

    # Retornar melhor solução
    melhor_solucao = binarizar(melhor_global)
    return melhor_solucao, melhor_valor_global

def executar_teste(n_itens):
    """Executa um teste com n_itens."""
    pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=10)

    inicio = time.time()
    solucao, valor = pso(n_itens, pesos, valores, capacidade)
    fim = time.time()

    peso_total = sum(p * i for p, i in zip(pesos, solucao))

    return {
        "algoritmo": "PSO",
        "n_itens": n_itens,
        "capacidade": capacidade,
        "valor_total": valor,
        "peso_total": peso_total,
        "tempo_execucao": fim - inicio,
        "pesos": pesos,
        "valores": valores,
        "melhor_solucao": solucao
    }

def main():
    tamanhos = [5, 1000, 10000]
    resultados = []

    for n_itens in tamanhos:
        resultado = executar_teste(n_itens)
        resultados.append(resultado)

    df_resultados = pd.DataFrame(resultados)
    return df_resultados

if __name__ == "__main__":
    df_resultados = main()
    print("\nResumo dos resultados de todos os testes:")
    print(df_resultados)