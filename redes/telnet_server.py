import socket
import threading
import subprocess


def gerenciar_cliente_telnet(conn, addr):
    conn.send(b"--- Servidor Telnet OS Ativo ---\n")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            comando = data.decode("utf-8").strip()

            if not comando:
                continue

            # Executa o comando no SO e captura a saída
            processo = subprocess.run(
                comando, shell=True, capture_output=True, text=True
            )

            # Pega o stdout (sucesso) ou stderr (erro)
            saida = processo.stdout if processo.stdout else processo.stderr
            if not saida:
                saida = "Comando executado sem retorno visual.\n"

            conn.send(saida.encode("utf-8"))
        except ConnectionResetError:
            print(f"Cliente {addr} desconectado abruptamente.")
            break
        except Exception as e:
            conn.send(f"Erro no servidor: {e}\n".encode("utf-8"))
            break
    conn.close()

host, port = "0.0.0.0", 2323
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Servidor Telnet escutando em {host}:{port}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=gerenciar_cliente_telnet, args=(conn, addr)).start()
