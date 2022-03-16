# serversocket.py

import socket
import hashlib

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
clave = 238758256798463278562457832479856984730

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
            dataString = data.decode("utf-8")
            trozos = dataString.split("\n")
            mensyClave = (str(trozos[0]) + str(clave)).encode("utf-8")
            hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
            if str(hasheo) == str(trozos[1]):
                conn.sendall(b"Transferencia realizada con exito")
            else:
                conn.sendall(b"Ha habido un error de integridad en la transmision, realice de nuevo la transferencia")
