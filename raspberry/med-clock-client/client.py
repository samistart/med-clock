import bluetooth
from time import time

devices = {}

def scan():
        timeStamp = int(time.time())
        nearby_devices = bluetooth.discover_devices(duration=1,lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
                if(addr not in devices):#add new device
                        devices[addr] = (name, timeStamp)
                        print("new device:   %s - %s added on: %s" % (addr, name, str(devices[addr][1])))
                else:
                        #update timestime
                        devices[addr]=(name, timeStamp)
                        print("updated device: %s - %s, new time: %s" % (addr, name, str(devices[addr][1])))
        return timeStamp

def remove_before_time(timeStamp):
        from pprint import pprint
        #pprint(devices)
        for device, data in devices.items():
                if data[1] < timeStamp:
                        print("removing device: %s - %s, addedTime: %s" % (device, data[0], data[1]))
                        del devices[device]
                
def main():
        while(True):
                scanTime = scan()
                remove_before_time(scanTime - 10)
                time.sleep(5)
