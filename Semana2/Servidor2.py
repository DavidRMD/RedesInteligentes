#servidor
import socket

# Configuración del servidor SIP
SERVER_IP = "192.168.0.16"  # Nueva IP del servidor
SERVER_PORT = 5060

# Crear socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"🟢 Servidor SIP iniciado en {SERVER_IP}:{SERVER_PORT}")

while True:
    data, addr = server_socket.recvfrom(2048)  # Recibir mensajes
    message = data.decode()
    print(f"\n📥 Mensaje recibido de {addr}:\n{message}")

    if "REGISTER" in message:
        response = "SIP/2.0 200 OK\r\nContent-Length: 0\r\n\r\n"
        server_socket.sendto(response.encode(), addr)
        print(f"📤 Enviando: {response.strip()}")

    elif "INVITE" in message:
        response = "SIP/2.0 100 Trying\r\nContent-Length: 0\r\n\r\n"
        server_socket.sendto(response.encode(), addr)
        print(f"📤 Enviando: {response.strip()}")

        response = "SIP/2.0 180 Ringing\r\nContent-Length: 0\r\n\r\n"
        server_socket.sendto(response.encode(), addr)
        print(f"📤 Enviando: {response.strip()}")

        response = "SIP/2.0 200 OK\r\nContent-Length: 0\r\n\r\n"
        server_socket.sendto(response.encode(), addr)
        print(f"📤 Enviando: {response.strip()}")

    elif "ACK" in message:
        print("✅ Llamada establecida correctamente.")

    elif "BYE" in message:
        response = "SIP/2.0 200 OK\r\nContent-Length: 0\r\n\r\n"
        server_socket.sendto(response.encode(), addr)
        print(f"📤 Enviando: {response.strip()} - Llamada terminada.")
