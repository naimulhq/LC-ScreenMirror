import socket
import pyautogui
import numpy as np
import cv2
import pickle


class AirplayClient:
    def __init__(self, **kwargs):

        self.HOSTIP = None if not ('host_ip' in kwargs) else kwargs['host_ip']
        self.PORT = None if not ('port' in kwargs) else kwargs['port']
        self.HOSTNAME = None if not ('hostname' in kwargs) else kwargs['hostname']
        self.scale_percent = .7 if not ('scale_percent' in  kwargs) else kwargs['scale_percent']

        if(self.HOSTIP is None and self.HOSTNAME is None):
            print("Need either hostname or host ip")
            exit()
        else:
            if(self.HOSTIP is None):
                pass
     
    def dataTransfer(self):
        
        ScreenImage = AirplayClient.getScreen(self.scale_percent)
        image_bytes = pickle.dumps(ScreenImage)
        total_bytes = len(image_bytes)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOSTIP, self.PORT))
            s.sendall(bytes(str(total_bytes),"utf-8"))
            s.recv(1024)
            while True:
                ScreenImage = AirplayClient.getScreen(self.scale_percent)
                image_bytes = pickle.dumps(ScreenImage)
                print("Length: ", len(image_bytes))
                s.sendall(image_bytes)
                result = s.recv(1024)
                print("Result: ", result.decode("utf-8"))
    
    def getScreen(scale_percent):
        ScreenImage = np.array(pyautogui.screenshot())
        ScreenImage = cv2.cvtColor(ScreenImage,cv2.COLOR_BGR2RGB)
        width = int(ScreenImage.shape[1] * scale_percent) 
        height = int(ScreenImage.shape[0] * scale_percent)
        dsize = (width, height)
        return cv2.resize(ScreenImage, dsize)

if __name__ == '__main__':
    client = AirplayClient(port=1800,host_ip='')
    client.dataTransfer()