import time
import random


class MinHeap:
    def __init__(self):
        self.heap: list[dict] = []

    def inserir(self, processo: dict) -> None:
        self.heap.append(processo)
        self._subir(len(self.heap) - 1)

    def extrair_minimo(self) -> dict | None:
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        raiz = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._descer(0)
        return raiz

    def _subir(self, indice: int) -> None:
        pai = (indice - 1) // 2
        if indice > 0 and self.heap[indice]["burst"] < self.heap[pai]["burst"]:
            self.heap[indice], self.heap[pai] = self.heap[pai], self.heap[indice]
            self._subir(pai)

    def _descer(self, indice: int) -> None:
        menor = indice
        esq = 2 * indice + 1
        dir_ = 2 * indice + 2

        if esq < len(self.heap) and self.heap[esq]["burst"] < self.heap[menor]["burst"]:
            menor = esq
        if (
            dir_ < len(self.heap)
            and self.heap[dir_]["burst"] < self.heap[menor]["burst"]
        ):
            menor = dir_

        if menor != indice:
            self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
            self._descer(menor)

    def vazia(self) -> bool:
        return len(self.heap) == 0


def simular_escalonador(bursts: list[int], quantum: int) -> None:
    fila_pronta: MinHeap = MinHeap()
    fila_suspensa: list[dict] = []

    print(f"{'PID':<5} | {'Estado':<12} | {'Burst Restante'}")
    print("-" * 35)

    # Nova → Pronta (carregamento na memória)
    for i, burst in enumerate(bursts):
        p = {"id": i + 1, "burst": burst, "estado": "Nova"}
        print(f"P{p['id']:<4} | {'Nova':<12} | {p['burst']}")
        p["estado"] = "Pronta"
        fila_pronta.inserir(p)
        print(f"P{p['id']:<4} | {'Pronta':<12} | {p['burst']}")

    while not fila_pronta.vazia() or fila_suspensa:
        # Libera processos suspensos aleatoriamente (I/O concluído)
        if fila_suspensa and random.random() > 0.5:
            p_liberado = fila_suspensa.pop(0)
            p_liberado["estado"] = "Pronta"
            fila_pronta.inserir(p_liberado)
            print(f"P{p_liberado['id']:<4} | {'Pronta':<12} | {p_liberado['burst']}")

        if fila_pronta.vazia():
            time.sleep(0.1)
            continue

        p = fila_pronta.extrair_minimo()
        p["estado"] = "Executando"
        print(f"P{p['id']:<4} | {'Executando':<12} | {p['burst']}")

        tempo_execucao = min(quantum, p["burst"])
        time.sleep(0.1)  # Temporização de CPU
        p["burst"] -= tempo_execucao

        if p["burst"] > 0:
            if random.random() < 0.2:
                p["estado"] = "Suspensa"
                fila_suspensa.append(p)
                print(f"P{p['id']:<4} | {'Suspensa':<12} | {p['burst']}")
            else:
                p["estado"] = "Pronta"
                fila_pronta.inserir(p)
                print(f"P{p['id']:<4} | {'Pronta':<12} | {p['burst']}")
        else:
            p["estado"] = "Terminada"
            print(f"P{p['id']:<4} | {'Terminada':<12} | 0")


if __name__ == "__main__":
    # quantum=3 garante mínimo de 3 ocupações da CPU para o menor burst (9 ÷ 3 = 3)
    simular_escalonador(
        bursts=[10, 15, 12, 20, 9, 30, 25, 18, 14, 22],
        quantum=3,
    )
