import socket
import time

# Configuración del cliente
CLIENTE_IP = "192.168.0.48"
PUERTO_CLIENTE = 5060
SERVIDOR_IP = "192.168.0.49"
PUERTO_SERVIDOR = 5060
ID_LLAMADA = "987654321@192.168.0.48"
IDENTIFICADOR = "54321"
RAMA = "z9hG4bK-123456-1---xyz"

# Crear el socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((CLIENTE_IP, PUERTO_CLIENTE))

# Función para enviar mensajes SIP
def enviar_mensaje_sip(mensaje):
    print(f"\nEnviando mensaje:\n{mensaje}\n")
    udp_socket.sendto(mensaje.encode(), (SERVIDOR_IP, PUERTO_SERVIDOR))

# Función para recibir respuesta SIP
def recibir_respuesta_sip():
    respuesta, _ = udp_socket.recvfrom(2048)
    print(f"\nRespuesta recibida:\n{respuesta.decode()}\n")
    return respuesta.decode()

# Enviar REGISTRO
mensaje_registro = f"""REGISTER sip:{SERVIDOR_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENTE_IP}:{PUERTO_CLIENTE};branch={RAMA}\r\n
From: <sip:labuser@{SERVIDOR_IP}>;tag={IDENTIFICADOR}\r\n
To: <sip:labuser@{SERVIDOR_IP}>\r\n
Call-ID: {ID_LLAMADA}\r\n
CSeq: 1 REGISTER\r\n
Contact: <sip:labuser@{CLIENTE_IP}:{PUERTO_CLIENTE}>\r\n
Content-Length: 0\r\n\r\n"""

enviar_mensaje_sip(mensaje_registro)
respuesta = recibir_respuesta_sip()

# Enviar INVITACION
mensaje_invitacion = f"""INVITE sip:labdest@{SERVIDOR_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENTE_IP}:{PUERTO_CLIENTE};branch={RAMA}\r\n
From: <sip:labuser@{SERVIDOR_IP}>;tag={IDENTIFICADOR}\r\n
To: <sip:labdest@{SERVIDOR_IP}>\r\n
Call-ID: {ID_LLAMADA}\r\n
CSeq: 2 INVITE\r\n
Contact: <sip:labuser@{CLIENTE_IP}:{PUERTO_CLIENTE}>\r\n
Content-Type: application/sdp\r\n
Content-Length: 0\r\n\r\n"""

enviar_mensaje_sip(mensaje_invitacion)
respuesta = recibir_respuesta_sip()

# Enviar CONFIRMACION si el servidor responde con 200 OK
if "200 OK" in respuesta:
    mensaje_confirmacion = f"""ACK sip:labdest@{SERVIDOR_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENTE_IP}:{PUERTO_CLIENTE};branch={RAMA}\r\n
From: <sip:labuser@{SERVIDOR_IP}>;tag={IDENTIFICADOR}\r\n
To: <sip:labdest@{SERVIDOR_IP}>\r\n
Call-ID: {ID_LLAMADA}\r\n
CSeq: 2 ACK\r\n
Contact: <sip:labuser@{CLIENTE_IP}:{PUERTO_CLIENTE}>\r\n
Content-Length: 0\r\n\r\n"""
    enviar_mensaje_sip(mensaje_confirmacion)

# Simular una conversación de 10 segundos
time.sleep(10)

# Enviar FINALIZAR para terminar la llamada
mensaje_finalizar = f"""BYE sip:labdest@{SERVIDOR_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENTE_IP}:{PUERTO_CLIENTE};branch={RAMA}\r\n
From: <sip:labuser@{SERVIDOR_IP}>;tag={IDENTIFICADOR}\r\n
To: <sip:labdest@{SERVIDOR_IP}>\r\n
Call-ID: {ID_LLAMADA}\r\n
CSeq: 3 BYE\r\n
Contact: <sip:labuser@{CLIENTE_IP}:{PUERTO_CLIENTE}>\r\n
Content-Length: 0\r\n\r\n"""

enviar_mensaje_sip(mensaje_finalizar)
respuesta = recibir_respuesta_sip()

# Cerrar el socket
udp_socket.close()
