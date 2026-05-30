"""
Questão 5.4 — Análise do servidor Telnet via curl.

Pré-requisito: telnet_server.py em execução.
Uso:          python curl_analise.py [host] [porta]
"""

import subprocess
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 2323

COMANDOS = [
    ("Listar diretório raiz", "ls /"),
    ("Data e hora do sistema", "date"),
    ("Usuário em execução", "whoami"),
    ("Tempo de atividade", "uptime"),
]


def executar_curl_telnet(host: str, port: int, comando: str, timeout: int = 5) -> dict:
    """
    Abre uma conexão Telnet via curl, envia `comando` pelo stdin e captura a
    resposta completa (stdout) e o handshake verbose (stderr).
    """
    resultado = subprocess.run(
        [
            "curl",
            "--verbose",
            "--max-time",
            str(timeout),
            f"telnet://{host}:{port}",
        ],
        input=f"{comando}\n".encode(),
        capture_output=True,
        timeout=timeout + 3,
    )
    return {
        "stdout": resultado.stdout.decode(errors="replace"),
        "stderr": resultado.stderr.decode(errors="replace"),
        "returncode": resultado.returncode,
    }


def exibir_resultado(rotulo: str, resultado: dict) -> None:
    print(f"\n{'=' * 60}")
    print(f"  Teste : {rotulo}")
    print("=" * 60)
    if resultado["stderr"]:
        print("[Handshake / Verbose curl]")
        print(resultado["stderr"].strip())
    print("\n[Resposta do servidor]")
    print(resultado["stdout"].strip() or "(sem saída)")
    print(f"\n[Código de saída curl]: {resultado['returncode']}")


def main(host: str, port: int) -> None:
    print("=" * 60)
    print("  Análise Telnet via curl")
    print("=" * 60)
    print(f"  Alvo : telnet://{host}:{port}")
    print("  Nota : certifique-se de que telnet_server.py está rodando.\n")

    for rotulo, cmd in COMANDOS:
        try:
            resultado = executar_curl_telnet(host, port, cmd)
            exibir_resultado(rotulo, resultado)
        except subprocess.TimeoutExpired:
            print(f"\n[TIMEOUT] Sem resposta para o comando '{cmd}'.")
        except FileNotFoundError:
            print("\n[ERRO] curl não encontrado. Instale com: sudo apt install curl")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("  Análise concluída.")
    print("=" * 60)


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    main(host, port)
