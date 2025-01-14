import socket
import time

# Configuración del cliente
IP_SERVIDOR = "192.168.0.49"  # Cambia a la IP del servidor
PUERTO_SERVIDOR = 5070        # Debe coincidir con el puerto del servidor

# Crear el socket
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Crear el mensaje SOLICITUD
solicitud = (
    "REQUEST sip:lab2@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK999xyz\r\n"
    "Content-Length: 0\r\n\r\n"
).format(IP_SERVIDOR, PUERTO_SERVIDOR)

# Enviar SOLICITUD
print(f"Enviando solicitud al servidor {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")
socket_cliente.sendto(solicitud.encode(), (IP_SERVIDOR, PUERTO_SERVIDOR))

# Esperar respuesta CONFIRMACIÓN
respuesta_servidor, _ = socket_cliente.recvfrom(1024)
print("Respuesta del servidor a la solicitud:")
print(respuesta_servidor.decode())

# Enviar CONFIRMAR
confirmar = (
    "CONFIRM sip:lab2@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK999xyz\r\n"
    "Content-Length: 0\r\n\r\n"
).format(IP_SERVIDOR, PUERTO_SERVIDOR)
print("Enviando confirmación...")
socket_cliente.sendto(confirmar.encode(), (IP_SERVIDOR, PUERTO_SERVIDOR))

# Simular duración de la sesión
time.sleep(5)

# Enviar TERMINAR
terminar = (
    "TERMINATE sip:lab2@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK999xyz\r\n"
    "Content-Length: 0\r\n\r\n"
).format(IP_SERVIDOR, PUERTO_SERVIDOR)
print("Enviando terminación...")
socket_cliente.sendto(terminar.encode(), (IP_SERVIDOR, PUERTO_SERVIDOR))

# Esperar respuesta CONFIRMACIÓN FINAL
respuesta_final, _ = socket_cliente.recvfrom(1024)
print("Respuesta del servidor a la terminación:")
print(respuesta_final.decode())

socket_cliente.close()
