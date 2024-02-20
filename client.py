import socket
import threading

# Función que maneja los mensajes recibidos por el servidor.
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("El servidor se ha desconectado")
            break

# Configuración del cliente.
host = "127.0.0.1"
port = 8080

# Conexión que se realiza al servidor.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Hilo que maneja los mensajes recibidos por el servidor.
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Bucle principal del cliente.
try:
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\n[INFO] Cliente desconectado")
    client_socket.close()
    exit(0)
