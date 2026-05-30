from collections import deque

# Modelagem do Grafo (Vértices = Pontos de Decisão/Bifurcações)
# Vértice 0 (Entrada) até Vértice 7 (Saída)
grafo = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 4],
    3: [1],  # Beco sem saída
    4: [2, 5, 6],  # Tripla bifurcação
    5: [4],  # Beco sem saída
    6: [4, 7],
    7: [6],  # Saída
}


def dfs_caminho(grafo, inicio, objetivo):
    pilha = [(inicio, [inicio])]
    visitados = set()

    while pilha:
        vertice, caminho = pilha.pop()

        if vertice == objetivo:
            return caminho

        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]:
                if vizinho not in visitados:
                    pilha.append((vizinho, caminho + [vizinho]))
    return None


def bfs_caminho(grafo, inicio, objetivo):
    fila = deque([(inicio, [inicio])])
    visitados = set()

    while fila:
        vertice, caminho = fila.popleft()

        if vertice == objetivo:
            return caminho

        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]:
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [vizinho]))
    return None


if __name__ == "__main__":
    print(f"Caminho DFS (Pilha): {dfs_caminho(grafo, 0, 7)}")
    print(f"Caminho BFS (Fila):  {bfs_caminho(grafo, 0, 7)}")
