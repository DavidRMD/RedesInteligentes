### Código del Cliente
import socket

# Configuración del cliente
SERVER_IP = "127.0.0.1"  # Localhost para pruebas en la misma máquina
SERVER_PORT = 5070
BUFFER_SIZE = 1024

# Crear socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar mensajes al servidor en un bucle infinito
mensaje_numero = 1
try:
    while True:
        mensaje = f"Mensaje {mensaje_numero}"
        client_socket.sendto(mensaje.encode(), (SERVER_IP, SERVER_PORT))
        print(f"Mensaje enviado: {mensaje}")

        # Recibir respuesta del servidor
        data, addr = client_socket.recvfrom(BUFFER_SIZE)
        print(f"Respuesta del servidor: {data.decode()}")

        mensaje_numero += 1
except KeyboardInterrupt:
    print("\nCliente detenido por el usuario.")
    client_socket.close()
