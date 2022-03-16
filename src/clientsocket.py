# clientsocket.py

import socket
from src import funciones


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server
clave = 238758256798463278562457832479856984730
i = input("Pon tu mensaje aqui: ")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #Codificar el mensaje con lo que mandamos y la clave simetrica
    mensByte = funciones.codificarMensaje(i, clave)
    s.sendall(mensByte)
    data = s.recv(1024)

print(f"Received {data!r}")