import socket
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

# Create a socket that will recieve data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = "192.168.1.120"
    port = 1800
    s.bind((host,port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = b''
        while True:
            part = conn.recv(6220962,socket.MSG_WAITALL)
            part = pickle.loads(part)
            conn.send(bytes("Recieved","utf-8"))
            cv2.imshow('frame',part)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



