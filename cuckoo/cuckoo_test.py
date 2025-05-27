import pytest
import random
from unittest.mock import patch, MagicMock
from algCuckoo_ref import (
    inicializar_populacao_ninhos,
    calcular_fitness_populacao,
    encontrar_melhor_ninho,
    aplicar_levy_flight,
    gerar_novos_ninhos_levy,
    calcular_ninhos_abandonados,
    substituir_ninhos_abandonados,
    executar_iteracao_cuckoo,
    avaliar_melhor_solucao_final,
    cuckoo_search
)


class TestCuckooSearch:
    """Classe de testes para o Algoritmo Cuckoo Search"""
    
    def setup_method(self):
        random.seed(42)
        self.pesos = [2, 1, 3, 2]
        self.valores = [12, 10, 20, 15]
        self.capacidade = 5
        self.n_itens = len(self.pesos)
    
    @patch('algCuckoo_ref.gerar_solucao_binaria')
    def test_inicializar_populacao_ninhos(self, mock_gerar):
        n_ninhos = 3
        mock_gerar.side_effect = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
        ninhos = inicializar_populacao_ninhos(n_ninhos, self.n_itens)
        assert len(ninhos) == n_ninhos
        assert mock_gerar.call_count == n_ninhos
        assert ninhos[0] == [1, 0, 0, 0]
        assert ninhos[1] == [0, 1, 0, 0]
        assert ninhos[2] == [0, 0, 1, 0]
    
    @patch('algCuckoo_ref.avaliar_solucao')
    def test_calcular_fitness_populacao(self, mock_avaliar):
        ninhos = [[1, 0, 0, 0], [0, 1, 0, 1], [1, 1, 0, 0]]
        mock_avaliar.side_effect = [(12, 2), (25, 3), (22, 3)]
        fitness_list = calcular_fitness_populacao(ninhos, self.pesos, self.valores, self.capacidade)
        assert len(fitness_list) == 3
        assert fitness_list == [12, 25, 22]
        assert mock_avaliar.call_count == 3
    
    def test_encontrar_melhor_ninho(self):
        ninhos = [[1, 0, 0, 0], [0, 1, 0, 1], [1, 1, 0, 0]]
        fitness_list = [12, 25, 22]
        melhor = encontrar_melhor_ninho(ninhos, fitness_list)
        assert melhor == [0, 1, 0, 1]
    
    def test_aplicar_levy_flight(self):
        solucao = [1, 0, 1, 0]
        resultados_diferentes = set()
        for _ in range(20):
            nova_solucao = aplicar_levy_flight(solucao)
            assert len(nova_solucao) == len(solucao)
            assert all(item in [0, 1] for item in nova_solucao)
            resultados_diferentes.add(tuple(nova_solucao))
        assert len(resultados_diferentes) > 1
    
    @patch('algCuckoo_ref.avaliar_solucao')
    def test_gerar_novos_ninhos_levy(self, mock_avaliar):
        ninhos = [[1, 0, 0, 0], [0, 1, 0, 0]]
        fitness_list = [12, 10]
        mock_avaliar.side_effect = [(15, 2), (20, 3)]
        with patch('algCuckoo_ref.aplicar_levy_flight') as mock_levy:
            mock_levy.side_effect = [[0, 0, 0, 1], [1, 0, 1, 0]]
            novos_ninhos, novo_fitness = gerar_novos_ninhos_levy(
                ninhos, fitness_list, self.pesos, self.valores, self.capacidade
            )
            assert novos_ninhos[0] == [0, 0, 0, 1]
            assert novos_ninhos[1] == [1, 0, 1, 0]
            assert novo_fitness == [15, 20]
    
    def test_calcular_ninhos_abandonados(self):
        assert calcular_ninhos_abandonados(10, 0.25) == 2
        assert calcular_ninhos_abandonados(20, 0.3) == 6
        assert calcular_ninhos_abandonados(5, 0.5) == 2

    @patch('algCuckoo_ref.gerar_solucao_binaria')
    @patch('algCuckoo_ref.avaliar_solucao')
    def test_substituir_ninhos_abandonados(self, mock_avaliar, mock_gerar):
        ninhos = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
        fitness_list = [12, 10, 20]
        n_abandonados = 2
        mock_gerar.side_effect = [[1, 1, 0, 0], [0, 0, 1, 1]]
        mock_avaliar.side_effect = [(22, 3), (35, 5)]
        with patch('random.randint') as mock_random:
            mock_random.side_effect = [0, 2]  # Índices dos ninhos a substituir
            novos_ninhos, novo_fitness = substituir_ninhos_abandonados(
                ninhos, fitness_list, n_abandonados, self.n_itens, self.pesos, self.valores, self.capacidade
            )
            # Verifica se os ninhos substituídos são os esperados
            assert novos_ninhos[0] == [1, 1, 0, 0]
            assert novos_ninhos[2] == [0, 0, 1, 1]
            # Verifica se os fitness foram atualizados corretamente
            assert novo_fitness[0] == 22
            assert novo_fitness[2] == 35
            # O ninhos e fitness no índice 1 permanecem iguais
            assert novos_ninhos[1] == ninhos[1]
            assert novo_fitness[1] == fitness_list[1]


    @patch('algCuckoo_ref.gerar_solucao_binaria')
    @patch('algCuckoo_ref.avaliar_solucao')
    @patch('algCuckoo_ref.aplicar_levy_flight')
    def test_executar_iteracao_cuckoo(self, mock_levy, mock_avaliar, mock_gerar):
        ninhos = [[1, 0, 0, 0], [0, 1, 0, 1]]
        fitness_list = [12, 15]
        mock_levy.side_effect = [[1, 1, 0, 0], [0, 0, 0, 1]]
        mock_avaliar.side_effect = [(20, 3), (18, 2), (10, 1), (30, 4)]
        mock_gerar.side_effect = [[0, 0, 1, 1]]
        pa = 0.5
        n_itens = 4

        with patch('random.randint') as mock_rand:
            mock_rand.side_effect = [0]  # Um ninho será abandonado

            ninhos_atualizados, fitness_atualizado, melhor_ninho = executar_iteracao_cuckoo(
                ninhos, fitness_list, self.pesos, self.valores, self.capacidade, pa, n_itens
            )

            # Verifica se o ninho foi atualizado pelo voo de Lévy
            assert ninhos_atualizados[0] == [0, 0, 1, 1]
            # Verifica se o fitness foi atualizado
            assert fitness_atualizado[0] == 10
            # Verifica se o melhor ninho está correto (fitness 30)
            assert melhor_ninho == ninhos_atualizados[1]

    @patch('algCuckoo_ref.avaliar_solucao')
    def test_averiar_melhor_solucao_final(self, mock_avaliar):
        melhor_ninho = [1, 0, 1, 0]
        mock_avaliar.return_value = (30, 5)
        valor, peso = avaliar_melhor_solucao_final(melhor_ninho, self.pesos, self.valores, self.capacidade)
        assert valor == 30
        assert peso == 5
        mock_avaliar.assert_called_once_with(melhor_ninho, self.pesos, self.valores, self.capacidade)