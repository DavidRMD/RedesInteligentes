#Cliente:
import socket
import time
import csv
import random

# Configuración del cliente
CLIENT_IP = "192.168.0.19"  # IP del cliente
SERVER_IP = "192.168.0.49"  # IP del servidor
SERVER_PORT = 5070          # Puerto del servidor
BUFFER_SIZE = 1024          # Tamaño del buffer

# Simulación de tráfico de red variable
MIN_INTERVAL = 0.05  # Intervalo mínimo entre paquetes (50ms)
MAX_INTERVAL = 0.5   # Intervalo máximo entre paquetes (500ms)
NUM_MESSAGES = 50     # Número total de mensajes

# Crear socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variables para métricas
results = []  # Lista de latencias por mensaje
total_bytes = 0
lost_packets = 0

# Tiempo inicial para throughput
start_time = time.time()

for i in range(NUM_MESSAGES):
    # Crear mensaje de prueba (~1 KB)
    message = f"Mensaje {i+1} " + "-" * 1000
    total_bytes += len(message.encode())
    message_start_time = time.time()

    # Enviar mensaje
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Simular tráfico de red aleatorio
    time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

    try:
        # Configurar timeout para pérdida de paquetes
        client_socket.settimeout(0.2)  # Espera hasta 200 ms
        data, addr = client_socket.recvfrom(BUFFER_SIZE)
        message_end_time = time.time()

        # Calcular latencia
        latency = (message_end_time - message_start_time) * 1000  # Convertir a ms
        results.append({"Mensaje": i+1, "Latencia (ms)": latency})

        print(f"📥 Respuesta del servidor: {data.decode()} | Latencia: {latency:.2f} ms")

    except socket.timeout:
        print(f"❌ Paquete {i+1} perdido (Timeout)")
        lost_packets += 1

# Tiempo final para throughput
end_time = time.time()

# Calcular throughput
elapsed_time = end_time - start_time
throughput = (total_bytes / elapsed_time) / 1024  # KB/s
packet_loss_percentage = (lost_packets / NUM_MESSAGES) * 100

print(f"\n📊 Métricas de Red Simuladas:")
print(f"🔹 Throughput total: {throughput:.2f} KB/s")
print(f"🔹 Pérdida de paquetes: {packet_loss_percentage:.2f}%")

# Guardar resultados en un archivo CSV
with open("resultados_ns3.csv", "w", newline="") as csvfile:
    fieldnames = ["Mensaje", "Latencia (ms)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

print("\n✅ Resultados exportados a 'resultados_ns3.csv'.")
client_socket.close()
