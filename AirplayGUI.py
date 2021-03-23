import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from AirplayClient import AirplayClient
from AirplayServer import serverConnection, acceptData
import concurrent.futures
import os

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
        userInputWindow = tk.Tk()
        userInputWindow.title("LC - Screen Mirroring")

        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(userInputWindow,image=img)

        ipInput = tk.Label(text="Host IP:")
        self.ipEntry = tk.Entry()

        hostnameInput = tk.Label(text="Hostname: ")
        self.hostnameEntry = tk.Entry()

        portInput = tk.Label(text="Port: ")
        self.portEntry = tk.Entry()

        scaleInput = tk.Label(text="Scale Percent(Value between 0 and 1): ")
        self.scaleEntry = tk.Entry()

        btn = tk.Button(userInputWindow,text="Submit", command = self.getInfo)
        btn2 = tk.Button(userInputWindow,text="Find Devices", command = self.findDevices)
        
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
        btn2.pack(side='right') 
        
 
        userInputWindow.mainloop()

    def findDevices(self):
        os.system("nmap -sn * > scans.txt")
        scanfile = open('scans.txt','r')
        lines = scanfile.readlines()
        del lines[0]
        del lines[len(lines)-1]
        i = 0
        hostnames = []
        ips = []
        while(i < len(lines)):
            temp_list = lines[i].split()
            hostnames.append(temp_list[4])
            ips.append(temp_list[4])
            i += 2
        self.findDevicesWindow = tk.Toplevel()
        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(self.findDevicesWindow,image=img)
        devices_listbox = tk.Listbox(self.findDevicesWindow)
        panel.pack()
        devices_listbox.pack(pady=15)
        for item in hostnames:
            devices_listbox.insert("end",item)
        self.findDevicesWindow.mainloop()

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
        self.welcome.quit
        self.server = tk.Toplevel()
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
            f1 = executor.submit(serverConnection)
            self.conn,addr = f1.result()
            texts.set("{} is trying to connect. \nDo you accept?".format(addr))
            btn1["state"] = "normal"
            btn2["state"] = "normal"

    def TransmitData(self):
        acceptData(self.conn)


if __name__ == '__main__':
    GUI = AirplayGUI()