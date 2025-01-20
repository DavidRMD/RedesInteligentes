#Cliente
import socket
import time

# Configuración del cliente
CLIENT_IP = "192.168.0.17"  # Nueva IP del cliente
CLIENT_PORT = 5060
SERVER_IP = "192.168.0.16"  # Nueva IP del servidor
SERVER_PORT = 5060
CALL_ID = "123456789@192.168.0.17"
TAG = "98765"
BRANCH = "z9hG4bK-524287-1---xyz"

# Creación del socket UDP
sip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sip_socket.bind((CLIENT_IP, CLIENT_PORT))

# Función para enviar mensajes SIP
def send_sip_message(message):
    print(f"\n📤 Enviando mensaje:\n{message}\n")
    sip_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Función para recibir respuesta SIP
def receive_sip_response():
    response, _ = sip_socket.recvfrom(2048)
    response_decoded = response.decode()
    print(f"\n📥 Respuesta recibida:\n{response_decoded}\n")
    return response_decoded

# **Enviar REGISTER** (Simula registro del usuario en el servidor)
register_message = f"""REGISTER sip:{SERVER_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch={BRANCH}\r\n
From: <sip:user1@{CLIENT_IP}>;tag={TAG}\r\n
To: <sip:user1@{SERVER_IP}>\r\n
Call-ID: {CALL_ID}\r\n
CSeq: 1 REGISTER\r\n
Contact: <sip:user1@{CLIENT_IP}:{CLIENT_PORT}>\r\n
Max-Forwards: 70\r\n
User-Agent: Python-SIP-Client\r\n
Expires: 3600\r\n
Content-Length: 0\r\n\r\n"""

send_sip_message(register_message)
response = receive_sip_response()

# **Enviar INVITE** (Iniciar llamada)
invite_message = f"""INVITE sip:user2@{SERVER_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch={BRANCH}\r\n
From: <sip:user1@{CLIENT_IP}>;tag={TAG}\r\n
To: <sip:user2@{SERVER_IP}>\r\n
Call-ID: {CALL_ID}\r\n
CSeq: 2 INVITE\r\n
Contact: <sip:user1@{CLIENT_IP}:{CLIENT_PORT}>\r\n
Content-Type: application/sdp\r\n
Content-Length: 0\r\n\r\n"""

send_sip_message(invite_message)
response = receive_sip_response()

# **Enviar ACK si el servidor responde con 200 OK**
if "200 OK" in response:
    ack_message = f"""ACK sip:user2@{SERVER_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch={BRANCH}\r\n
From: <sip:user1@{CLIENT_IP}>;tag={TAG}\r\n
To: <sip:user2@{SERVER_IP}>\r\n
Call-ID: {CALL_ID}\r\n
CSeq: 2 ACK\r\n
Contact: <sip:user1@{CLIENT_IP}:{CLIENT_PORT}>\r\n
Content-Length: 0\r\n\r\n"""
    send_sip_message(ack_message)

# **Simulación de una conversación de 10 segundos**
time.sleep(10)

# **Enviar BYE para finalizar la llamada**
bye_message = f"""BYE sip:user2@{SERVER_IP} SIP/2.0\r\n
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch={BRANCH}\r\n
From: <sip:user1@{CLIENT_IP}>;tag={TAG}\r\n
To: <sip:user2@{SERVER_IP}>\r\n
Call-ID: {CALL_ID}\r\n
CSeq: 3 BYE\r\n
Contact: <sip:user1@{CLIENT_IP}:{CLIENT_PORT}>\r\n
Content-Length: 0\r\n\r\n"""

send_sip_message(bye_message)
response = receive_sip_response()

# Cerrar el socket
sip_socket.close()
