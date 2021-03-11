import socket
import pyautogui
import numpy as np
import cv2
import pickle



HOST = '192.168.1.120'  # The server's hostname or IP address
PORT = 1800       # The port used by the server

# Create a socket which will transfer data.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        pyautogui.screenshot("screen.png")
        image = cv2.imread("screen.png")
        image_bytes = pickle.dumps(image)
        print("Length: ", len(image_bytes))
        s.sendall(image_bytes)
        result = s.recv(1024)
        print("Result: ", result.decode("utf-8"))
    

