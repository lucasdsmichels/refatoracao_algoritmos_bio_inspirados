#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# importa as funções originais e _ref de cada algoritmo
from bee_algorithm import beeAlgorithm, beeAlgorithm_ref
from aco import algColonFormigas, algColonFormigas_ref
from cuckoo import algCuckoo, algCuckoo_ref
from geneticos import algGeneticos, algGeneticos_ref
from pso import algEnxParticulas, algEnxParticulas_ref

def run_and_label(obj, nome_alg, versao):
    """
    Se 'obj' for um módulo com main(), chama obj.main().
    Caso contrário, chama obj() diretamente.
    """
    if hasattr(obj, 'main'):
        df = obj.main()
    else:
        df = obj()
    df['algoritmo'] = nome_alg
    df['versao'] = versao
    return df[['n_itens', 'tempo_execucao', 'algoritmo', 'versao']]

# executa todos os orig/ref
dfs = [
    run_and_label(beeAlgorithm,         'Bee Algorithm',      'orig'),
    run_and_label(beeAlgorithm_ref,     'Bee Algorithm',      'ref'),
    run_and_label(algColonFormigas,     'Algoritmo ACO',      'orig'),
    run_and_label(algColonFormigas_ref, 'Algoritmo ACO',      'ref'),
    run_and_label(algCuckoo,            'Cuckoo Search',      'orig'),
    run_and_label(algCuckoo_ref,        'Cuckoo Search',      'ref'),
    run_and_label(algEnxParticulas,     'PSO',                'orig'),
    run_and_label(algEnxParticulas_ref, 'PSO',                'ref'),
    run_and_label(algGeneticos,         'Algoritmo Genético', 'orig'),
    run_and_label(algGeneticos_ref,     'Algoritmo Genético', 'ref'),
]

# concatena e pivota
df_all = pd.concat(dfs, ignore_index=True)
df_cmp = df_all.pivot_table(
    index='n_itens',
    columns=['algoritmo', 'versao'],
    values='tempo_execucao'
).reset_index()

# 1) Achata o MultiIndex das colunas em strings "Algoritmo (versao)"
new_cols = ['n_itens'] + [
    f"{alg} ({versao})"
    for alg, versao in df_cmp.columns[1:].tolist()
]
df_cmp.columns = new_cols

# 2) Reordena para ficar: n_itens, [Bee orig, Bee ref, ACO orig, ACO ref, ...]
desired_order = ['n_itens']
for alg in ['Bee Algorithm', 'Algoritmo ACO', 'Cuckoo Search', 'PSO', 'Algoritmo Genético']:
    for ver in ['orig', 'ref']:
        colname = f"{alg} ({ver})"
        if colname in df_cmp.columns:
            desired_order.append(colname)

df_cmp = df_cmp[desired_order]

# 3) Imprime em Markdown com 5 casas decimais
print(df_cmp.to_markdown(index=False, floatfmt=".5f"))
