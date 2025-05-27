import random
import time
import pandas as pd
from utils import avaliar_solucao, gerar_solucao_binaria, gerar_instancia_aleatoria

def inicializar_populacao_ninhos(n_ninhos, n_itens):
    """Inicializa a população de ninhos com soluções aleatórias."""
    return [gerar_solucao_binaria(n_itens) for _ in range(n_ninhos)]

def calcular_fitness_populacao(ninhos, pesos, valores, capacidade):
    """Calcula o fitness de toda a população de ninhos."""
    fitness_list = []
    for ninho in ninhos:
        valor, _ = avaliar_solucao(ninho, pesos, valores, capacidade)
        fitness_list.append(valor)
    return fitness_list

def encontrar_melhor_ninho(ninhos, fitness_list):
    """Encontra o melhor ninho baseado no fitness."""
    melhor_indice = fitness_list.index(max(fitness_list))
    return ninhos[melhor_indice]

def aplicar_levy_flight(solucao):
    """Aplica o voo de Lévy para gerar uma nova solução."""
    nova_solucao = solucao[:]
    for i in range(len(nova_solucao)):
        if random.random() < 0.5:
            nova_solucao[i] = 1 - nova_solucao[i]
    return nova_solucao

def gerar_novos_ninhos_levy(ninhos, fitness_list, pesos, valores, capacidade):
    """Gera novos ninhos usando voo de Lévy e atualiza os melhores."""
    ninhos_atualizados = ninhos[:]
    fitness_atualizado = fitness_list[:]
    
    for i in range(len(ninhos)):
        novo_ninho = aplicar_levy_flight(ninhos[i])
        novo_fitness, _ = avaliar_solucao(novo_ninho, pesos, valores, capacidade)
        
        if novo_fitness > fitness_list[i]:
            ninhos_atualizados[i] = novo_ninho
            fitness_atualizado[i] = novo_fitness
    
    return ninhos_atualizados, fitness_atualizado

def calcular_ninhos_abandonados(n_ninhos, pa):
    """Calcula o número de ninhos a serem abandonados."""
    return int(pa * n_ninhos)

def substituir_ninhos_abandonados(ninhos, fitness_list, n_abandonados, n_itens, pesos, valores, capacidade):
    """Substitui os ninhos abandonados por novos ninhos aleatórios."""
    ninhos_atualizados = ninhos[:]
    fitness_atualizado = fitness_list[:]
    
    for _ in range(n_abandonados):
        idx = random.randint(0, len(ninhos) - 1)
        novo_ninho = gerar_solucao_binaria(n_itens)
        novo_fitness, _ = avaliar_solucao(novo_ninho, pesos, valores, capacidade)
        
        ninhos_atualizados[idx] = novo_ninho
        fitness_atualizado[idx] = novo_fitness
    
    return ninhos_atualizados, fitness_atualizado

def executar_iteracao_cuckoo(ninhos, fitness_list, pesos, valores, capacidade, pa, n_itens):
    """Executa uma iteração completa do algoritmo Cuckoo Search."""
    # Fase 1: Gerar novos ninhos com voo de Lévy
    ninhos, fitness_list = gerar_novos_ninhos_levy(ninhos, fitness_list, pesos, valores, capacidade)
    
    # Fase 2: Abandonar ninhos com baixa qualidade
    n_abandonados = calcular_ninhos_abandonados(len(ninhos), pa)
    ninhos, fitness_list = substituir_ninhos_abandonados(
        ninhos, fitness_list, n_abandonados, n_itens, pesos, valores, capacidade
    )
    
    # Fase 3: Encontrar o melhor ninho atual
    melhor_ninho = encontrar_melhor_ninho(ninhos, fitness_list)
    
    return ninhos, fitness_list, melhor_ninho

def avaliar_melhor_solucao_final(melhor_ninho, pesos, valores, capacidade):
    """Avalia a melhor solução final encontrada."""
    return avaliar_solucao(melhor_ninho, pesos, valores, capacidade)

def cuckoo_search(pesos, valores, capacidade, n_ninhos=25, n_iteracoes=50, pa=0.25):
    """
    Implementa o algoritmo Cuckoo Search para o Problema da Mochila 0/1.
    
    Args:
        pesos: Lista com os pesos dos itens
        valores: Lista com os valores dos itens
        capacidade: Capacidade máxima da mochila
        n_ninhos: Número de ninhos (soluções) na população
        n_iteracoes: Número de iterações do algoritmo
        pa: Probabilidade de abandono (discovery rate of alien eggs)
    
    Returns:
        Tupla contendo (melhor_solucao, melhor_valor, melhor_peso)
    """
    n_itens = len(pesos)
    
    # Fase 1: Inicialização
    ninhos = inicializar_populacao_ninhos(n_ninhos, n_itens)
    fitness_list = calcular_fitness_populacao(ninhos, pesos, valores, capacidade)
    melhor_ninho = encontrar_melhor_ninho(ninhos, fitness_list)

    # Fase 2: Loop principal das iterações
    for iteracao in range(n_iteracoes):
        ninhos, fitness_list, melhor_ninho = executar_iteracao_cuckoo(
            ninhos, fitness_list, pesos, valores, capacidade, pa, n_itens
        )

    # Fase 3: Avaliação final
    melhor_valor, melhor_peso = avaliar_melhor_solucao_final(melhor_ninho, pesos, valores, capacidade)
    
    return melhor_ninho, melhor_valor, melhor_peso

def criar_resultado_teste_cuckoo(n_itens, capacidade, valor, peso, tempo_execucao, pesos, valores, solucao):
    """Cria um dicionário com os resultados de um teste Cuckoo Search."""
    return {
        "algoritmo": "Cuckoo Search",
        "n_itens": n_itens,
        "capacidade": capacidade,
        "valor_total": valor,
        "peso_total": peso,
        "tempo_execucao": round(tempo_execucao, 5),
        "pesos": pesos,
        "valores": valores,
        "melhor_solucao": solucao
    }

def executar_teste_cuckoo_para_instancia(n_itens):
    """Executa um teste completo do Cuckoo Search para uma instância com n_itens."""
    pesos, valores, capacidade = gerar_instancia_aleatoria(n_itens)
    
    inicio = time.time()
    solucao, valor, peso = cuckoo_search(pesos, valores, capacidade)
    fim = time.time()
    
    tempo_execucao = fim - inicio
    
    return criar_resultado_teste_cuckoo(
        n_itens, capacidade, valor, peso,
        tempo_execucao, pesos, valores, solucao
    )

def main():
    """Função principal que executa os testes Cuckoo Search para diferentes tamanhos de instância."""
    tamanhos_instancia = [5, 1000, 10000]
    resultados_testes = []
    
    for n_itens in tamanhos_instancia:
        resultado = executar_teste_cuckoo_para_instancia(n_itens)
        resultados_testes.append(resultado)

    return pd.DataFrame(resultados_testes)