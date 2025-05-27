import random
import time
import pandas as pd
from utils import avaliar_solucao, gerar_instancia_aleatoria

def inicializar_feromonios(n_itens):
    """Inicializa as trilhas de feromônio com valores iniciais."""
    return [1.0] * n_itens

def calcular_atratividade(valor, peso):
    """Calcula a atratividade de um item (razão valor/peso)."""
    return (valor / peso) if peso > 0 else 0

def calcular_probabilidade(feromonio, atratividade, alfa, beta):
    """Calcula a probabilidade de seleção de um item."""
    prob = (feromonio ** alfa) * (atratividade ** beta)
    return prob / (1 + prob)

def construir_solucao_formiga(pesos, valores, capacidade, feromonios, alfa, beta):
    """Constrói uma solução para uma formiga seguindo as probabilidades."""
    n = len(pesos)
    solucao = [0] * n
    peso_total = 0

    for i in range(n):
        if peso_total + pesos[i] <= capacidade:
            atratividade = calcular_atratividade(valores[i], pesos[i])
            probabilidade = calcular_probabilidade(feromonios[i], atratividade, alfa, beta)

            if random.random() < probabilidade:
                solucao[i] = 1
                peso_total += pesos[i]

    return solucao

def encontrar_melhor_solucao_iteracao(pesos, valores, capacidade, feromonios, n_formigas, alfa, beta, melhor_valor_atual):
    """Encontra a melhor solução em uma iteração usando todas as formigas."""
    melhor_solucao_iteracao = None
    melhor_valor_iteracao = melhor_valor_atual
    melhor_peso_iteracao = 0

    for _ in range(n_formigas):
        solucao = construir_solucao_formiga(pesos, valores, capacidade, feromonios, alfa, beta)
        valor, peso = avaliar_solucao(solucao, pesos, valores, capacidade)

        if valor > melhor_valor_iteracao:
            melhor_solucao_iteracao = solucao
            melhor_valor_iteracao = valor
            melhor_peso_iteracao = peso

    return melhor_solucao_iteracao, melhor_valor_iteracao, melhor_peso_iteracao

def evaporar_feromonios(feromonios, rho):
    """Aplica a evaporação dos feromônios."""
    for i in range(len(feromonios)):
        feromonios[i] *= (1 - rho)

def depositar_feromonios(feromonios, melhor_solucao, melhor_peso, Q):
    """Deposita feromônios na melhor solução encontrada."""
    if melhor_solucao:
        deposito = Q / (1 + melhor_peso)
        for i in range(len(feromonios)):
            if melhor_solucao[i] == 1:
                feromonios[i] += deposito

def atualizar_feromonios(feromonios, melhor_solucao, melhor_peso, rho, Q):
    """Atualiza os feromônios: evaporação + depósito."""
    evaporar_feromonios(feromonios, rho)
    depositar_feromonios(feromonios, melhor_solucao, melhor_peso, Q)

def atualizar_melhor_global(solucao_atual, valor_atual, peso_atual, melhor_solucao, melhor_valor, melhor_peso):
    """Atualiza a melhor solução global se necessário."""
    if solucao_atual and valor_atual > melhor_valor:
        return solucao_atual[:], valor_atual, peso_atual
    return melhor_solucao, melhor_valor, melhor_peso

def executar_iteracao_aco(pesos, valores, capacidade, feromonios, n_formigas, alfa, beta, melhor_solucao, melhor_valor, melhor_peso, rho, Q):
    """Executa uma iteração completa do algoritmo ACO."""
    # Construir soluções com as formigas
    solucao_iteracao, valor_iteracao, peso_iteracao = encontrar_melhor_solucao_iteracao(
        pesos, valores, capacidade, feromonios, n_formigas, alfa, beta, melhor_valor
    )

    # Atualizar melhor solução global
    melhor_solucao, melhor_valor, melhor_peso = atualizar_melhor_global(
        solucao_iteracao, valor_iteracao, peso_iteracao,
        melhor_solucao, melhor_valor, melhor_peso
    )

    # Atualizar feromônios
    atualizar_feromonios(feromonios, melhor_solucao, melhor_peso, rho, Q)

    return melhor_solucao, melhor_valor, melhor_peso

def aco_knapsack(pesos, valores, capacidade, n_formigas=50, n_iteracoes=50, alfa=1.0, beta=2.0, rho=0.1, Q=100):
    """
    Implementa o Algoritmo de Colônia de Formigas para o Problema da Mochila 0/1.

    Args:
        pesos: Lista com os pesos dos itens
        valores: Lista com os valores dos itens
        capacidade: Capacidade máxima da mochila
        n_formigas: Número de formigas na colônia
        n_iteracoes: Número de iterações do algoritmo
        alfa: Parâmetro de importância do feromônio
        beta: Parâmetro de importância da heurística
        rho: Taxa de evaporação do feromônio
        Q: Constante para depósito de feromônio

    Returns:
        Tupla contendo (melhor_solucao, melhor_valor, melhor_peso)
    """
    n_itens = len(pesos)

    # Fase 1: Inicialização
    feromonios = inicializar_feromonios(n_itens)
    melhor_solucao = None
    melhor_valor = 0
    melhor_peso = 0

    # Fase 2: Loop principal das iterações
    for iteracao in range(n_iteracoes):
        melhor_solucao, melhor_valor, melhor_peso = executar_iteracao_aco(
            pesos, valores, capacidade, feromonios, n_formigas, alfa, beta,
            melhor_solucao, melhor_valor, melhor_peso, rho, Q
        )

    return melhor_solucao, melhor_valor, melhor_peso

def criar_resultado_teste_aco(n_itens, capacidade, valor, peso, tempo_execucao, pesos, valores, solucao):
    """Cria um dicionário com os resultados de um teste ACO."""
    return {
        "algoritmo": "Algoritmo ACO",
        "n_itens": n_itens,
        "capacidade": capacidade,
        "valor_total": valor,
        "peso_total": peso,
        "tempo_execucao": round(tempo_execucao, 5),
        "pesos": pesos,
        "valores": valores,
        "melhor_solucao": solucao
    }

def executar_teste_aco_para_instancia(n_itens):
    """Executa um teste completo do ACO para uma instância com n_itens."""
    pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens)

    inicio = time.time()
    solucao, valor, peso = aco_knapsack(pesos, valores, capacidade)
    fim = time.time()

    tempo_execucao = fim - inicio

    return criar_resultado_teste_aco(
        n_itens, capacidade, valor, peso,
        tempo_execucao, pesos, valores, solucao
    )

def main():
    """Função principal que executa os testes ACO para diferentes tamanhos de instância."""
    tamanhos_instancia = [5, 1000, 10000]
    resultados_testes = []

    for n_itens in tamanhos_instancia:
        resultado = executar_teste_aco_para_instancia(n_itens)
        resultados_testes.append(resultado)

    return pd.DataFrame(resultados_testes)