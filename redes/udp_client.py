import socket

host, port = "127.0.0.1", 65433
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Ola Servidor UDP!", (host, port))
    data, addr = s.recvfrom(1024)
print(f"Resposta do servidor: {data.decode()}")
