#Servidor:
import socket
import random
import time

# Configuración del servidor
SERVER_IP = "192.168.0.49"  # IP del servidor
SERVER_PORT = 5070          # Puerto del servidor
BUFFER_SIZE = 1024          # Tamaño del buffer

# Simulación de latencia en la red
MIN_LATENCY = 10   # ms
MAX_LATENCY = 100  # ms
PACKET_LOSS_RATE = 0.05  # Probabilidad de pérdida de paquetes (5%)

# Crear socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"🟢 Servidor UDP (Simulación NS-3) activo en {SERVER_IP}:{SERVER_PORT}")

while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    received_time = time.time()

    # Simular pérdida de paquetes
    if random.random() < PACKET_LOSS_RATE:
        print(f"❌ Paquete de {addr} perdido")
        continue  # No responde al cliente

    # Simular latencia de red
    latency = random.uniform(MIN_LATENCY, MAX_LATENCY) / 1000  # Convertir a segundos
    time.sleep(latency)

    print(f"📥 Mensaje recibido de {addr}: {data.decode()} | Latencia simulada: {latency*1000:.2f} ms")

    # Enviar respuesta al cliente
    response = "ACK: " + data.decode()
    server_socket.sendto(response.encode(), addr)
