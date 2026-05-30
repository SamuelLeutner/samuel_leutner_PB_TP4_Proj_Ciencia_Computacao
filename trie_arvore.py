PALAVRAS_PT_100: list[str] = [
    "que",
    "não",
    "de",
    "a",
    "o",
    "e",
    "é",
    "do",
    "da",
    "em",
    "um",
    "para",
    "com",
    "uma",
    "os",
    "no",
    "se",
    "na",
    "por",
    "mais",
    "as",
    "dos",
    "como",
    "mas",
    "ao",
    "ele",
    "das",
    "à",
    "seu",
    "sua",
    "ou",
    "quando",
    "muito",
    "nos",
    "já",
    "eu",
    "também",
    "só",
    "pelo",
    "pela",
    "até",
    "isso",
    "ela",
    "entre",
    "depois",
    "sem",
    "mesmo",
    "aos",
    "seus",
    "quem",
    "nas",
    "me",
    "esse",
    "eles",
    "você",
    "essa",
    "num",
    "nem",
    "suas",
    "meu",
    "às",
    "minha",
    "numa",
    "pelos",
    "elas",
    "qual",
    "nós",
    "lhe",
    "deles",
    "essas",
    "esses",
    "pelas",
    "este",
    "dele",
    "tu",
    "te",
    "vocês",
    "vos",
    "lhes",
    "meus",
    "minhas",
    "teu",
    "tua",
    "teus",
    "tuas",
    "nosso",
    "nossa",
    "nossos",
    "nossas",
    "vosso",
    "vossa",
    "vossos",
    "vossas",
    "dela",
    "delas",
    "esta",
    "estes",
    "estas",
    "aquele",
    "aquela",
]


class TrieNode:
    def __init__(self):
        self.filhos: dict[str, "TrieNode"] = {}
        self.fim_palavra: bool = False


class Trie:
    def __init__(self):
        self.raiz = TrieNode()

    def inserir(self, palavra: str) -> None:
        no = self.raiz
        for char in palavra:
            if char not in no.filhos:
                no.filhos[char] = TrieNode()
            no = no.filhos[char]
        no.fim_palavra = True

    def buscar(self, palavra: str) -> bool:
        no = self._encontrar_no(palavra)
        return no is not None and no.fim_palavra

    def remover(self, palavra: str) -> None:
        def _remover_recursivo(no: TrieNode, palavra: str, profundidade: int) -> bool:
            if profundidade == len(palavra):
                if not no.fim_palavra:
                    return False
                no.fim_palavra = False
                return len(no.filhos) == 0

            char = palavra[profundidade]
            if char not in no.filhos:
                return False

            pode_deletar = _remover_recursivo(
                no.filhos[char], palavra, profundidade + 1
            )
            if pode_deletar:
                del no.filhos[char]
                return len(no.filhos) == 0 and not no.fim_palavra
            return False

        _remover_recursivo(self.raiz, palavra, 0)

    def listar(self) -> list[str]:
        return self.autocompletar("")

    def autocompletar(self, prefixo: str) -> list[str]:
        no = self._encontrar_no(prefixo)
        if not no:
            return []
        resultados: list[str] = []
        self._dfs(no, prefixo, resultados)
        return resultados

    def autocorrecao(self, palavra: str, max_erros: int = 1) -> list[str]:
        resultados: list[str] = []
        linha_atual = range(len(palavra) + 1)
        for char in self.raiz.filhos:
            self._buscar_tolerancia(
                self.raiz.filhos[char],
                char,
                palavra,
                linha_atual,
                resultados,
                max_erros,
            )
        return resultados


    def _encontrar_no(self, prefixo: str) -> TrieNode | None:
        no = self.raiz
        for char in prefixo:
            if char not in no.filhos:
                return None
            no = no.filhos[char]
        return no

    def _dfs(self, no: TrieNode, caminho_atual: str, resultados: list[str]) -> None:
        if no.fim_palavra:
            resultados.append(caminho_atual)
        for char, filho in no.filhos.items():
            self._dfs(filho, caminho_atual + char, resultados)

    def _buscar_tolerancia(
        self,
        no: TrieNode,
        char: str,
        palavra: str,
        linha_anterior: range,
        resultados: list[str],
        max_erros: int,
    ) -> None:
        colunas = len(palavra) + 1
        linha_atual = [linha_anterior[0] + 1]

        for c in range(1, colunas):
            custo = 0 if palavra[c - 1] == char[-1] else 1
            linha_atual.append(
                min(
                    linha_atual[c - 1] + 1,
                    linha_anterior[c] + 1,
                    linha_anterior[c - 1] + custo,
                )
            )

        if linha_atual[-1] <= max_erros and no.fim_palavra:
            resultados.append(char)

        if min(linha_atual) <= max_erros:
            for prox_char in no.filhos:
                self._buscar_tolerancia(
                    no.filhos[prox_char],
                    char + prox_char,
                    palavra,
                    linha_atual,
                    resultados,
                    max_erros,
                )


if __name__ == "__main__":
    trie = Trie()
    for p in PALAVRAS_PT_100:
        trie.inserir(p)

    print("Autocomplete 'n':", trie.autocompletar("n"))
    print("Autocorreção 'nao':", trie.autocorrecao("nao"))
