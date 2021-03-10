import socket
import cv2
import numpy as np
f = open('Python.png','rb')
image_bytes = f.read()
print("Length Client: ", len(image_bytes))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1800       # The port used by the server

# Create a socket which will transfer data.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(image_bytes)
    

