import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from AirplayClient import AirplayClient
from AirplayServer import serverConnection, acceptData
import concurrent.futures

class AirplayGUI:
    def __init__(self):
        self.WelcomeScreen()
        pass
    
    def getInfo(self):
        ip = self.ipEntry.get()
        hostname = self.hostnameEntry.get()
        port = self.portEntry.get()
        scale=self.scaleEntry.get()
        client = AirplayClient(port=port,host_ip=ip,hostname=hostname,scale_percent=scale)
        client.dataTransfer()
        

    def userInputScreen(self):
        self.welcome.destroy()
        userInputWindow = tk.Tk()
        userInputWindow.title("LC - Screen Mirroring")
        
        ipInput = tk.Label(text="Host IP:")
        self.ipEntry = tk.Entry()

        hostnameInput = tk.Label(text="Hostname: ")
        self.hostnameEntry = tk.Entry()

        portInput = tk.Label(text="Port: ")
        self.portEntry = tk.Entry()

        scaleInput = tk.Label(text="Scale Percentage(Between 0 - 1): ")
        self.scaleEntry = tk.Entry()

        btn = tk.Button(userInputWindow,text="Submit", command = self.getInfo)
        btn2 = tk.Button(userInputWindow,text="I don't know", command = userInputWindow.destroy)



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
        self.server = tk.Tk()
        self.server.title("Server Setup")
        self.server.resizable(0,0)
       
        btn1 = tk.Button(self.server,text="Connect",command=self.TransmitData)
        btn1["state"] = "disabled"
        btn2 = tk.Button(self.server,text="Refuse", command=self.WelcomeScreen)
        btn2["state"] = "disabled"
        texts = tk.StringVar(self.server)
        texts.set("Waiting for Connection . . .")
        connecting = tk.Label(self.server,textvariable=texts)
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