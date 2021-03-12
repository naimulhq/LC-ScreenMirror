import socket
import pyautogui
import numpy as np
import cv2
import pickle


class AirplayClient:
    def __init__(self):
        pass
    
    def dataTransfer(self):
        HOST = ''  # The server's hostname or IP address
        PORT = 1800       # The port used by the server

        # Create a socket which will transfer data.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                ScreenImage = AirplayClient.getScreen()
                image_bytes = pickle.dumps(ScreenImage)
                print("Length: ", len(image_bytes))
                s.sendall(image_bytes)
                result = s.recv(1024)
                print("Result: ", result.decode("utf-8"))
    
    def getScreen():
        ScreenImage = np.array(pyautogui.screenshot())
        ScreenImage = cv2.cvtColor(ScreenImage,cv2.COLOR_BGR2RGB)
        scale_percent = 70
        width = int(ScreenImage.shape[1] * scale_percent / 100)
        height = int(ScreenImage.shape[0] * scale_percent / 100)
        dsize = (width, height)
        return cv2.resize(ScreenImage, dsize)

if __name__ == '__main__':
    client = AirplayClient()
    client.dataTransfer()