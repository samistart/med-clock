import bluetooth
import time
from tornado.httpclient import HTTPClient, HTTPRequest
from urllib import urlencode


devices = {}

def enterStage(addr, timestamp):
        client = HTTPClient()

        body = {"experiment_id": 1, "patient_id": 1, "stage_id": 1, "patient": addr, "timestamp": timestamp}


        response = client.fetch("http://127.0.0.1:5000/api/stage/1",method="POST", body=urlencode(body), headers=urlencode({}))

        print(response.body)
        client.close()
        return

def leaveStage(addr, timestamp):
        client = HTTPClient()
        body = {"experiment_id": 1, "patient_id": 1, "stage_id": 1, "patient": addr, "timestamp": timestamp}

        response = client.fetch("http://127.0.0.1:5000/api/stage/1",method="POST", body=urlencode(body), headers=urlencode({}))

        print(response.body)
        client.close()
        return

def scan():
        timeStamp = int(time.time())
        nearby_devices = bluetooth.discover_devices(duration=1,lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
                if(addr not in devices):#add new device
                        devices[addr] = (name, timeStamp)
                        print("new device:   %s - %s added on: %s" % (addr, name, str(devices[addr][1])))
                        enterStage(addr, timeStamp)
                else:
                        #update timestime
                        devices[addr]=(name, timeStamp)
                        print("updated device: %s - %s, new time: %s" % (addr, name, str(devices[addr][1])))
                        leaveStage(addr,timeStamp)
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
