### Código del Servidor
import socket

# Configuración del servidor
SERVER_IP = "127.0.0.1"  # Localhost para pruebas en la misma máquina
SERVER_PORT = 5070
BUFFER_SIZE = 1024

# Crear socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Servidor ejecutándose en {SERVER_IP}:{SERVER_PORT}")

# Escuchar mensajes del cliente
while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Mensaje recibido de {addr}: {data.decode()}")

    # Responder al cliente
    response = "ACK: " + data.decode()
    server_socket.sendto(response.encode(), addr)
