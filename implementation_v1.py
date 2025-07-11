#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edmonds_mst.py
----------------
Implementação do algoritmo de Edmonds (Chu–Liu/Edmonds) para encontrar a
Arborescência Mínima (Minimum Spanning Arborescence) em grafos direcionados.

Uso em memória:
    from edmonds_mst import Edmonds
    mst = Edmonds().msa(V, E, r, w)

Parâmetros:
    V   -> set de vértices (tipicamente int ou str)
    E   -> set de arestas (tuplas (u, v))
    r   -> vértice raiz (r ∈ V)
    w   -> dict mapeando cada aresta (u, v) para custo (float)

Retorna:
    set de arestas (u, v) que formam a arborescência mínima.

Erros lançados:
    ValueError para vértices inacessíveis (sem arestas de entrada)
"""

from copy import deepcopy

class Edmonds:
    """
    Classe que encapsula o estado do algoritmo de Edmonds, incluindo um
    contador para geração única de rótulos de vértices contraídos.
    """
    def __init__(self):
        # contador para novos vértices contraídos (valores negativos únicos)
        self._vcounter = -1

    def msa(self, V, E, r, w):
        """
        Executa recursivamente o algoritmo de Edmonds para arborescência mínima.

        Passos:
        1. Copiar V, E, w para não mutar objetos externos
        2. Remover arestas que apontam para a raiz
        3. Selecionar, para cada v != r, a aresta de menor custo entrando em v
        4. Detectar ciclos em pi; se não houver, retorno das arestas mínimas
        5. Identificar vértices do ciclo C
        6. Contrair C em novo vértice v_c
        7. Recursão em grafo contraído
        8. Reexpansão do ciclo e reconstrução da arborescência

        Lança:
            ValueError: se existir vértice além da raiz sem arestas de entrada
        """
        # 1. Cópias defensivas
        V = set(V)
        E = set(E)
        w = dict(w)

        # 2. Remover arestas para a raiz
        E = {(u, v) for (u, v) in E if v != r}
        w = {edge: cost for edge, cost in w.items() if edge in E}

        # 3. Encontrar aresta de menor custo para cada v != r
        pi = {}
        for v in V - {r}:
            incoming = [(u, _v) for (u, _v) in E if _v == v]
            if not incoming:
                continue
            # escolhe a aresta com peso mínimo
            min_edge = min(incoming, key=lambda e: w[e])
            pi[v] = min_edge

        # Verificar vértices sem incoming (inacessíveis)
        unreachable = (V - {r}) - set(pi.keys())
        if unreachable:
            raise ValueError(f"Vértices sem caminho de entrada: {unreachable}")

        # 4. Detectar ciclos em pi
        cycle_vertex = None
        for v in V:
            if v == r:
                continue
            visited = set()
            curr = v
            while curr not in visited and curr != r:
                visited.add(curr)
                curr = pi[curr][0]
            if curr in visited:
                cycle_vertex = curr
                break

        # 5. Sem ciclos: retorna diretamente conjunto de pi.values()
        if cycle_vertex is None:
            return set(pi.values())

        # 6. Identificar todos vértices do ciclo C
        C = {cycle_vertex}
        curr = pi[cycle_vertex][0]
        while curr != cycle_vertex:
            C.add(curr)
            curr = pi[curr][0]

        # 7. Contrair ciclo em novo vértice v_c
        v_c = self._vcounter
        self._vcounter -= 1
        V_prime = (V - C) | {v_c}
        E_prime = set()
        w_prime = {}
        corr = {}  # para mapear arestas de E_prime de volta às originais

        for (u, v) in E:
            cost = w[(u, v)]
            # entrada em C
            if u not in C and v in C:
                e = (u, v_c)
                adjusted = cost - w[pi[v]]
                if e not in w_prime or w_prime[e] > adjusted:
                    w_prime[e] = adjusted
                    corr[e] = (u, v)
                E_prime.add(e)
            # saída de C
            elif u in C and v not in C:
                e = (v_c, v)
                if e not in w_prime or w_prime[e] > cost:
                    w_prime[e] = cost
                    corr[e] = (u, v)
                E_prime.add(e)
            # aresta externa a C
            elif u not in C and v not in C:
                E_prime.add((u, v))
                w_prime[(u, v)] = cost

        # 8. Chamada recursiva no grafo contraído
        tree_prime = self.msa(V_prime, E_prime, r, w_prime)

        # 9. Reexpansão: encontrar aresta em tree_prime que aponta para v_c
        for (u, v) in tree_prime:
            if v == v_c:
                chosen = corr[(u, v)]
                break

        # 10. Reconstruir árvore final
        result = set()
        for (u, v) in tree_prime:
            if v == v_c:
                result.add(chosen)
            else:
                result.add((u, v))
        # adicionar arestas de pi do ciclo (exceto a removida)
        for v in C:
            edge = pi[v]
            if edge != chosen:
                result.add(edge)

        return result

# -----------------------------------------------------------------------------
# Exemplos de casos de teste de entrada (definir V, E, r, w):
# -----------------------------------------------------------------------------
# 1) Grafo simples sem ciclos:
# V = {0,1,2,3}
# E = {(0,1),(1,2),(2,3)}
# r = 0
# w = {(0,1):1.0,(1,2):2.0,(2,3):3.0}
# -> mst = {(0,1),(1,2),(2,3)}

# 2) Grafo com ciclo:
# V = {0,1,2}
# E = {(0,1),(1,2),(2,0)}
# r = 0
# w = {(0,1):5.0,(1,2):3.0,(2,0):4.0}
# -> mst = {(0,1),(1,2)}  # custo total = 8.0

# 3) Grafo com vértice inacessível:
# V = {0,1,2}
# E = {(0,1)}
# r = 0
# w = {(0,1):1.0}
# -> ValueError: Vértices sem caminho de entrada: {2}

# 4) Exemplo clássico de arborescência direcionada:
# V = {0,1,2,3}
# E = {(0,1),(0,2),(1,3),(2,3),(3,1)}
# r = 0
# w = {(0,1):1.0,(0,2):2.0,(1,3):1.5,(2,3):1.0,(3,1):0.5}
# -> mst = {(0,1),(2,3),(3,1)}  # custo total = 1.0+1.0+0.5 = 2.5

if __name__ == '__main__':
    # Demonstração rápida usando o caso com ciclo
    V = {0,1,2,3}
    E = {(0,1),(1,2),(2,3)}
    r = 0
    w = {(0,1):1.0,(1,2):2.0,(2,3):3.0}
    mst = Edmonds().msa(V, E, r, w)
    print("MST encontrado:", mst)
