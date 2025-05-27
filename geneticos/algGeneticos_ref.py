import random
import time
import pandas as pd
from utils import gerar_instancia_aleatoria, avaliar_solucao, gerar_solucao_binaria

def avaliar_individuo(individuo, pesos, valores, capacidade):
    """Avalia fitness de um indivíduo com penalização."""
    valor, peso_total = avaliar_solucao(individuo, pesos, valores, capacidade)
    if peso_total > capacidade:
        excesso = peso_total - capacidade
        return valor - excesso * 2  # Penalização
    return valor

def criar_populacao_inicial(tam_populacao, n_itens):
    """Cria população inicial aleatória."""
    return [gerar_solucao_binaria(n_itens) for _ in range(tam_populacao)]

def selecionar_pais(populacao, pesos, valores, capacidade, tamanho_torneio=3):
    """Seleciona dois pais por torneio."""
    def torneio():
        competidores = random.sample(populacao, tamanho_torneio)
        return max(competidores, key=lambda ind: avaliar_individuo(ind, pesos, valores, capacidade))

    return torneio(), torneio()

def fazer_crossover(pai1, pai2):
    """Realiza crossover de um ponto."""
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def aplicar_mutacao(individuo, taxa_mutacao):
    """Aplica mutação bit a bit."""
    individuo_mutado = individuo[:]
    for i in range(len(individuo_mutado)):
        if random.random() < taxa_mutacao:
            individuo_mutado[i] = 1 - individuo_mutado[i]
    return individuo_mutado

def criar_nova_geracao(populacao, pesos, valores, capacidade, taxa_mutacao):
    """Cria nova geração através de seleção, crossover e mutação."""
    nova_populacao = []
    tam_populacao = len(populacao)

    while len(nova_populacao) < tam_populacao:
        # Seleção
        pai1, pai2 = selecionar_pais(populacao, pesos, valores, capacidade)

        # Crossover
        filho1, filho2 = fazer_crossover(pai1, pai2)

        # Mutação
        filho1 = aplicar_mutacao(filho1, taxa_mutacao)
        filho2 = aplicar_mutacao(filho2, taxa_mutacao)

        nova_populacao.extend([filho1, filho2])

    return nova_populacao[:tam_populacao]

def encontrar_melhor_individuo(populacao, pesos, valores, capacidade):
    """Encontra o melhor indivíduo da população."""
    melhor = max(populacao, key=lambda ind: avaliar_individuo(ind, pesos, valores, capacidade))
    melhor_valor = avaliar_individuo(melhor, pesos, valores, capacidade)
    return melhor, melhor_valor

def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
    """Executa o algoritmo genético."""
    n_itens = len(pesos)

    # Inicialização
    populacao = criar_populacao_inicial(tam_populacao, n_itens)
    melhor_solucao, melhor_valor = encontrar_melhor_individuo(populacao, pesos, valores, capacidade)

    # Evolução
    for _ in range(n_geracoes):
        # Criar nova geração
        populacao = criar_nova_geracao(populacao, pesos, valores, capacidade, taxa_mutacao)

        # Atualizar melhor solução se necessário
        melhor_atual, valor_atual = encontrar_melhor_individuo(populacao, pesos, valores, capacidade)
        if valor_atual > melhor_valor:
            melhor_solucao = melhor_atual
            melhor_valor = valor_atual

    return melhor_solucao, melhor_valor

def executar_teste(n_itens):
    """Executa um teste com n_itens."""
    pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens)

    inicio = time.time()
    solucao, valor = algoritmo_genetico(pesos, valores, capacidade)
    fim = time.time()

    peso_total = sum(p * i for p, i in zip(pesos, solucao))

    return {
        "algoritmo": "Algoritmo Genético",
        "n_itens": n_itens,
        "capacidade": capacidade,
        "valor_total": valor,
        "peso_total": peso_total,
        "tempo_execucao": round(fim - inicio, 5),
        "pesos": pesos,
        "valores": valores,
        "melhor_solucao": solucao
    }

def main():
    testes = []
    tamanhos = [5, 1000, 10000]

    for n in tamanhos:
        teste = executar_teste(n)
        testes.append(teste)

    df = pd.DataFrame(testes)
    return df

if __name__ == "__main__":
    df = main()
    print("\nResumo dos resultados de todos os testes:")
    print(df)