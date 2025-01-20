#--Cliente--
import socket
import time
import pandas as pd
import matplotlib.pyplot as plt

# Configuración del cliente SIP
CLIENT_IP = "192.168.0.48"
CLIENT_PORT = 5060
SERVER_IP = "192.168.0.49"
SERVER_PORT = 5070

# Mensajes SIP
SIP_MESSAGES = {
    "INVITE": "INVITE sip:lab1 SIP/2.0",
    "200_OK": "SIP/2.0 200 OK",
    "ACK": "ACK sip:lab1 SIP/2.0",
    "BYE": "BYE sip:lab1 SIP/2.0",
}

# Configuración de la prueba
NUM_MESSAGES = 500
latencias = []
lost_messages = 0

def send_message(client, message, expect_response=True):
    """Envía un mensaje SIP y mide la latencia si se espera respuesta."""
    global lost_messages

    start_time = time.time()
    client.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    if not expect_response:
        return
   
    try:
        client.settimeout(1)  # Espera máxima de 1 segundo
        data, _ = client.recvfrom(1024)
        end_time = time.time()
        latencias.append((end_time - start_time) * 1000)  # Latencia en ms
        print(f"[Cliente] Respuesta recibida: {data.decode()}")
    except socket.timeout:
        print("[Cliente] Paquete perdido.")
        lost_messages += 1

def generate_results():
    """Genera la tabla de resultados y gráficos."""
    avg_latency = sum(latencias) / len(latencias) if latencias else 0
    packet_loss = (lost_messages / NUM_MESSAGES) * 100

    df = pd.DataFrame({
        "Mensaje": list(range(1, len(latencias) + 1)),
        "Latencia (ms)": latencias
    })
    df.to_csv("resultados_final.csv", index=False)

    print(f"\n--- Resultados ---")
    print(f"Latencia promedio: {avg_latency:.2f} ms")
    print(f"Pérdida de paquetes: {packet_loss:.2f}%")

    # Gráficos
    plt.figure(figsize=(10, 5))
    plt.plot(df["Mensaje"], df["Latencia (ms)"], marker='o', linestyle='-', color='b')
    plt.axhline(y=avg_latency, color='r', linestyle='--', label=f"Promedio: {avg_latency:.2f} ms")
    plt.xlabel("Número de Mensaje")
    plt.ylabel("Latencia (ms)")
    plt.title("Latencia por Mensaje en la Simulación Final")
    plt.legend()
    plt.grid()
    plt.savefig("latencia_final.png")
    plt.show()

    plt.figure(figsize=(6, 5))
    plt.bar(["Mensajes Enviados", "Mensajes Perdidos"], [NUM_MESSAGES, lost_messages], color=["blue", "red"])
    plt.title("Pérdida de Paquetes en la Simulación Final")
    plt.ylabel("Cantidad de Mensajes")
    plt.savefig("perdida_final.png")
    plt.show()

def start_client():
    """Ejecuta la simulación SIP final."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.bind((CLIENT_IP, CLIENT_PORT))
        print(f"[Cliente] Conectando desde {CLIENT_IP}:{CLIENT_PORT} a {SERVER_IP}:{SERVER_PORT}")

        for i in range(NUM_MESSAGES):
            send_message(client, SIP_MESSAGES["INVITE"])

        send_message(client, SIP_MESSAGES["ACK"], expect_response=False)
        time.sleep(2)
        send_message(client, SIP_MESSAGES["BYE"])

        generate_results()

if __name__ == "__main__":
    start_client()

#Tablacliente:
import pandas as pd
from tabulate import tabulate

# Cargar los datos de la simulación final
df = pd.read_csv("resultados_final.csv")
avg_latency = df["Latencia (ms)"].mean()

# Valores simulados de throughput
throughput_simulado = 50  # Suposición de throughput en Mbps

# Datos de comparación
data = {
    "Métrica": ["Latencia (ms)", "Throughput (Mbps)"],
    "LTE": ["20-50 ms", "100 Mbps - 1 Gbps"],
    "5G": ["1-10 ms", "Hasta 10 Gbps"],
    "Simulación Final": [f"{avg_latency:.2f} ms", f"{throughput_simulado:.2f} Mbps"]
}

# Crear tabla y mostrar
df_comparativa = pd.DataFrame(data)
print("Tabla comparativa final:")
print(tabulate(df_comparativa, headers="keys", tablefmt="grid"))

# Exportar la tabla a CSV
df_comparativa.to_csv("tabla_comparativa_final.csv", index=False)
