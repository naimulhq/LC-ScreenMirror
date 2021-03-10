import socket
import cv2
import numpy as np

# Create a socket that will recieve data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = "127.0.0.1"
    port = 1800
    s.bind((host,port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = b''
        while True:
            part = conn.recv(40000,socket.MSG_WAITALL)
            break

print("Bytes in Server: ", len(part))
decoded = cv2.imdecode(np.frombuffer(part, np.uint8), -1)
cv2.imwrite('PythonTest2.png',decoded)
