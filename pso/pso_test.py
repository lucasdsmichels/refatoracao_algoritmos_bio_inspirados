import pytest
import random
import time
from pso.algEnxParticulas_ref import (
    sigmoid,
    binarizar,
    inicializar_particula,
    calcular_nova_velocidade,
    atualizar_velocidade,
    atualizar_posicao,
    avaliar_particula,
    inicializar_enxame,
    encontrar_melhor_global,
    atualizar_melhor_pessoal,
    pso,
    executar_teste
)

class TestPSO:
    @pytest.fixture(autouse=True)
    def seed_random(self):
        random.seed(0)

    def test_sigmoid(self):
        assert pytest.approx(sigmoid(0), rel=1e-3) == 0.5
        assert sigmoid(100) > 0.99
        assert sigmoid(-100) < 0.01

    def test_binarizar(self):
        # valores acima e abaixo do limiar
        pos = [-10, 0, 10]
        resultado = binarizar(pos)
        assert resultado == [0, 1, 1]

    def test_inicializar_particula(self):
        # monkeypatch random.uniform para retornar extremo
        random_values = [-3.0, -2.5, 0.5, -0.5]
        def fake_uniform(a, b):
            return random_values.pop(0)
        random.uniform = fake_uniform
        pos, vel = inicializar_particula(2)
        assert pos == [-3.0, -2.5]
        assert vel == [0.5, -0.5]

    def test_calcular_nova_velocidade_e_clamp(self):
        # fixa r1 e r2
        random.random = lambda: 1.0
        vel = [10]
        pos = [0]
        bp = [0]
        bg = [0]
        # sem cog/soc, w*10=8, mas clamp em 4
        nova = calcular_nova_velocidade(vel, pos, bp, bg, 0)
        assert nova == 4  # limite máximo

    def test_atualizar_velocidade(self):
        # monkeypatch calcular_nova_velocidade
        calls = []
        def fake_calc(v, p, bp, bg, i):
            calls.append(i)
            return i * 0.1
        vel = [0, 0]
        pos = [0, 0]
        bp = [0, 0]
        bg = [0, 0]
        from pso.algEnxParticulas_ref import calcular_nova_velocidade as real_calc
        # substitui temporariamente
        import pso.algEnxParticulas_ref as mod
        mod.calcular_nova_velocidade = fake_calc
        nova = atualizar_velocidade(vel, pos, bp, bg)
        assert nova == [0.0, 0.1]
        assert calls == [0, 1]
        # restaura
        mod.calcular_nova_velocidade = real_calc

    def test_atualizar_posicao(self):
        pos = [1, 2]
        vel = [0.5, -1]
        assert atualizar_posicao(pos, vel) == [1.5, 1]

    @pytest.mark.parametrize("solucao_binaria,retorno", [
        ([1, 0], (10, 5)),
    ])
    def test_avaliar_particula(self, monkeypatch, solucao_binaria, retorno):
        # binarizar retorna solucao_binaria e avaliar_solucao retorna retorno
        monkeypatch.setattr('pso.algEnxParticulas_ref.binarizar', lambda x: solucao_binaria)
        monkeypatch.setattr('utils.avaliar_solucao', lambda s, p, v, c: retorno)
        valor = avaliar_particula([0, 0], [1, 2], [10, 20], 5)
        assert valor == 10

    def test_inicializar_enxame(self, monkeypatch):
        # monkeypatch inicializar_particula e avaliar_particula
        monkeypatch.setattr('pso.algEnxParticulas_ref.inicializar_particula', lambda n: ([0], [0]))
        monkeypatch.setattr('pso.algEnxParticulas_ref.avaliar_particula', lambda p, w, v, c: 42)
        enxame = inicializar_enxame(1, [1], [1], 1)
        assert len(enxame) == 30
        for particula in enxame:
            assert particula['posicao'] == [0]
            assert particula['velocidade'] == [0]
            assert particula['melhor_posicao'] == [0]
            assert particula['melhor_valor'] == 42

    def test_encontrar_melhor_global(self):
        particulas = [
            {'melhor_posicao': [0], 'melhor_valor': 1},
            {'melhor_posicao': [1], 'melhor_valor': 5},
            {'melhor_posicao': [2], 'melhor_valor': 3}
        ]
        pos, valor = encontrar_melhor_global(particulas)
        assert pos == [1]
        assert valor == 5

    def test_atualizar_melhor_pessoal(self, monkeypatch):
        particula = {'posicao': [0], 'melhor_posicao': [1], 'melhor_valor': 1}
        # sem melhoria
        monkeypatch.setattr('pso.algEnxParticulas_ref.avaliar_particula', lambda p, w, v, c: 0)
        atualizar_melhor_pessoal(particula, [], [], 0)
        assert particula['melhor_valor'] == 1
        # com melhoria
        monkeypatch.setattr('pso.algEnxParticulas_ref.avaliar_particula', lambda p, w, v, c: 10)
        atualizar_melhor_pessoal(particula, [], [], 0)
        assert particula['melhor_valor'] == 10
        assert particula['melhor_posicao'] == particula['posicao']

    def test_executar_teste(self, monkeypatch):
        # instancia controlada
        monkeypatch.setattr('utils.gerar_instancia_aleatoria', lambda n, **kw: ([1,2], [3,4], 5))
        # pso retorna solucao e valor fixos
        monkeypatch.setattr('pso.algEnxParticulas_ref.pso', lambda n, p, v, c: ([1,0], 7))
        # fixa tempo
        monkeypatch.setattr(time, 'time', lambda: 100)
        resultado = executar_teste(2)
        assert resultado['algoritmo'] == 'PSO'
        assert resultado['n_itens'] == 2
        assert resultado['valor_total'] == 7
        assert resultado['peso_total'] != 1*1 + 2*0
        assert 'tempo_execucao' in resultado
