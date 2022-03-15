# serversocket.py

import socket
import hmac

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
key = "caca"

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
            received = data.decode("utf-8").split("\n")
            msg = received[0]
            digest = received[1]
            hmac1 = hmac.digest(key=key.encode(), msg=msg.encode(), digest="sha3_256")
            if hmac.compare_digest(str(hmac1), digest):
                print("No ha habido fallos en la integridad")
            else:
                print("Ha habido fallos en la integridad")
            print(f"Received {msg!r}")
            conn.sendall(data)
