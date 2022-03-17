# clientsocket.py

import socket
import time
from src import funciones
from datetime import datetime


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server
clave = 238758256798463278562457832479856984730

i = input("Pon tu mensaje aqui: ")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        #Codificar el mensaje con lo que mandamos y la clave simetrica
        mensByte = funciones.codificarMensaje(i, clave)
        s.sendall(mensByte)
        data = s.recv(1024)
        if not data:
            break
        mens = funciones.decodificarMensaje(data)
        if funciones.comprobarIntegridad(mens, clave) and mens[0] == "Transferencia realizada con exito":
            print("Cerrando conexión")
            time.sleep(2)
            break
        elif funciones.comprobarIntegridad(mens, clave) and mens[0] == "Se ha producido un error de integridad, vuelva a realizar la transferencia":
            print("Aqui hay que repetir el mensaje")
            time.sleep(2)
            #enviarMensaje()
        elif not(funciones.comprobarIntegridad(mens, clave)):
            print("Aqui hay que pedirle la confirmación otra vez al server")
            time.sleep(2)
            break
        
        
    

print(f"Received {data!r}")