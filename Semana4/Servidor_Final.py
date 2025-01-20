#--Servidor--
import socket
import random

# Configuración del servidor SIP
SERVER_IP = "192.168.0.49"
SERVER_PORT = 5070

# Simulación de red
PACKET_LOSS_PROBABILITY = 0.05  # 5% de pérdida de paquetes
LATENCY_MIN = 10  # ms
LATENCY_MAX = 100  # ms

# Mensajes SIP
SIP_MESSAGES = {
    "INVITE": "INVITE sip:lab1 SIP/2.0",
    "200_OK": "SIP/2.0 200 OK",
    "ACK": "ACK sip:lab1 SIP/2.0",
    "BYE": "BYE sip:lab1 SIP/2.0",
}

def simulate_packet_loss():
    """Simula la pérdida de paquetes según una probabilidad definida."""
    return random.random() < PACKET_LOSS_PROBABILITY

def start_server():
    """Inicia el servidor SIP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        print(f"[Servidor] Escuchando en {SERVER_IP}:{SERVER_PORT}")

        while True:
            data, addr = server.recvfrom(1024)
            message = data.decode()
            print(f"[Servidor] Mensaje recibido de {addr}: {message}")

            if simulate_packet_loss():
                print("[Servidor] Simulando pérdida de paquete...")
                continue

            # Simular latencia de red
            latency = random.uniform(LATENCY_MIN, LATENCY_MAX) / 1000  # Convertir a segundos
            time.sleep(latency)

            if message == SIP_MESSAGES["INVITE"]:
                print("[Servidor] Respondiendo con 200 OK...")
                server.sendto(SIP_MESSAGES["200_OK"].encode(), addr)
            elif message == SIP_MESSAGES["ACK"]:
                print("[Servidor] Recibido ACK, conexión establecida.")
            elif message == SIP_MESSAGES["BYE"]:
                print("[Servidor] Recibido BYE, cerrando la conexión...")
                server.sendto(SIP_MESSAGES["200_OK"].encode(), addr)
                print("[Servidor] Conexión cerrada.")
                break

if __name__ == "__main__":
    start_server()
