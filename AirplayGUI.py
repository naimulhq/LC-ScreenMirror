import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from AirplayClient import AirplayClient

class AirplayGUI:
    def __init__(self):
        self.WelcomeScreen()
        self.userInputScreen()
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
        userInputWindow.geometry('400x200')
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
        self.server.geometry("400x200")
        connecting = tk.Label(text="Waiting for Connection . . .")
        connecting.pack()
        self.server.mainloop()

if __name__ == '__main__':
    GUI = AirplayGUI()