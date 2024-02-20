import socket
import threading

# Lista para llevar un registro de los sockets de clientes conectados
clientes = []

# Función para manejar las conexiones de clientes
def handle_client(client_socket, client_address):
    print("Estableciste conexión con el cliente")

    while True:
        # Recibir mensaje del cliente
        try:
            mensaje = client_socket.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"[{client_address[0]}:{client_address[1]}] {mensaje}")

            # Enviar el mensaje a todos los clientes conectados
            for c in clientes: 
                if c != client_socket:  # Evitar enviar el mensaje al cliente que lo envió
                    c.send(f"[{client_address[0]}:{client_address[1]}] {mensaje}".encode("utf-8"))
        except ConnectionResetError:
            break

    # Cuando un cliente se desconecta, cerrar el socket y eliminarlo de la lista
    print(f"[INFO] {client_address} se ha desconectado")
    clientes.remove(client_socket)
    client_socket.close()


# Configuración del servidor #Aqui se pone la ip del servidor
host = ""
puerto = 8080

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, puerto))

# Iniciar el servidor
try:
    server_socket.listen(5)  # Escuchar conexiones entrantes, hasta 5 clientes en espera
    print(f"[INFO] Servidor escuchando en {host}:{puerto}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[INFO] Nueva conexión de {client_address}")
        clientes.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except Exception as e:
    print(f"[ERROR] Error en el bucle principal del servidor: {e}")

