import socket

# Configuración del servidor
IP_SERVIDOR = "192.168.0.50"  # Dirección IP del servidor
PUERTO_SERVIDOR = 5080        # Puerto UDP
TAMANIO_BUFFER = 1024         # Tamaño del buffer

# Crear socket UDP
servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind((IP_SERVIDOR, PUERTO_SERVIDOR))
print(f"Servidor UDP corriendo en {IP_SERVIDOR}:{PUERTO_SERVIDOR}")

# Escuchar mensajes entrantes
while True:
    mensaje, direccion = servidor_udp.recvfrom(TAMANIO_BUFFER)
    print(f"Mensaje recibido de {direccion}: {mensaje.decode()}")

    # Responder al cliente
    respuesta = "Respuesta: " + mensaje.decode()
    servidor_udp.sendto(respuesta.encode(), direccion)
