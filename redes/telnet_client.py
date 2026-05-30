import socket

host, port = "127.0.0.1", 2323
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print(s.recv(1024).decode())
    s.sendall(b"Comando via Client Script\n")
    print(s.recv(1024).decode())
