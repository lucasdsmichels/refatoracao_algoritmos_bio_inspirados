# Refatoração dos Algoritmos de Otimização

## Visão Geral

Este documento descreve as refatorações aplicadas aos algoritmos de otimização para o Problema da Mochila 0/1. As refatorações focaram em melhorar a legibilidade, manutenibilidade e organização do código.

## Princípios de Refatoração Aplicados

### 1. **Modularização e Responsabilidade Única**
- **Antes**: Funções grandes com múltiplas responsabilidades
- **Depois**: Funções menores, cada uma com uma responsabilidade específica
- **Por quê**: Facilita testes, depuração e reutilização de código

### 2. **Reutilização através de Módulo Utils**
- **Antes**: Código duplicado em cada arquivo
- **Depois**: Importação de funções comuns do módulo `utils`
- **Por quê**: Elimina duplicação e centraliza manutenção

### 3. **Nomenclatura Descritiva**
- **Antes**: Nomes genéricos ou abreviados
- **Depois**: Nomes que descrevem claramente o propósito
- **Por quê**: Melhora a compreensão do código sem necessidade de comentários

### 4. **Documentação com Docstrings**
- **Antes**: Sem documentação ou comentários mínimos
- **Depois**: Docstrings explicando parâmetros e retornos
- **Por quê**: Facilita o entendimento e uso das funções

## Refatorações por Algoritmo

### 1. Algoritmo de Colônia de Formigas (ACO)

#### Principais Mudanças:
- **Separação de Fases**: Dividido em inicialização, construção de soluções, e atualização de feromônios
- **Funções Especializadas**:
  ```python
  # Antes: Tudo em uma função
  # Depois:
  - inicializar_feromonios()
  - calcular_atratividade()
  - calcular_probabilidade()
  - construir_solucao_formiga()
  - evaporar_feromonios()
  - depositar_feromonios()
  ```
- **Organização Lógica**: Loop principal claramente estruturado com fases documentadas

### 2. Bee Algorithm

#### Principais Mudanças:
- **Decomposição Funcional**:
  ```python
  # Antes: Lógica entrelaçada
  # Depois:
  - inicializar_populacao_abelhas()
  - avaliar_populacao()
  - selecionar_melhores_abelhas()
  - explorar_vizinhanca()
  - executar_busca_local()
  ```
- **Uso de Utils**: Importação de `gerar_solucao_binaria`, `gerar_vizinho`, `avaliar_solucao`
- **Clareza nas Fases**: Cada fase do algoritmo claramente identificada com comentários

### 3. Cuckoo Search

#### Principais Mudanças:
- **Modularização do Processo**:
  ```python
  # Antes: Função monolítica
  # Depois:
  - inicializar_populacao_ninhos()
  - calcular_fitness_populacao()
  - aplicar_levy_flight()
  - gerar_novos_ninhos_levy()
  - substituir_ninhos_abandonados()
  ```
- **Iteração Estruturada**: Função `executar_iteracao_cuckoo()` encapsula uma iteração completa
- **Separação de Cálculos**: Cálculo de ninhos abandonados isolado em função própria

### 4. Algoritmo Genético

#### Principais Mudanças:
- **Operadores Genéticos Isolados**:
  ```python
  # Antes: Operações inline
  # Depois:
  - criar_populacao_inicial()
  - selecionar_pais()
  - fazer_crossover()
  - aplicar_mutacao()
  - criar_nova_geracao()
  ```
- **Melhor Organização**: Separação clara entre inicialização, evolução e avaliação
- **Função de Avaliação Melhorada**: `avaliar_individuo()` com lógica de penalização mais clara

### 5. Particle Swarm Optimization (PSO)

#### Principais Mudanças:
- **Eliminação de Classes**: Mudança de orientação a objetos para funcional
  ```python
  # Antes: class Particula
  # Depois: Funções puras e dicionários para padronizar todos algoritmos
  ```
- **Funções Atômicas**:
  ```python
  - binarizar()
  - inicializar_particula()
  - calcular_nova_velocidade()
  - atualizar_velocidade()
  - atualizar_posicao()
  ```
- **Estrutura de Dados Simplificada**: Uso de dicionários em vez de classes

## Melhorias Comuns a Todos os Algoritmos

### 1. **Estrutura da Função Main**
- Criação de funções auxiliares para execução de testes
- Separação entre lógica do algoritmo e código de teste
- Padronização na criação de resultados

### 2. **Tratamento de Dados**
- Uso consistente de `gerar_instancia_aleatoria()` do módulo utils
- Padronização na estrutura de retorno dos resultados

### 3. **Legibilidade**
- Adição de espaços em branco estratégicos
- Agrupamento lógico de operações relacionadas
- Comentários descrevendo fases do algoritmo

## Benefícios da Refatoração

1. **Manutenibilidade**: Código mais fácil de modificar e estender
2. **Testabilidade**: Funções menores são mais fáceis de testar isoladamente
3. **Reutilização**: Código comum centralizado no módulo utils
4. **Compreensão**: Nomes descritivos e estrutura clara facilitam entendimento
5. **Depuração**: Funções específicas facilitam identificação de problemas
6. **Documentação**: Docstrings fornecem documentação integrada ao código

## Exemplo de Melhoria

### Antes (algColonFormigas.py):
```python
for i in range(n):
    if peso_total + pesos[i] <= capacidade:
        atratividade = (valores[i] / pesos[i]) if pesos[i] > 0 else 0
        prob = (feromonio[i] ** alfa) * (atratividade ** beta)
        if random.random() < prob / (1 + prob):
            solucao[i] = 1
            peso_total += pesos[i]
```

### Depois (algColonFormigas_ref.py):
```python
def calcular_atratividade(valor, peso):
    """Calcula a atratividade de um item (razão valor/peso)."""
    return (valor / peso) if peso > 0 else 0

def calcular_probabilidade(feromonio, atratividade, alfa, beta):
    """Calcula a probabilidade de seleção de um item."""
    prob = (feromonio ** alfa) * (atratividade ** beta)
    return prob / (1 + prob)

```

## Conclusão

As refatorações aplicadas transformaram código funcional mas monolítico em código modular, bem documentado e fácil de manter. A separação de responsabilidades e a criação de funções específicas não apenas melhoram a qualidade do código, mas também facilitam futuras modificações e extensões dos algoritmos.