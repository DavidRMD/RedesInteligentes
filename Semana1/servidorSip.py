from pjsip.simple import SIPServer

# Configuración del servidor SIP
def iniciar_servidor_sip():
    # Crear una instancia del servidor SIP
    servidor_sip = SIPServer(port=5070)  # Configura el puerto (ajusta si es necesario)

    # Iniciar el servidor
    servidor_sip.start()
    print("Servidor SIP activo en el puerto 5070...")

    # Mantener el servidor en ejecución
    try:
        while True:
            pass  # Agregar lógica adicional si es necesario
    except KeyboardInterrupt:
        print("Deteniendo el servidor...")
        servidor_sip.stop()

if __name__ == "__main__":
    iniciar_servidor_sip()
