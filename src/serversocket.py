# serversocket.py

import socket
from src import funciones
from datetime import datetime

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
clave = 238758256798463278562457832479856984730
claveMal = 2387582567984632785624578324798
global fechaIni
global diccPalSeed
diccPalSed = funciones.sacarPalabrasDelDiccionario("./diccionario/diccionarioPalabras.txt")
with open("./configuracion/config.txt", "r") as f:
    global fechaIni
    fechaIni = datetime.strptime(f.readline(), "%d-%m-%Y")
fechaHoy = datetime.today()
indiceSEED = (fechaHoy-fechaIni).days


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mens = funciones.decodificarMensaje(data)
            if funciones.comprobarIntegridad(mens, clave):
                funciones.enviarConfimación(conn, claveMal)
            else:
                funciones.enviarNegativa(conn, clave)
            
            print(f"Received {data!r}")