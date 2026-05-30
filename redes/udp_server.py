import socket

HOST = "0.0.0.0"  
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Servidor UDP operando em {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(1024)
        print(f"Mensagem de {addr}: {data.decode()}")
        s.sendto(b"ACK: " + data, addr)
