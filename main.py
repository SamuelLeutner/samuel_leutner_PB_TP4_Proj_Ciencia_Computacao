import random

from escalonador import MinHeap, simular_escalonador
from trie_arvore import Trie, PALAVRAS_PT_100
from labirinto_grafos import grafo, dfs_caminho, bfs_caminho


def run_tests() -> None:
    print("=" * 60)
    print(" TP4 - TESTES E VALIDAÇÕES (ORDEM COMPLETA) ")
    print("=" * 60)

    # ── EXERCÍCIO 1: Escalonador de Processos ─────────────────────────────────
    print("\n[Módulo 1] Simulação de Escalonador (Min-Heap e Quantum)")
    simular_escalonador(
        bursts=[10, 15, 12, 20, 9, 30, 25, 18, 14, 22],
        quantum=3,
    )

    # ── EXERCÍCIO 2: Árvore Trie ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("[Módulo 2] Árvore Trie (Autocomplete e Autocorreção)")
    print("-" * 60)

    trie = Trie()
    for p in PALAVRAS_PT_100:
        trie.inserir(p)
    print(f" -> {len(PALAVRAS_PT_100)} palavras carregadas com sucesso.")

    print(f" -> Busca Exata ('para'):            {trie.buscar('para')}")
    print(f" -> Busca Inexistente ('carro'):      {trie.buscar('carro')}")
    print(f" -> Autocomplete ('n'):               {trie.autocompletar('n')}")
    print(f" -> Autocomplete ('d'):               {trie.autocompletar('d')}")
    print(f" -> Autocorreção ('nao'):             {trie.autocorrecao('nao')}")
    print(f" -> Autocorreção ('do'):              {trie.autocorrecao('do')}")

    # ── EXERCÍCIO 3: Grafos e Labirinto ───────────────────────────────────────
    print("\n" + "=" * 60)
    print("[Módulo 3] Resolução de Labirinto (Grafos DFS/BFS)")
    print("-" * 60)

    print(" -> Topologia do labirinto carregada com 8 vértices de decisão.")
    caminho_dfs = dfs_caminho(grafo, 0, 7)
    caminho_bfs = bfs_caminho(grafo, 0, 7)

    print(f" -> Caminho via DFS (Pilha/Profundidade):\n    {caminho_dfs}")
    print(f" -> Caminho via BFS (Fila/Fronteira):\n    {caminho_bfs}")
    print(f" -> BFS: {len(caminho_bfs)} passos | DFS: {len(caminho_dfs)} passos")

    print("\n" + "=" * 60)
    print(" FIM DA EXECUÇÃO DOS ALGORITMOS LOCAIS ")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
