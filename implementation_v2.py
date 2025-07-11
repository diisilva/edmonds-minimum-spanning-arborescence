#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
implementation_v2.py
--------------------
Implementação de Arborescência Mínima (Directed MST) com:

  1) Edmonds recursivo (Chu–Liu/Edmonds)
  2) Gabow et al. (GGST) seguindo o pseudocódigo exato do artigo

Uso:
    from implementation_v2 import DirectedMST
    mst_ed = DirectedMST().edmonds_msa(V, E, r, w)
    mst_gb = DirectedMST().gabow_msa(V, E, r, w)
"""

from copy import deepcopy
import heapq

# -------------------------------------------------------------------------
# 0) DSU para contrações
# -------------------------------------------------------------------------
class UnionFind:
    def __init__(self, elems):
        self.p = {v: v for v in elems}
        self.r = {v: 0 for v in elems}

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True

# -------------------------------------------------------------------------
# 1) Edmonds (Chu–Liu/Edmonds)
# -------------------------------------------------------------------------
class DirectedMST:
    def __init__(self):
        self._vcounter = -1

    def edmonds_msa(self, V, E, r, w):
        """
        Implementação recursiva de Chu–Liu/Edmonds para
        Directed Minimum Spanning Arborescence.
        """
        V, E, w = set(V), set(E), dict(w)
        # Passo 1: remover arestas de entrada em r
        E = {(u, v) for (u, v) in E if v != r}
        w = {e: c for e, c in w.items() if e in E}
        # Passo 2: escolher π(v) para cada v ≠ r
        pi = {}
        for v in V - {r}:
            inc = [(u, vv) for (u, vv) in E if vv == v]
            if not inc:
                raise ValueError(f"Vértice {v} sem incoming edge")
            pi[v] = min(inc, key=lambda e: w[e])
        # Passo 3: detectar ciclo
        cycle_start = None
        for v in V - {r}:
            seen, cur = set(), v
            while cur not in seen and cur != r:
                seen.add(cur)
                cur = pi[cur][0]
            if cur in seen:
                cycle_start = cur
                break
        # Passo 4: sem ciclo → retornar arborescência
        if cycle_start is None:
            return set(pi.values())
        # Passo 5: identificar ciclo C
        C = {cycle_start}
        cur = pi[cycle_start][0]
        while cur not in C:
            C.add(cur)
            cur = pi[cur][0]
        # Passo 6: contrair C em novo vértice v_c
        v_c = self._vcounter
        self._vcounter -= 1
        Vp = (V - C) | {v_c}
        Ep, wp, corr = set(), {}, {}
        for (u, v) in E:
            cost = w[(u, v)]
            if u not in C and v in C:
                e = (u, v_c)
                adj = cost - w[pi[v]]
                if e not in wp or wp[e] > adj:
                    wp[e], corr[e] = adj, (u, v)
                Ep.add(e)
            elif u in C and v not in C:
                e = (v_c, v)
                if e not in wp or wp[e] > cost:
                    wp[e], corr[e] = cost, (u, v)
                Ep.add(e)
            elif u not in C and v not in C:
                Ep.add((u, v))
                wp[(u, v)] = cost
        # Passo 7: recursão em grafo contraído
        treep = self.edmonds_msa(Vp, Ep, r, wp)
        # Passo 8: reexpansão
        for e in treep:
            if e[1] == v_c:
                chosen = corr[e]
                break
        result = set()
        for e in treep:
            if e[1] == v_c:
                result.add(chosen)
            else:
                result.add(e)
        for v in C:
            e = pi[v]
            if e != chosen:
                result.add(e)
        return result

    # ---------------------------------------------------------------------
    # 2) Gabow et al. (GGST) – implementação direta do pseudocódigo
    # ---------------------------------------------------------------------
    def gabow_msa(self, V, E, r, w):
        """
        Algorithm 1 de Gabow et al.:
          1) initial path ← [r]
          2) exit_lists[r] ← incoming_edges(r)
          3) while len(recon) < |V|:
             4) query min edge (u,v) de active forest
             5) recon[v] ← (u,v)
             6) se find(u) não em path:
                  inserir incoming_edges(u) em exit_lists[u]
                  path.append(find(u))
               senão:
                  deletar prefixo de path até última ocorrência de find(u)
                  ajustar custos em exit_lists e active
                  remover outgoing edges de prefixo em exit_lists
                  unir prefixo em UF e limitar 1 edge por origem
                  rebuild de path
             7) inserir find(u) na frente de path
          8) return set(recon.values()) filtrado
        """
        V, E, w = set(V), set(E), dict(w)
        # 0) inicializar DSU e exit_lists
        uf = UnionFind(V)
        exit_lists = {v: [] for v in V}
        # exit_lists[r] recebe todas as arestas que entram em r
        for (u, v) in E:
            if v == r:
                exit_lists[r].append((w[(u, v)], u, v))
        heapq.heapify(exit_lists[r])
        # remover arestas de entrada em r para o loop principal
        E = {(u, v) for (u, v) in E if v != r}
        w = {e: c for e, c in w.items() if e in E}
        path = [r]
        active = []
        recon = {}

        # loop principal: até extrair |V| arcos
        while len(recon) < len(V):
            head = path[-1]
            # inserir arestas de exit_lists[head] em active
            while exit_lists[head]:
                heapq.heappush(active, heapq.heappop(exit_lists[head]))
            # extrair aresta de menor custo
            if not active:
                raise ValueError("Grafo desconexo")
            cost, u, v = heapq.heappop(active)
            cu, cv = uf.find(u), uf.find(v)
            recon[cv] = (u, v)
            # se componente de u não está em path → expandir
            if cu not in path:
                for (x, y) in E:
                    if y == u:
                        heapq.heappush(exit_lists[cu], (w[(x, y)], x, y))
                path.append(cu)
            else:
                # ciclo detectado → contrair prefixo
                idx = max(i for i, p in enumerate(path) if p == cu)
                prefix = path[idx+1:]
                # ajustar custos em exit_lists e active
                for z in prefix:
                    pu, pv = recon[z]
                    delta = w[(pu, pv)]
                    exit_lists[z] = [(c - delta, a, b)
                                     for (c, a, b) in exit_lists[z]]
                    active = [(c - delta, a, b)
                              for (c, a, b) in active if b != z]
                    heapq.heapify(active)
                # unir prefixo em DSU
                for z in prefix:
                    uf.union(cu, z)
                # limitar 1 edge por origem em active
                best = {}
                for (c, a, b) in active:
                    if a not in best or c < best[a][0]:
                        best[a] = (c, a, b)
                active = list(best.values())
                heapq.heapify(active)
                # rebuild de path até ciclo
                path = path[:idx+1]
            # inserir componente de u na frente de path
            mu = uf.find(u)
            if mu not in path:
                path.insert(0, mu)

        # retorna só arcos que não apontam para a raiz
        return { (u, v) for (u, v) in recon.values() if v != r }

# -------------------------------------------------------------------------
# Teste rápido
# -------------------------------------------------------------------------
if __name__ == "__main__":
    V = {0, 1, 2}
    E = {(0, 1), (1, 2), (2, 0)}
    r = 0
    w = {(0, 1): 5.0, (1, 2): 3.0, (2, 0): 4.0}

    solver = DirectedMST()
    print("Edmonds MST:", solver.edmonds_msa(V, E, r, w))
    print("Gabow MST:  ", solver.gabow_msa(V, E, r, w))
