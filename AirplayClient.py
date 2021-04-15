import socket
import pyautogui
import numpy as np
import cv2
import pickle
import zlib
from tkinter import messagebox
import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
import threading


class AirplayClient:
    def __init__(self, **kwargs):

        self.HOSTIP = None if (kwargs['host_ip'] == '') else kwargs['host_ip']
        self.PORT = None if (kwargs['port'] == '')  else int(kwargs['port'])
        self.HOSTNAME = None if (kwargs['hostname'] == '')  else kwargs['hostname']
        self.scale_percent = .2 if (kwargs['scale_percent'] == '')  else float(kwargs['scale_percent'])
        self.EndStream = False
        if(self.HOSTIP is None and self.HOSTNAME is None):
            print("Need either hostname or host ip")
            exit()
        else:
            if(self.HOSTIP is None):
                pass
     
    def dataTransfer(self):
        self.EndStream = False
        windowThread = threading.Thread(target=self.GenerateWindow)
        dataThread = threading.Thread(target=self.dataTransferThread)
        windowThread.start()
        dataThread.start()

    def dataTransferThread(self):
        ScreenImage = AirplayClient.getScreen(self.scale_percent)
        image_bytes = pickle.dumps(ScreenImage)
        image_bytes = zlib.compress(image_bytes)
        total_bytes = len(image_bytes)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOSTIP, self.PORT))
            s.sendall(bytes(str(total_bytes),"utf-8"))
            s.recv(1024)
            s.sendall(bytes(str(socket.gethostname()),"utf-8"))
            s.recv(1024)
            while not self.EndStream:
                ScreenImage = AirplayClient.getScreen(self.scale_percent)
                image_bytes = pickle.dumps(ScreenImage)
                image_bytes = zlib.compress(image_bytes)
                s.sendall(bytes(str(len(image_bytes)),"utf-8"))
                s.recv(1024)
                s.sendall(image_bytes)
                result = s.recv(1024)
            s.close()
            self.EndConnection.destroy()
            

    def GenerateWindow(self):
        self.EndConnection = tk.Toplevel()
        self.EndStream = False
        btn = tk.Button(self.EndConnection,text="End Stream", command = self.setBool)
        btn.pack(side='left')
        def on_closing():
            if messagebox.askokcancel("Quit","Do you want to End Stream"):
                self.setBool()
                self.EndConnection.destroy()
        self.EndConnection.protocol("WM_DELETE_WINDOW",on_closing)
        self.EndConnection.update_idletasks()
        self.EndConnection.update()

    
    def setBool(self):
        self.EndStream = True

    def getScreen(scale_percent):
        ScreenImage = np.array(pyautogui.screenshot())
        ScreenImage = cv2.cvtColor(ScreenImage,cv2.COLOR_BGR2RGB)
        width = int(ScreenImage.shape[1] * scale_percent) 
        height = int(ScreenImage.shape[0] * scale_percent)
        dsize = (width, height)
        return cv2.resize(ScreenImage, dsize)

