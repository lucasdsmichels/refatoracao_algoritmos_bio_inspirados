import random
import time
import numpy as np
import pandas as pd
from utils import avaliar_solucao, gerar_solucao_binaria, gerar_vizinho, gerar_instancia_aleatoria

def gerar_solucao_aleatoria(n):
    """Gera uma solução inicial aleatória usando utils."""
    return gerar_solucao_binaria(n)

def inicializar_populacao_abelhas(n_abelhas, n_itens):
    """Inicializa a população de abelhas com soluções aleatórias."""
    return [gerar_solucao_aleatoria(n_itens) for _ in range(n_abelhas)]

def avaliar_populacao(abelhas, pesos, valores, capacidade):
    """Avalia toda a população de abelhas e retorna lista com avaliações."""
    avaliacoes = []
    for abelha in abelhas:
        solucao = abelha
        valor, peso = avaliar_solucao(solucao, pesos, valores, capacidade)
        avaliacoes.append((solucao, valor, peso))
    return avaliacoes

def selecionar_melhores_abelhas(avaliacoes, n_melhores):
    """Seleciona as n melhores abelhas com base na avaliação."""
    avaliacoes_ordenadas = sorted(avaliacoes, key=lambda x: x[1], reverse=True)
    return avaliacoes_ordenadas[:n_melhores]

def explorar_vizinhanca(solucao, n_vizinhos, pesos, valores, capacidade):
    """Explora a vizinhança de uma solução e retorna a melhor encontrada."""
    vizinhos = [gerar_vizinho(solucao) for _ in range(n_vizinhos)]
    vizinhos.append(solucao)  # Inclui a solução atual

    vizinhos_avaliados = []
    for vizinho in vizinhos:
        valor, peso = avaliar_solucao(vizinho, pesos, valores, capacidade)
        vizinhos_avaliados.append((vizinho, valor, peso))

    return max(vizinhos_avaliados, key=lambda x: x[1])

def executar_busca_local(melhores_abelhas, n_vizinhos, pesos, valores, capacidade):
    """Executa busca local para cada uma das melhores abelhas."""
    novas_solucoes = []
    for solucao, _, _ in melhores_abelhas:
        melhor_vizinho = explorar_vizinhanca(solucao, n_vizinhos, pesos, valores, capacidade)
        novas_solucoes.append(melhor_vizinho)
    return novas_solucoes

def encontrar_melhor_solucao_global(todas_solucoes):
    """Encontra a melhor solução global dentre todas as soluções encontradas."""
    return max(todas_solucoes, key=lambda x: x[1])

def bee_algorithm(pesos, valores, capacidade, n_abelhas=30, n_melhores=10, n_vizinhos=2, n_iter=50):
    """
    Implementa o Algoritmo das Abelhas para o Problema da Mochila 0/1.

    Args:
        pesos: Lista com os pesos dos itens
        valores: Lista com os valores dos itens
        capacidade: Capacidade máxima da mochila
        n_abelhas: Número de abelhas na população
        n_melhores: Número de melhores abelhas selecionadas
        n_vizinhos: Número de vizinhos explorados por cada abelha
        n_iter: Número de iterações

    Returns:
        Tupla contendo (solução, valor, peso)
    """
    n_itens = len(pesos)
    todas_solucoes = []

    for iteracao in range(n_iter):
        # Fase 1: Inicializar população de abelhas
        populacao_abelhas = inicializar_populacao_abelhas(n_abelhas, n_itens)

        # Fase 2: Avaliar população
        avaliacoes = avaliar_populacao(populacao_abelhas, pesos, valores, capacidade)

        # Fase 3: Selecionar melhores abelhas
        melhores_abelhas = selecionar_melhores_abelhas(avaliacoes, n_melhores)

        # Fase 4: Executar busca local nas melhores soluções
        novas_solucoes = executar_busca_local(melhores_abelhas, n_vizinhos, pesos, valores, capacidade)

        # Fase 5: Armazenar soluções encontradas
        todas_solucoes.extend(novas_solucoes)

    # Fase 6: Encontrar melhor solução global
    melhor_global = encontrar_melhor_solucao_global(todas_solucoes)
    return melhor_global[0], melhor_global[1], melhor_global[2]

def gerar_instancia_aleatoria_abelha(num_itens, max_peso=10, max_valor=50):
    """Gera uma instância aleatória do Problema da Mochila usando utils."""
    return gerar_instancia_aleatoria(num_itens, max_peso, max_valor)

def criar_resultado_teste(algoritmo_nome, n_itens, capacidade, valor, peso, tempo_execucao, pesos, valores, solucao):
    """Cria um dicionário com os resultados de um teste."""
    return {
        "algoritmo": algoritmo_nome,
        "n_itens": n_itens,
        "capacidade": capacidade,
        "valor_total": valor,
        "peso_total": peso,
        "tempo_execucao": round(tempo_execucao, 5),
        "pesos": pesos,
        "valores": valores,
        "melhor_solucao": solucao
    }

def executar_teste_para_instancia(n_itens):
    """Executa um teste completo para uma instância com n_itens."""
    pesos, valores, capacidade = gerar_instancia_aleatoria_abelha(n_itens)

    inicio = time.time()
    solucao, valor, peso = bee_algorithm(pesos, valores, capacidade)
    fim = time.time()

    tempo_execucao = fim - inicio

    return criar_resultado_teste(
        "Bee Algorithm", n_itens, capacidade, valor, peso,
        tempo_execucao, pesos, valores, solucao
    )

def main():
    """Função principal que executa os testes para diferentes tamanhos de instância."""
    tamanhos_instancia = [5, 1000, 10000]
    resultados_testes = []

    for n_itens in tamanhos_instancia:
        resultado = executar_teste_para_instancia(n_itens)
        resultados_testes.append(resultado)

    return pd.DataFrame(resultados_testes)