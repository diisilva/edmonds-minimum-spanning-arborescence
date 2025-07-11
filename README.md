# Algoritmo de Edmonds para Arborescência Mínima

Este projeto contém uma implementação do algoritmo de Edmonds (também conhecido como algoritmo de Chu–Liu/Edmonds) para encontrar a Arborescência Mínima (Minimum Spanning Arborescence) em grafos direcionados.

## Sobre o Artigo

Este projeto é baseado no artigo "Efficiently Computing Directed Minimum Spanning Trees", um trabalho científico publicado em 2022 como preprint no arXiv. O artigo foca na otimização do cálculo de árvores geradoras mínimas em grafos direcionados.

### Autores
- Maximilian Böther - Hasso Plattner Institute
- Otto Kißig - Hasso Plattner Institute
- Christopher Weyand - Karlsruhe Institute of Technology

O artigo pode ser encontrado gratuitamente em: [https://arxiv.org/pdf/2208.02590](https://arxiv.org/pdf/2208.02590)

## O que é uma Arborescência Mínima?

Uma arborescência é uma árvore dirigida onde todos os vértices são acessíveis a partir de um único vértice raiz. Uma arborescência mínima é aquela que tem o menor custo total das arestas, considerando um grafo dirigido com pesos nas arestas.

## Sobre o Algoritmo de Edmonds

O algoritmo de Edmonds, descoberto independentemente por Jack Edmonds, Y. J. Chu e T. H. Liu nos anos 1960, resolve o problema de encontrar a arborescência mínima em grafos direcionados ponderados. Os passos principais do algoritmo são:

1. Selecionar para cada vértice (exceto a raiz) a aresta de entrada de menor custo
2. Verificar se há ciclos nessas seleções
3. Se não houver ciclos, o conjunto de arestas selecionado forma a arborescência mínima
4. Se houver ciclos, contrair cada ciclo em um único vértice e ajustar os pesos das arestas
5. Resolver recursivamente o problema no grafo contraído
6. Expandir os ciclos e reconstruir a arborescência original

A implementação tem complexidade temporal O(n·m), onde n é o número de vértices e m é o número de arestas do grafo.

## Estrutura do Projeto

- `implementation_v1.py`: Código-fonte da implementação do algoritmo
- `relatorio_txt.txt`: Relatório sobre o artigo "Efficiently Computing Directed Minimum Spanning Trees"
- `README.md`: Este arquivo de documentação

## Como Utilizar

### Requisitos

- Python 3.x

### Execução

1. Clone ou baixe este repositório
2. Execute o script diretamente para ver o exemplo de demonstração:

```bash
python implementation_v1.py
```

### Uso como Módulo

```python
from implementation_v1 import Edmonds

# Definir o grafo
V = {0, 1, 2, 3}               # Conjunto de vértices
E = {(0, 1), (1, 2), (2, 3)}   # Conjunto de arestas direcionadas (u, v)
r = 0                          # Vértice raiz
w = {(0, 1): 1.0, (1, 2): 2.0, (2, 3): 3.0}  # Pesos das arestas

# Executar o algoritmo
edmonds = Edmonds()
mst = edmonds.msa(V, E, r, w)

# Mostrar resultado
print("Arborescência mínima:", mst)
```

## Exemplos Incluídos

No código-fonte, há quatro exemplos comentados que demonstram diferentes casos:

1. Grafo simples sem ciclos
2. Grafo com ciclo
3. Grafo com vértice inacessível (lança erro)
4. Exemplo clássico com ciclo na arborescência

Para testar qualquer um destes exemplos, descomente o trecho correspondente no final do arquivo `implementation_v1.py`.

## Referência Teórica

Esta implementação é baseada no artigo "Efficiently Computing Directed Minimum Spanning Trees" de Maximilian Böther, Otto Kißig e Christopher Weyand, que discute vários algoritmos para resolver o problema da arborescência mínima, incluindo o algoritmo original de Edmonds e suas otimizações posteriores por Tarjan e outros pesquisadores.

O artigo apresenta uma comparação abrangente entre várias abordagens algorítmicas para o problema, desde as mais simples até as mais complexas, avaliando o custo-benefício de estruturas de dados avançadas no desempenho final. Os autores disponibilizaram todo o código-fonte das implementações de forma aberta, incluindo a primeira implementação pública do algoritmo GGST (Gabow, Galil, Spencer e Tarjan).
