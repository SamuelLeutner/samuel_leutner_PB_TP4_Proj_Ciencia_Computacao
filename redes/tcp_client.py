import socket

host, port = "127.0.0.1", 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b"Ola Servidor TCP!")
    data = s.recv(1024)
print(f"Recebido do servidor: {data.decode()}")
