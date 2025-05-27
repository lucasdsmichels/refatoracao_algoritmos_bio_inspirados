import pytest
import random
from unittest.mock import patch, MagicMock
from algColonFormigas_ref import (
    inicializar_feromonios,
    calcular_atratividade,
    calcular_probabilidade,
    construir_solucao_formiga,
    evaporar_feromonios,
    depositar_feromonios,
    atualizar_feromonios,
    aco_knapsack,
    encontrar_melhor_solucao_iteracao,
    atualizar_melhor_global
)


class TestACO:
    """Classe de testes para o Algoritmo de Colônia de Formigas"""

    def setup_method(self):
        """Configuração executada antes de cada teste"""
        random.seed(42)  # Para resultados reproduzíveis
        self.pesos = [2, 1, 3, 2]
        self.valores = [12, 10, 20, 15]
        self.capacidade = 5
        self.n_itens = len(self.pesos)
    
    def test_inicializar_feromonios(self):
        """Testa a inicialização das trilhas de feromônio"""
        feromonios = inicializar_feromonios(self.n_itens)
        
        assert len(feromonios) == self.n_itens
        assert all(f == 1.0 for f in feromonios)
    
    def test_calcular_atratividade(self):
        """Testa o cálculo de atratividade"""
        # Teste normal
        atratividade = calcular_atratividade(10, 2)
        assert atratividade == 5.0
        
        # Teste com peso zero
        atratividade = calcular_atratividade(10, 0)
        assert atratividade == 0
        
        # Teste com valores negativos
        atratividade = calcular_atratividade(-10, 2)
        assert atratividade == -5.0
    
    def test_calcular_probabilidade(self):
        """Testa o cálculo de probabilidade"""
        # Teste com valores normais
        prob = calcular_probabilidade(1.0, 2.0, 1.0, 1.0)
        assert 0 <= prob <= 1
        assert prob == 2.0 / 3.0  # (1^1 * 2^1) / (1 + 1^1 * 2^1)
        
        # Teste com alfa e beta diferentes
        prob = calcular_probabilidade(2.0, 3.0, 2.0, 1.0)
        assert 0 <= prob <= 1
        assert prob == 12.0 / 13.0  # (2^2 * 3^1) / (1 + 2^2 * 3^1)
    
    def test_construir_solucao_formiga(self):
        """Testa a construção de solução por uma formiga"""
        feromonios = [1.0] * self.n_itens
        
        # Executa múltiplas vezes para testar a natureza estocástica
        solucoes = []
        for _ in range(10):
            solucao = construir_solucao_formiga(
                self.pesos, self.valores, self.capacidade, 
                feromonios, alfa=1.0, beta=2.0
            )
            solucoes.append(solucao)
            
            # Verifica se é uma solução válida
            assert len(solucao) == self.n_itens
            assert all(item in [0, 1] for item in solucao)
            
            # Verifica se respeita a capacidade
            peso_total = sum(p * s for p, s in zip(self.pesos, solucao))
            assert peso_total <= self.capacidade
    
    def test_evaporar_feromonios(self):
        """Testa a evaporação dos feromônios"""
        feromonios = [2.0, 3.0, 4.0, 5.0]
        rho = 0.1
        
        evaporar_feromonios(feromonios, rho)
        
        assert feromonios == [1.8, 2.7, 3.6, 4.5]
    
    def test_depositar_feromonios(self):
        """Testa o depósito de feromônios"""
        feromonios = [1.0, 1.0, 1.0, 1.0]
        melhor_solucao = [1, 0, 1, 0]
        melhor_peso = 5
        Q = 100
        
        depositar_feromonios(feromonios, melhor_solucao, melhor_peso, Q)
        
        deposito = Q / (1 + melhor_peso)
        assert feromonios[0] == 1.0 + deposito
        assert feromonios[1] == 1.0
        assert feromonios[2] == 1.0 + deposito
        assert feromonios[3] == 1.0
    
    def test_atualizar_feromonios(self):
        """Testa a atualização completa dos feromônios"""
        feromonios = [2.0, 2.0, 2.0, 2.0]
        melhor_solucao = [1, 0, 1, 0]
        melhor_peso = 5
        rho = 0.1
        Q = 100
        
        atualizar_feromonios(feromonios, melhor_solucao, melhor_peso, rho, Q)
        
        # Verifica evaporação e depósito
        evaporado = 2.0 * (1 - rho)
        deposito = Q / (1 + melhor_peso)
        
        assert feromonios[0] == evaporado + deposito
        assert feromonios[1] == evaporado
        assert feromonios[2] == evaporado + deposito
        assert feromonios[3] == evaporado
    
    def test_atualizar_melhor_global(self):
        """Testa a atualização da melhor solução global"""
        # Teste quando a nova solução é melhor
        melhor_solucao = [1, 0, 0, 0]
        melhor_valor = 10
        melhor_peso = 2
        
        nova_solucao = [0, 1, 0, 1]
        novo_valor = 25
        novo_peso = 3
        
        result = atualizar_melhor_global(
            nova_solucao, novo_valor, novo_peso,
            melhor_solucao, melhor_valor, melhor_peso
        )
        
        assert result[0] == nova_solucao
        assert result[1] == novo_valor
        assert result[2] == novo_peso
        
        # Teste quando a nova solução é pior
        nova_solucao = [0, 0, 1, 0]
        novo_valor = 5
        novo_peso = 3
        
        result = atualizar_melhor_global(
            nova_solucao, novo_valor, novo_peso,
            melhor_solucao, melhor_valor, melhor_peso
        )
        
        assert result[0] == melhor_solucao
        assert result[1] == melhor_valor
        assert result[2] == melhor_peso
    
    def test_encontrar_melhor_solucao_iteracao(self):
        """Testa a busca da melhor solução em uma iteração"""
        feromonios = [1.0] * self.n_itens
        n_formigas = 5
        
        melhor_solucao, melhor_valor, melhor_peso = encontrar_melhor_solucao_iteracao(
            self.pesos, self.valores, self.capacidade,
            feromonios, n_formigas, alfa=1.0, beta=2.0,
            melhor_valor_atual=0
        )
        
        # Verifica se retornou uma solução válida
        if melhor_solucao is not None:
            assert len(melhor_solucao) == self.n_itens
            assert all(item in [0, 1] for item in melhor_solucao)
            assert melhor_valor >= 0
            assert melhor_peso >= 0
    
    def test_aco_knapsack_pequena_instancia(self):
        """Testa o algoritmo completo com uma instância pequena"""
        solucao, valor, peso = aco_knapsack(
            self.pesos, self.valores, self.capacidade,
            n_formigas=10, n_iteracoes=5
        )
        
        # Verifica se retornou uma solução válida
        assert len(solucao) == self.n_itens
        assert all(item in [0, 1] for item in solucao)
        assert peso <= self.capacidade
        assert valor >= 0
        
        # Verifica se o valor e peso estão corretos
        valor_calculado = sum(v * s for v, s in zip(self.valores, solucao))
        peso_calculado = sum(p * s for p, s in zip(self.pesos, solucao))
        assert valor == valor_calculado
        assert peso == peso_calculado
    
    def test_aco_knapsack_sem_itens(self):
        """Testa o algoritmo com lista vazia de itens"""
        pesos = []
        valores = []
        capacidade = 10
        
        solucao, valor, peso = aco_knapsack(
            pesos, valores, capacidade,
            n_formigas=5, n_iteracoes=2
        )
        
        assert solucao is None or solucao == []
        assert valor == 0
        assert peso == 0
    
    def test_aco_knapsack_capacidade_zero(self):
        """Testa o algoritmo com capacidade zero"""
        solucao, valor, peso = aco_knapsack(
            self.pesos, self.valores, 0,
            n_formigas=5, n_iteracoes=2
        )
        
        assert solucao is None
        assert valor == 0
        assert peso == 0
    
    def test_aco_knapsack_parametros_diferentes(self):
        """Testa o algoritmo com diferentes configurações de parâmetros"""
        # Teste com alfa alto (mais importância ao feromônio)
        solucao1, _, _ = aco_knapsack(
            self.pesos, self.valores, self.capacidade,
            n_formigas=10, n_iteracoes=5, alfa=5.0, beta=1.0
        )
        
        # Teste com beta alto (mais importância à heurística)
        solucao2, _, _ = aco_knapsack(
            self.pesos, self.valores, self.capacidade,
            n_formigas=10, n_iteracoes=5, alfa=1.0, beta=5.0
        )
        
        # Ambas devem ser soluções válidas
        assert len(solucao1) == self.n_itens
        assert len(solucao2) == self.n_itens
    
    def test_aco_knapsack_grande_instancia(self):
        """Testa o algoritmo com uma instância maior"""
        n_itens = 50
        pesos = [random.randint(1, 10) for _ in range(n_itens)]
        valores = [random.randint(1, 50) for _ in range(n_itens)]
        capacidade = sum(pesos) // 3
        
        solucao, valor, peso = aco_knapsack(
            pesos, valores, capacidade,
            n_formigas=20, n_iteracoes=10
        )
        
        assert len(solucao) == n_itens
        assert peso <= capacidade
        assert valor > 0  # Deve encontrar alguma solução válida
    
    @patch('algColonFormigas_ref.avaliar_solucao')
    def test_aco_knapsack_com_mock(self, mock_avaliar):
        """Testa o algoritmo usando mock para isolar o teste"""
        # Configura o mock para retornar valores fixos
        mock_avaliar.return_value = (100, 5)
        
        solucao, valor, peso = aco_knapsack(
            self.pesos, self.valores, self.capacidade,
            n_formigas=5, n_iteracoes=2
        )
        
        # Verifica se a função foi chamada
        assert mock_avaliar.called
        assert valor == 100
        assert peso == 5