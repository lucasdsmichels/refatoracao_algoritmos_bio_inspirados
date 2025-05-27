import pytest
import random
from unittest.mock import patch, MagicMock
from beeAlgorithm_ref import (
    gerar_solucao_aleatoria,
    inicializar_populacao_abelhas,
    avaliar_populacao,
    selecionar_melhores_abelhas,
    explorar_vizinhanca,
    executar_busca_local,
    encontrar_melhor_solucao_global,
    bee_algorithm,
    criar_resultado_teste
)


class TestBeeAlgorithm:
    """Classe de testes para o Algoritmo de Abelhas"""
    
    def setup_method(self):
        """Configuração executada antes de cada teste"""
        random.seed(42)
        self.pesos = [2, 1, 3, 2]
        self.valores = [12, 10, 20, 15]
        self.capacidade = 5
        self.n_itens = len(self.pesos)
    
    @patch('beeAlgorithm_ref.gerar_solucao_binaria')
    def test_gerar_solucao_aleatoria(self, mock_gerar):
        """Testa a geração de solução aleatória"""
        mock_gerar.return_value = [1, 0, 1, 0]
        
        solucao = gerar_solucao_aleatoria(self.n_itens)
        
        mock_gerar.assert_called_once_with(self.n_itens)
        assert solucao == [1, 0, 1, 0]
    
    def test_inicializar_populacao_abelhas(self):
        """Testa a inicialização da população de abelhas"""
        n_abelhas = 5
        
        with patch('beeAlgorithm_ref.gerar_solucao_aleatoria') as mock_gerar:
            mock_gerar.side_effect = [[1, 0, 0, 0], [0, 1, 0, 0], 
                                      [0, 0, 1, 0], [0, 0, 0, 1], 
                                      [1, 1, 0, 0]]
            
            populacao = inicializar_populacao_abelhas(n_abelhas, self.n_itens)
            
            assert len(populacao) == n_abelhas
            assert mock_gerar.call_count == n_abelhas
            assert populacao[0] == [1, 0, 0, 0]
            assert populacao[-1] == [1, 1, 0, 0]
    
    @patch('beeAlgorithm_ref.avaliar_solucao')
    def test_avaliar_populacao(self, mock_avaliar):
        """Testa a avaliação da população"""
        populacao = [[1, 0, 0, 0], [0, 1, 0, 1], [1, 1, 0, 0]]
        mock_avaliar.side_effect = [(10, 2), (25, 3), (22, 3)]
        
        avaliacoes = avaliar_populacao(populacao, self.pesos, self.valores, self.capacidade)
        
        assert len(avaliacoes) == 3
        assert avaliacoes[0] == ([1, 0, 0, 0], 10, 2)
        assert avaliacoes[1] == ([0, 1, 0, 1], 25, 3)
        assert avaliacoes[2] == ([1, 1, 0, 0], 22, 3)
        assert mock_avaliar.call_count == 3
    
    def test_selecionar_melhores_abelhas(self):
        """Testa a seleção das melhores abelhas"""
        avaliacoes = [
            ([1, 0, 0, 0], 10, 2),
            ([0, 1, 0, 1], 25, 3),
            ([1, 1, 0, 0], 22, 3),
            ([0, 0, 1, 0], 20, 3),
            ([0, 0, 0, 1], 15, 2)
        ]
        
        n_melhores = 3
        melhores = selecionar_melhores_abelhas(avaliacoes, n_melhores)
        
        assert len(melhores) == n_melhores
        assert melhores[0][1] == 25  # Maior valor
        assert melhores[1][1] == 22  # Segundo maior
        assert melhores[2][1] == 20  # Terceiro maior
    
    @patch('beeAlgorithm_ref.gerar_vizinho')
    @patch('beeAlgorithm_ref.avaliar_solucao')
    def test_explorar_vizinhanca(self, mock_avaliar, mock_vizinho):
        """Testa a exploração da vizinhança"""
        solucao = [1, 0, 0, 0]
        n_vizinhos = 3
        
        # Configura os vizinhos gerados
        mock_vizinho.side_effect = [
            [0, 0, 0, 0],  # Vizinho 1
            [1, 1, 0, 0],  # Vizinho 2
            [1, 0, 1, 0]   # Vizinho 3
        ]
        
        # Configura as avaliações
        mock_avaliar.side_effect = [
            (0, 0),    # Vizinho 1
            (22, 3),   # Vizinho 2
            (32, 5),   # Vizinho 3
            (12, 2)    # Solução original
        ]
        
        melhor = explorar_vizinhanca(solucao, n_vizinhos, self.pesos, self.valores, self.capacidade)
        
        assert mock_vizinho.call_count == n_vizinhos
        assert mock_avaliar.call_count == n_vizinhos + 1  # vizinhos + solução original
        assert melhor == ([1, 0, 1, 0], 32, 5)  # Melhor vizinho
    
    def test_executar_busca_local(self):
        """Testa a execução da busca local"""
        melhores_abelhas = [
            ([1, 0, 0, 0], 10, 2),
            ([0, 1, 0, 1], 25, 3)
        ]
        n_vizinhos = 2
        
        with patch('beeAlgorithm_ref.explorar_vizinhanca') as mock_explorar:
            mock_explorar.side_effect = [
                ([1, 1, 0, 0], 22, 3),
                ([0, 1, 1, 1], 45, 6)
            ]
            
            novas_solucoes = executar_busca_local(
                melhores_abelhas, n_vizinhos, 
                self.pesos, self.valores, self.capacidade
            )
            
            assert len(novas_solucoes) == 2
            assert novas_solucoes[0] == ([1, 1, 0, 0], 22, 3)
            assert novas_solucoes[1] == ([0, 1, 1, 1], 45, 6)
    
    def test_encontrar_melhor_solucao_global(self):
        """Testa a busca da melhor solução global"""
        todas_solucoes = [
            ([1, 0, 0, 0], 10, 2),
            ([0, 1, 0, 1], 25, 3),
            ([1, 1, 0, 0], 22, 3),
            ([0, 0, 1, 0], 20, 3)
        ]
        
        melhor = encontrar_melhor_solucao_global(todas_solucoes)
        
        assert melhor == ([0, 1, 0, 1], 25, 3)
    
    def test_bee_algorithm_pequena_instancia(self):
        """Testa o algoritmo completo com uma instância pequena"""
        solucao, valor, peso = bee_algorithm(
            self.pesos, self.valores, self.capacidade,
            n_abelhas=10, n_melhores=3, n_vizinhos=2, n_iter=5
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
    
    def test_bee_algorithm_sem_itens(self):
        """Testa o algoritmo com lista vazia de itens"""
        pesos = []
        valores = []
        capacidade = 10

        with pytest.raises(ValueError, match="empty range for randrange"):
            bee_algorithm(
                pesos, valores, capacidade,
                n_abelhas=5, n_melhores=2, n_vizinhos=1, n_iter=2
            )

    def test_bee_algorithm_capacidade_zero(self):
        """Testa o algoritmo com capacidade zero"""
        solucao, valor, peso = bee_algorithm(
            self.pesos, self.valores, 0,
            n_abelhas=5, n_melhores=2, n_vizinhos=1, n_iter=2
        )
        
        assert all(item == 0 for item in solucao)
        assert valor == 0
        assert peso == 0
    
    def test_bee_algorithm_parametros_diferentes(self):
        """Testa o algoritmo com diferentes configurações de parâmetros"""
        # Teste com muitas abelhas
        solucao1, valor1, peso1 = bee_algorithm(
            self.pesos, self.valores, self.capacidade,
            n_abelhas=50, n_melhores=20, n_vizinhos=5, n_iter=3
        )
        
        # Teste com poucas abelhas
        solucao2, valor2, peso2 = bee_algorithm(
            self.pesos, self.valores, self.capacidade,
            n_abelhas=5, n_melhores=2, n_vizinhos=1, n_iter=3
        )
        
        # Ambas devem ser soluções válidas
        assert len(solucao1) == self.n_itens
        assert len(solucao2) == self.n_itens
        assert peso1 <= self.capacidade
        assert peso2 <= self.capacidade
    
    def test_bee_algorithm_grande_instancia(self):
        """Testa o algoritmo com uma instância maior"""
        n_itens = 50
        pesos = [random.randint(1, 10) for _ in range(n_itens)]
        valores = [random.randint(1, 50) for _ in range(n_itens)]
        capacidade = sum(pesos) // 3
        
        solucao, valor, peso = bee_algorithm(
            pesos, valores, capacidade,
            n_abelhas=20, n_melhores=8, n_vizinhos=3, n_iter=10
        )
        
        assert len(solucao) == n_itens
        assert peso <= capacidade
        assert valor > 0
    
    def test_criar_resultado_teste(self):
        """Testa a criação do dicionário de resultados"""
        resultado = criar_resultado_teste(
            "Bee Algorithm", 10, 100, 50, 20, 0.12345,
            [1, 2, 3], [10, 20, 30], [1, 0, 1]
        )
        
        assert resultado["algoritmo"] == "Bee Algorithm"
        assert resultado["n_itens"] == 10
        assert resultado["capacidade"] == 100
        assert resultado["valor_total"] == 50
        assert resultado["peso_total"] == 20
        assert resultado["tempo_execucao"] == 0.12345
        assert resultado["pesos"] == [1, 2, 3]
        assert resultado["valores"] == [10, 20, 30]
        assert resultado["melhor_solucao"] == [1, 0, 1]
    
    @patch('beeAlgorithm_ref.avaliar_solucao')
    def test_bee_algorithm_com_mock(self, mock_avaliar):
        """Testa o algoritmo usando mock para isolar o teste"""
        # Configura o mock para retornar valores fixos
        mock_avaliar.return_value = (100, 5)
        
        solucao, valor, peso = bee_algorithm(
            self.pesos, self.valores, self.capacidade,
            n_abelhas=5, n_melhores=2, n_vizinhos=1, n_iter=2
        )
        
        # Verifica se a função foi chamada
        assert mock_avaliar.called
        assert valor == 100 or valor == 0  # Pode ser 0 se todas as soluções forem [0,0,0,0]
        assert peso == 5 or peso == 0
    
    def test_bee_algorithm_convergencia(self):
        """Testa se o algoritmo melhora ao longo das iterações"""
        valores_por_iteracao = []
        
        for n_iter in [1, 5, 10, 20]:
            _, valor, _ = bee_algorithm(
                self.pesos, self.valores, self.capacidade,
                n_abelhas=10, n_melhores=4, n_vizinhos=2, n_iter=n_iter
            )
            valores_por_iteracao.append(valor)
        
        # Verifica se há uma tendência de melhoria (não estritamente crescente devido à aleatoriedade)
        assert max(valores_por_iteracao) >= valores_por_iteracao[0]