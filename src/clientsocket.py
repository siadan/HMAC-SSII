# clientsocket.py

import socket
import time
from src import funciones


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server
clave = "472D4B6150645367566B5970337336763979244226452948404D625165546857"

origen = input("Introduzca la cuenta de origen: ")
destino = input("Introduzca la cuenta de destino: ")
cantidad = input("Introduzca la cantidad que quiere transferir: ")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        #Codificar el mensaje con lo que mandamos y la clave simetrica
        mensCompleto = origen + "," + destino + "," + cantidad
        funciones.actualizarContador()
        mensByte = funciones.codificarMensaje(mensCompleto, clave)
        s.sendall(mensByte)
        data = s.recv(1024)
        if not data:
            break
        mens = funciones.decodificarMensaje(data)
        if funciones.comprobarIntegridad(mens, clave) and mens[0] == "Transferencia realizada con exito":
            print("Transferencia realizada con exito")
            time.sleep(1)
            print("Cerrando conexión")
            time.sleep(2)
            break
        elif funciones.comprobarIntegridad(mens, clave) and mens[0] == "Se ha producido un error de integridad, vuelva a realizar la transferencia":
            print("Se ha producido un error de integridad, vuelva a realizar la transferencia")
            time.sleep(1)
            print("Cerrando conexión")
            time.sleep(2)
            break
        elif not(funciones.comprobarIntegridad(mens, clave)):
            print("Ha habido un error de integridad en la respuesta, consulte con el servidor si la transacción se ha realizado correctamente.")
            time.sleep(1)
            print("Cerrando conexión")
            time.sleep(2)
            break