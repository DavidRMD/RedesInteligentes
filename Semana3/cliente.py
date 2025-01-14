import socket
import time
import csv

# Configuración del cliente
IP_OBJETIVO = "192.168.0.50"  # Dirección IP del servidor
PUERTO_OBJETIVO = 5080        # Puerto del servidor
TAMANIO_BUFFER = 1024         # Tamaño del buffer

# Crear socket UDP
cliente_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Inicializar métricas
latencias = []
total_bytes = 0
mensajes_totales = 50

# Medir throughput
tiempo_inicio = time.time()

for num in range(mensajes_totales):
    contenido_mensaje = f"Mensaje-{num + 1}" + "-" * 1000
    total_bytes += len(contenido_mensaje.encode())
    inicio_mensaje = time.time()

    # Enviar mensaje al servidor
    cliente_udp.sendto(contenido_mensaje.encode(), (IP_OBJETIVO, PUERTO_OBJETIVO))

    # Recibir respuesta
    respuesta, _ = cliente_udp.recvfrom(TAMANIO_BUFFER)
    fin_mensaje = time.time()

    # Calcular latencia
    tiempo_respuesta = (fin_mensaje - inicio_mensaje) * 1000
    latencias.append({"Mensaje": num + 1, "Latencia (ms)": tiempo_respuesta})
    print(f"Respuesta recibida: {respuesta.decode()} | Latencia: {tiempo_respuesta:.2f} ms")

# Calcular throughput
tiempo_total = time.time() - tiempo_inicio
rendimiento = (total_bytes / tiempo_total) / 1024
print(f"\nThroughput total: {rendimiento:.2f} KB/s")

# Guardar resultados en CSV
with open("metricas_red.csv", "w", newline="") as archivo_csv:
    campos = ["Mensaje", "Latencia (ms)"]
    escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(latencias)

print("\nResultados exportados a 'metricas_red.csv'.")
cliente_udp.close()

