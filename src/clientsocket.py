# clientsocket.py

import socket
import hmac
import hashlib

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server
key = "caca"
msg = "hola servidor"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    hmac1 = hmac.digest(key=key.encode(), msg=msg.encode(), digest="sha3_256")

    s.sendall((msg + "\n" + str(hmac1)).encode("utf-8"))
    
    data = s.recv(1024)


print(f"Sent {data!r}")
