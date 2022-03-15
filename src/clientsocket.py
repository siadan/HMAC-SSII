# clientsocket.py

import socket
import hashlib

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server
clave = 238758256798463278562457832479856984730
i = input("Pon tu mensaje aquí: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    mensyClave = (i+str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    print(hasheo)
    mensajeConc = i + "\n" + str(hasheo)
    mensByte = mensajeConc.encode("utf-8")
    s.sendall(mensByte)
    data = s.recv(1024)

print(f"Received {data!r}")
