# Algoritmos de Otimização para o Problema da Mochila 0/1

## Alunos
- Luis Felipe Mondini
- Gustavo Larsen
- João Antonio David
- Lucas Michels
- Thiago de Freitas Saraiva

## 📋 Sobre o Projeto

Este repositório contém implementações de cinco algoritmos bio-inspirados para resolver o Problema da Mochila 0/1, com versões originais e refatoradas de cada algoritmo.

### Algoritmos Implementados
- 🐜 **ACO** (Ant Colony Optimization)
- 🐝 **Bee Algorithm**
- 🐦 **Cuckoo Search**
- 🧬 **Algoritmo Genético**
- 🌊 **PSO** (Particle Swarm Optimization)

## 🚀 Quick Start

### Instalação
```bash
# Clone o repositório
git clone [url-do-repositorio]

# Instale as dependências
pip install -r requirements.txt
```

### Execução Rápida
```python
# Para executar qualquer algoritmo refatorado
python algGeneticos_ref.py

# Para executar a versão original
python algGeneticos.py

# Para verificar a comparação do tempo de execução entre o código refatorado e o antigo
python main.py
```

## 💻 Como Usar

### Uso Básico
Cada algoritmo pode ser executado independentemente e testará automaticamente três tamanhos de instância: 5, 1000 e 10000 itens.

```python
# Exemplo de uso direto
from algGeneticos_ref import algoritmo_genetico
from utils import gerar_instancia_aleatoria

# Gerar uma instância
pesos, valores, capacidade = gerar_instancia_aleatoria(100)

# Resolver com Algoritmo Genético
solucao, valor = algoritmo_genetico(pesos, valores, capacidade)
print(f"Valor encontrado: {valor}")
```

### Customizando Parâmetros

#### ACO (Ant Colony Optimization)
```python
from algColonFormigas_ref import aco_knapsack

solucao, valor, peso = aco_knapsack(
    pesos, valores, capacidade,
    n_formigas=50,      # Número de formigas
    n_iteracoes=100,    # Número de iterações
    alfa=1.0,           # Importância do feromônio
    beta=2.0,           # Importância da heurística
    rho=0.1,            # Taxa de evaporação
    Q=100               # Constante de depósito
)
```

#### Bee Algorithm
```python
from beeAlgorithm_ref import bee_algorithm

solucao, valor, peso = bee_algorithm(
    pesos, valores, capacidade,
    n_abelhas=30,       # Tamanho da população
    n_melhores=10,      # Abelhas elite
    n_vizinhos=2,       # Vizinhos por busca
    n_iter=50           # Iterações
)
```

#### Parâmetros dos Outros Algoritmos
- **Cuckoo Search**: `n_ninhos`, `n_iteracoes`, `pa` (probabilidade de abandono)
- **Algoritmo Genético**: `tam_populacao`, `taxa_mutacao`, `n_geracoes`
- **PSO**: `n_particulas`, `n_iteracoes`, `c1`, `c2`, `w`

## 📊 Formato de Saída

Todos os algoritmos retornam um DataFrame pandas com as seguintes colunas:
- `algoritmo`: Nome do algoritmo utilizado
- `n_itens`: Número de itens na instância
- `capacidade`: Capacidade da mochila
- `valor_total`: Valor da solução encontrada
- `peso_total`: Peso total da solução
- `tempo_execucao`: Tempo em segundos
- `pesos`: Lista de pesos dos itens
- `valores`: Lista de valores dos itens
- `melhor_solucao`: Vetor binário da solução

## 🔧 Módulo Utils

O módulo `utils.py` fornece funções reutilizáveis:

```python
from utils import (
    gerar_instancia_aleatoria,  # Gera problemas aleatórios
    avaliar_solucao,            # Avalia uma solução
    gerar_solucao_binaria,      # Gera solução inicial
    gerar_vizinho               # Gera vizinho de uma solução
)
```

## 📚 Documentação Adicional

Para informações detalhadas sobre:
- **Refatorações realizadas**: Ver [refatoracao.md](./refatoracao.md)
- **Processo completo e métricas**: Ver [processo.md](./processo.md)

---

---

### Slides

[Refatoração de algoritmos Bio-Inspirados.pdf](https://github.com/user-attachments/files/20466637/Refatoracao.de.algoritmos.Bio-Inspirados.pdf)


---
