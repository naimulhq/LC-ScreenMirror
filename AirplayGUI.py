import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image

class AirplayGUI:
    def __init__(self):
        self.WelcomeScreen()
        self.userInputScreen()
        pass
    
    def getInfo(self):
        ip = self.ipEntry.get()
        hostname = self.hostnameEntry.get()

    def userInputScreen(self):
        userInputWindow = tk.Tk()
        userInputWindow.title("LC - Screen Mirroring")
        userInputWindow.geometry('400x200')
        ipInput = tk.Label(text="Host IP:")
        self.ipEntry = tk.Entry()

        hostnameInput = tk.Label(text="Hostname: ")
        self.hostnameEntry = tk.Entry()

        btn = tk.Button(userInputWindow,text="Submit", command = self.getInfo)
        btn2 = tk.Button(userInputWindow,text="I don't know", command = userInputWindow.destroy)

        ipInput.pack()
        self.ipEntry.pack()
        hostnameInput.pack()
        self.hostnameEntry.pack()
        btn.pack(side='left')
        btn2.pack(side='right') 
        
 
        userInputWindow.mainloop()

    def WelcomeScreen(self):
        welcome = tk.Tk()
       
        img = ImageTk.PhotoImage(Image.open('LC.png'))
        panel = tk.Label(welcome,image=img)
        btn1 = tk.Button(welcome,text="Client",command=welcome.destroy)
        btn2 = tk.Button(welcome,text="Server", command=welcome.destroy)
        panel.pack()
        btn1.pack(side='left')
        btn2.pack(side='right')
        welcome.mainloop()
        

if __name__ == '__main__':
    GUI = AirplayGUI()