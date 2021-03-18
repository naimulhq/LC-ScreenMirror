import socket
import cv2
import numpy as np

import pickle

# Create a socket that will recieve data
def serverConnection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = ""
        port = 1800
        s.bind((host,port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            if conn != None: 
                return conn, addr

def acceptData(conn):
    with conn:
        size_data = int(conn.recv(1024))
        conn.send(bytes("Size Recieved!", "utf-8"))
        hostname = (conn.recv(1024)).decode()
        conn.send(bytes("Name Recieved!", "utf-8"))
        while True:
            part = conn.recv(size_data,socket.MSG_WAITALL)
            part = pickle.loads(part)
            conn.send(bytes("Recieved","utf-8"))
            cv2.imshow(hostname,part)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def previewScreen(conn):
    pass
