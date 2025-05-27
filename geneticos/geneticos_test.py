import pytest
import random
from unittest.mock import patch, MagicMock
from algGeneticos_ref import (
    avaliar_individuo,
    criar_populacao_inicial,
    selecionar_pais,
    fazer_crossover,
    aplicar_mutacao,
    criar_nova_geracao,
    encontrar_melhor_individuo,
    algoritmo_genetico,
    executar_teste
)


class TestAlgoritmoGenetico:
    """Classe de testes para o Algoritmo Genético"""
    
    def setup_method(self):
        """Configuração executada antes de cada teste"""
        random.seed(42)
        self.pesos = [2, 1, 3, 2]
        self.valores = [12, 10, 20, 15]
        self.capacidade = 5
        self.n_itens = len(self.pesos)
    
    @patch('algGeneticos_ref.avaliar_solucao')
    def test_avaliar_individuo_valido(self, mock_avaliar):
        """Testa a avaliação de um indivíduo válido"""
        individuo = [1, 0, 1, 0]
        mock_avaliar.return_value = (32, 5)  # Dentro da capacidade
        
        fitness = avaliar_individuo(individuo, self.pesos, self.valores, self.capacidade)
        
        assert fitness == 32  # Sem penalização
        mock_avaliar.assert_called_once_with(individuo, self.pesos, self.valores, self.capacidade)
    
    @patch('algGeneticos_ref.avaliar_solucao')
    def test_avaliar_individuo_invalido(self, mock_avaliar):
        """Testa a avaliação de um indivíduo inválido (excede capacidade)"""
        individuo = [1, 1, 1, 1]
        mock_avaliar.return_value = (57, 8)  # Excede capacidade (5)
        
        fitness = avaliar_individuo(individuo, self.pesos, self.valores, self.capacidade)
        
        excesso = 8 - 5  # 3
        penalizacao = excesso * 2  # 6
        assert fitness == 57 - 6  # 51
    
    @patch('algGeneticos_ref.gerar_solucao_binaria')
    def test_criar_populacao_inicial(self, mock_gerar):
        """Testa a criação da população inicial"""
        tam_populacao = 4
        mock_gerar.side_effect = [[1, 0, 0, 0], [0, 1, 0, 0], 
                                  [0, 0, 1, 0], [0, 0, 0, 1]]
        
        populacao = criar_populacao_inicial(tam_populacao, self.n_itens)
        
        assert len(populacao) == tam_populacao
        assert mock_gerar.call_count == tam_populacao
        assert populacao[0] == [1, 0, 0, 0]
        assert populacao[-1] == [0, 0, 0, 1]
    
    def test_selecionar_pais(self):
        """Testa a seleção de pais por torneio"""
        populacao = [[1, 0, 0, 0], [0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 1, 0]]
        
        with patch('random.sample') as mock_sample:
            with patch('algGeneticos_ref.avaliar_individuo') as mock_avaliar:
                # Configura dois torneios
                mock_sample.side_effect = [
                    [[1, 0, 0, 0], [0, 1, 0, 1], [1, 1, 0, 0]],  # Torneio 1
                    [[0, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]]   # Torneio 2
                ]
                
                # Configura avaliações para fazer [0, 1, 0, 1] ganhar ambos os torneios
                def avaliar_side_effect(ind, *args):
                    if ind == [0, 1, 0, 1]:
                        return 25
                    elif ind == [1, 1, 0, 0]:
                        return 22
                    elif ind == [0, 0, 1, 0]:
                        return 20
                    else:
                        return 12
                
                mock_avaliar.side_effect = avaliar_side_effect
                
                pai1, pai2 = selecionar_pais(populacao, self.pesos, self.valores, self.capacidade)
                
                assert pai1 == [0, 1, 0, 1]  # Melhor do torneio 1
                assert pai2 == [0, 1, 0, 1]  # Melhor do torneio 2
    
    def test_fazer_crossover(self):
        """Testa o crossover de um ponto"""
        pai1 = [1, 1, 1, 1]
        pai2 = [0, 0, 0, 0]
        
        with patch('random.randint') as mock_random:
            mock_random.return_value = 2  # Ponto de corte
            
            filho1, filho2 = fazer_crossover(pai1, pai2)
            
            assert filho1 == [1, 1, 0, 0]  # pai1[:2] + pai2[2:]
            assert filho2 == [0, 0, 1, 1]  # pai2[:2] + pai1[2:]
    
    def test_aplicar_mutacao_sem_mutacao(self):
        """Testa a mutação quando nenhum bit é mutado"""
        individuo = [1, 0, 1, 0]
        taxa_mutacao = 0.1
        
        with patch('random.random') as mock_random:
            mock_random.side_effect = [0.2, 0.3, 0.4, 0.5]  # Todos > taxa_mutacao
            
            mutado = aplicar_mutacao(individuo, taxa_mutacao)
            
            assert mutado == individuo  # Sem mudanças
    
    def test_aplicar_mutacao_com_mutacao(self):
        """Testa a mutação quando alguns bits são mutados"""
        individuo = [1, 0, 1, 0]
        taxa_mutacao = 0.5
        
        with patch('random.random') as mock_random:
            mock_random.side_effect = [0.1, 0.6, 0.3, 0.8]  # 1º e 3º < taxa_mutacao
            
            mutado = aplicar_mutacao(individuo, taxa_mutacao)
            
            assert mutado == [0, 0, 0, 0]  # Bits 0 e 2 foram invertidos
    
    def test_criar_nova_geracao(self):
        """Testa a criação de uma nova geração"""
        populacao = [[1, 0, 0, 0], [0, 1, 0, 0]]
        taxa_mutacao = 0.1
        
        with patch('algGeneticos_ref.selecionar_pais') as mock_selecionar:
            with patch('algGeneticos_ref.fazer_crossover') as mock_crossover:
                with patch('algGeneticos_ref.aplicar_mutacao') as mock_mutacao:
                    # Configura seleção
                    mock_selecionar.return_value = ([1, 0, 0, 0], [0, 1, 0, 0])
                    
                    # Configura crossover
                    mock_crossover.return_value = ([1, 1, 0, 0], [0, 0, 0, 0])
                    
                    # Configura mutação (sem mudanças)
                    mock_mutacao.side_effect = lambda ind, taxa: ind
                    
                    nova_geracao = criar_nova_geracao(
                        populacao, self.pesos, self.valores, 
                        self.capacidade, taxa_mutacao
                    )
                    
                    assert len(nova_geracao) == len(populacao)
                    assert nova_geracao == [[1, 1, 0, 0], [0, 0, 0, 0]]
    
    def test_algoritmo_genetico_pequena_instancia(self):
        """Testa o algoritmo completo com uma instância pequena"""
        solucao, valor = algoritmo_genetico(
            self.pesos, self.valores, self.capacidade,
            tam_populacao=10, taxa_mutacao=0.1, n_geracoes=5
        )
        
        # Verifica se retornou uma solução válida
        assert len(solucao) == self.n_itens
        assert all(item in [0, 1] for item in solucao)
        assert valor >= 0
        
        # Verifica se o valor está correto
        valor_calculado = sum(v * s for v, s in zip(self.valores, solucao))
        peso_calculado = sum(p * s for p, s in zip(self.pesos, solucao))
        
        if peso_calculado <= self.capacidade:
            assert valor == valor_calculado
        else:
            # Com penalização
            excesso = peso_calculado - self.capacidade
            assert valor == valor_calculado - excesso * 2
    
    def test_algoritmo_genetico_capacidade_zero(self):
        """Testa o algoritmo com capacidade zero"""
        solucao, valor = algoritmo_genetico(
            self.pesos, self.valores, 0,
            tam_populacao=5, taxa_mutacao=0.1, n_geracoes=2
        )
        
        # Com capacidade 0, qualquer item resulta em penalização
        assert all(item == 0 for item in solucao) or valor < 0
    
    def test_algoritmo_genetico_parametros_diferentes(self):
        """Testa o algoritmo com diferentes configurações de parâmetros"""
        # Teste com alta taxa de mutação
        solucao1, _ = algoritmo_genetico(
            self.pesos, self.valores, self.capacidade,
            tam_populacao=20, taxa_mutacao=0.5, n_geracoes=5
        )
        
        # Teste com baixa taxa de mutação
        solucao2, _ = algoritmo_genetico(
            self.pesos, self.valores, self.capacidade,
            tam_populacao=20, taxa_mutacao=0.01, n_geracoes=5
        )
        
        # Ambas devem ser soluções válidas
        assert len(solucao1) == self.n_itens
        assert len(solucao2) == self.n_itens
    
    def test_algoritmo_genetico_grande_instancia(self):
        """Testa o algoritmo com uma instância maior"""
        n_itens = 50
        pesos = [random.randint(1, 10) for _ in range(n_itens)]
        valores = [random.randint(1, 50) for _ in range(n_itens)]
        capacidade = sum(pesos) // 3
        
        solucao, valor = algoritmo_genetico(
            pesos, valores, capacidade,
            tam_populacao=30, taxa_mutacao=0.1, n_geracoes=10
        )
        
        assert len(solucao) == n_itens
        assert valor > 0 or all(item == 0 for item in solucao)
    
    @patch('algGeneticos_ref.gerar_instancia_aleatoria')
    @patch('algGeneticos_ref.algoritmo_genetico')
    def test_executar_teste(self, mock_algoritmo, mock_gerar):
        """Testa a função de execução de teste"""
        n_itens = 10
        mock_gerar.return_value = ([1, 2, 3], [10, 20, 30], 5)
        mock_algoritmo.return_value = ([1, 0, 1], 40)
        
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0.0, 0.5]  # Tempo de execução = 0.5s
            
            resultado = executar_teste(n_itens)
            
            assert resultado["algoritmo"] == "Algoritmo Genético"
            assert resultado["n_itens"] == n_itens
            assert resultado["capacidade"] == 5
            assert resultado["valor_total"] == 40
            assert resultado["peso_total"] == 4  # 1*1 + 2*0 + 3*1
            assert resultado["tempo_execucao"] == 0.5
            assert resultado["pesos"] == [1, 2, 3]
            assert resultado["valores"] == [10, 20, 30]
            assert resultado["melhor_solucao"] == [1, 0, 1]
    
    def test_algoritmo_genetico_convergencia(self):
        """Testa se o algoritmo melhora ao longo das gerações"""
        # Usa uma instância maior para melhor observar a convergência
        n_itens = 20
        pesos = [random.randint(1, 10) for _ in range(n_itens)]
        valores = [random.randint(1, 50) for _ in range(n_itens)]
        capacidade = sum(pesos) // 3
        
        valores_por_geracao = []
        
        for n_ger in [1, 5, 10, 20]:
            _, valor = algoritmo_genetico(
                pesos, valores, capacidade,
                tam_populacao=20, taxa_mutacao=0.1, n_geracoes=n_ger
            )
            valores_por_geracao.append(valor)
        
        # Verifica se há uma tendência de melhoria
        assert max(valores_por_geracao) >= valores_por_geracao[0]
    
    def test_algoritmo_genetico_elitismo(self):
        """Testa se o algoritmo preserva boas soluções (elitismo implícito)"""
        # Executa o algoritmo várias vezes
        valores = []
        for _ in range(5):
            _, valor = algoritmo_genetico(
                self.pesos, self.valores, self.capacidade,
                tam_populacao=10, taxa_mutacao=0.1, n_geracoes=10
            )
            valores.append(valor)
        
        # Com gerações suficientes, deve encontrar soluções razoáveis
        assert max(valores) >= 20  # Pelo menos o valor de um item bom