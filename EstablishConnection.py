import bluetooth

class ScreenMirrorConnection:
    def __init__(self):
        pass

    def findNearbyDevices(self):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=20)
        except OSError:
            print("Turn on Bluetooth")
            exit()
        print("Found {} devices.".format(len(nearby_devices)))
        return nearby_devices


    def EstablishConnection(self,nearby_devices):
        address = []
        count = 1
        port = 1
        for addr,name in nearby_devices:
            print(str(count) + ". Address: {} - Name: {}".format(addr,name))
            address.append(addr)
            count += 1

        device_number = int(input("Choose a device: "))
        if device_number <= 0 or device_number > len(nearby_devices):
            print("Wrong Number")
            exit()
        else:
            addr = address[device_number-1]

        try:
            soc = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            soc.connect((addr,port))
        except bluetooth.btcommon.BluetoothError as err:
            print("Error. Unable to connect!")
        

if __name__ == '__main__':
    conn = ScreenMirrorConnection()
    nearby_devices = conn.findNearbyDevices()
    conn.EstablishConnection(nearby_devices)