# Lucid Circuit Screen Mirroring Application

 In order to use the application, you will need to install the software in the client device and server device.
 
 Run the following commands:
```
mkdir LucidCircuit
cd LucidCircuit
git clone https://github.com/naimulhq/LC-ScreenMirror
./install.sh
```

# Home Screen
<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/LCWelcomeScreen.png>

* Choose Client if the device you are using is the device you would like to display on a different device.
* Choose Server if the device you are using is the device that will be recieveing the stream.

# Client Menu
<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/ClientSide.png>

* You will need to enter the Host IP and Port Number. Default is 1800. All other entries are optional.
* If you are unaware of the device, you can find the device you are trying to connect to by selecting Find Device.
* Scale Percent is optional but different values will result in different appearences of your screen on the server side. 

# Find Devices Menu
<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/FindDevices.png>

* Select device that appears in list and put value for scale percent
* Click connect to connect to the device chosen

# Server Menu
<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/ServerBeforeConnection.png>

* Server will listen for client connection

<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/ServerAfterConnection.png>

* Once server finds client connection, server will be prompted to accept or refuse connection.
* Accepting will begin the streaming process.
* Refusing will sever connection between the client and server and return to home screen.


# Server Side Display
<img src = https://github.com/naimulhq/LC-ScreenMirror/blob/main/images/MirrorStreaming.png>

* The server gets a screenshot from the client side and displays the image using OpenCV.
* User can click End Stream to sever the connection to the server device.
