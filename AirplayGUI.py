import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from AirplayClient import AirplayClient
from AirplayServer import serverConnection, acceptData
import concurrent.futures
import os
import pickle
import cv2
import time

class AirplayGUI:
    def __init__(self):
        self.WelcomeScreen()
       
    def getInfo(self):
        ip = self.ipEntry.get()
        hostname = self.hostnameEntry.get()
        port = self.portEntry.get()
        scale = self.scaleEntry.get()
        client = AirplayClient(port=port,host_ip=ip,hostname=hostname,scale_percent=scale)
        client.dataTransfer()

    def userInputScreen(self):
        self.welcome.destroy()
        self.userInputWindow = tk.Tk()
        self.userInputWindow.title("Client Information")

        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(self.userInputWindow,image=img)

        ipInput = tk.Label(text="Host IP:")
        self.ipEntry = tk.Entry()
        

        hostnameInput = tk.Label(text="Hostname: ")
        self.hostnameEntry = tk.Entry()

        portInput = tk.Label(text="Port: ")
        self.portEntry = tk.Entry()

        scaleInput = tk.Label(text="Scale Percent(Value between 0 and 1): ")
        self.scaleEntry = tk.Entry()

        btn = tk.Button(self.userInputWindow,text="Submit", command = self.getInfo)
        btn2 = tk.Button(self.userInputWindow,text="Find Devices", command = self.findDevices)
        returnHomeButton = tk.Button(self.userInputWindow,text="Home", command = self.goHomeFromInputScreen)
        
        panel.pack()
        ipInput.pack()
        self.ipEntry.pack()
        hostnameInput.pack()
        self.hostnameEntry.pack()
        portInput.pack()
        self.portEntry.pack()
        scaleInput.pack()
        self.scaleEntry.pack()
        btn.pack(side='left')
        btn2.pack(side='left')
        returnHomeButton.pack(side='right') 
        
 
        self.userInputWindow.mainloop()

    def goHomeFromInputScreen(self):
        self.userInputWindow.destroy()
        self.WelcomeScreen()

    def findDevices(self):
        os.system("nmap -sn  > scans.txt")
        scanfile = open('scans.txt','r')
        lines = scanfile.readlines()
        del lines[0]
        del lines[len(lines)-1]
        i = 0
        self.hostnames = []
        self.ips = []
        while(i < len(lines)):
            temp_list = lines[i].split()
            if(len(temp_list) == 5):
                i+=2
                continue
            self.hostnames.append(temp_list[4])
            a_ip = temp_list[5].replace('(','')
            a_ip = a_ip.replace(')','')
            self.ips.append(a_ip)
            i += 2
        self.findDevicesWindow = tk.Toplevel()
        self.findDevicesWindow.title("Find Devices")
        scale = tk.Label(self.findDevicesWindow,text="Scale Percent(Value between 0 and 1): ")
        self.scaleVal = tk.Entry(self.findDevicesWindow)
        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(self.findDevicesWindow,image=img)
        connectButton = tk.Button(self.findDevicesWindow,text="Connect",command=self.connectUsingDevice)
        homeButton = tk.Button(self.findDevicesWindow,text="Home",command=self.WelcomeScreen)
        self.devices_listbox = tk.Listbox(self.findDevicesWindow)
        panel.pack()
        self.devices_listbox.pack(pady=10)
        scale.pack()
        self.scaleVal.pack()
        connectButton.pack(side='left')
        homeButton.pack(side='right')
        for item in self.hostnames:
            self.devices_listbox.insert("end",item)
        self.findDevicesWindow.mainloop()

    def connectUsingDevice(self):
        name = self.devices_listbox.get(tk.ANCHOR)
        scale = self.scaleVal.get()
        for i in range(len(self.hostnames)):
            if self.hostnames[i] == name:
                ip = self.ips[i]
                break
        client = AirplayClient(host_ip=ip,hostname='',port=1800,scale_percent=scale)
        client.dataTransfer()
        

    def WelcomeScreen(self):
        self.welcome = tk.Tk()
        self.welcome.title("Welcome to LC - Screen Mirroring")
        self.welcome.resizable(0,0)
        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(self.welcome,image=img)
        prompt = tk.Label(text="Choose between Client or Server Device")
        btn1 = tk.Button(self.welcome,text="Client",command=self.userInputScreen)
        btn2 = tk.Button(self.welcome,text="Server", command=self.serverConnectionScreen)
        panel.pack()
        prompt.pack()
        btn1.pack(side='left')
        btn2.pack(side='right')
        self.welcome.mainloop()
        
    def serverConnectionScreen(self):
        self.welcome.destroy()
        self.server = tk.Tk()
        self.server.title("Server Setup")
        self.server.resizable(0,0)
        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(self.server,image=img)
        btn1 = tk.Button(self.server,text="Connect",command=self.TransmitData)
        btn1["state"] = "disabled"
        btn2 = tk.Button(self.server,text="Refuse", command=self.WelcomeScreen)
        btn2["state"] = "disabled"
        texts = tk.StringVar(self.server)
        texts.set("Waiting for Connection . . .")
        connecting = tk.Label(self.server,textvariable=texts)
        panel.pack()
        connecting.pack()
        btn1.pack(side='left')
        btn2.pack(side='right')
        self.server.update_idletasks()
        self.server.update()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                f1 = executor.submit(serverConnection)
                self.conn,addr = f1.result()
                texts.set("{} is trying to connect. \nDo you accept?".format(addr))
                panel.configure(image=img)
                panel.image = img
                btn1["state"] = "normal"
                btn2["state"] = "normal"
            except OSError:
                temp_window = tk.Toplevel()
                temp_window.title("Error")
                temp_window.resizable(0,0)
                img = ImageTk.PhotoImage(Image.open('LC.png'))
                panel = tk.Label(temp_window,image=img)
                pickleLabel = tk.Label(temp_window,text="Server is already running. Close Window!")
                panel.pack()
                pickleLabel.pack()
                temp_window.mainloop()
    

    def TransmitData(self):
        try:
            acceptData(self.conn)
        except (pickle.UnpicklingError, ConnectionResetError) as e:
            cv2.destroyAllWindows()
            temp_window = tk.Toplevel()
            temp_window.title("Server Error")
            temp_window.resizable(0,0)
            img = ImageTk.PhotoImage(Image.open('LC.png'))
            panel = tk.Label(temp_window,image=img)
            pickleLabel = tk.Label(temp_window,text="Connection Severed by Client during streaming!")
            panel.pack()
            pickleLabel.pack()
            temp_window.update_idletasks()
            temp_window.update()
            time.sleep(1)
            temp_window.destroy()
            self.server.destroy()
            self.WelcomeScreen()

if __name__ == '__main__':
    GUI = AirplayGUI()
