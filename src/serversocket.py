# serversocket.py

import socket
import funciones


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
clave = "472D4B6150645367566B5970337336763979244226452948404D625165546857"
claveMal = 2387582567984632785624578324798

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    funciones.comprobarContador()
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
                funciones.actualizarContador()
                funciones.enviarConfimación(conn, clave)
            else:
                funciones.actualizarContador()
                funciones.enviarNegativa(conn, clave)
            
            print(f"Received {data!r}")